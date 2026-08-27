---
type: concept
status: verified
area: [language-models, rag, multi-hop-retrieval, tools]
node_id: LM-47
aliases: [多跳检索, 迭代 RAG 与图检索]
prerequisites: ["[[Context Construction、Citation、Grounding 与冲突证据]]", "[[Test-time Compute、Search、Verifier 与预算]]"]
related: ["[[RAG 的 Retrieval—Generation—Attribution 评估地图]]", "[[Chain-of-Thought、Scratchpad 与 Faithfulness]]"]
sources: ["[[S-2018-Yang-HotpotQA]]", "[[S-2023-Trivedi-IRCoT]]", "[[S-2024-Asai-Self-RAG]]", "[[S-2023-Su-9632-NBCE]]"]
exercises: ["[[习题 - Multi-hop、Iterative、Graph Retrieval 与 Tool Interface]]"]
solutions: ["[[解答 - Multi-hop、Iterative、Graph Retrieval 与 Tool Interface]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-rag-iterative-state-machine-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Multi-hop、Iterative、Graph Retrieval 与 Tool Interface

> [!abstract] 一句话结论
> 多跳问题中，下一次该搜什么取决于已经找到什么；因此检索从一次排序变成带状态、动作、观察、停止和预算的序贯决策。可见推理文本可以帮助生成查询，却不能自动当作忠实证据链。

## 一、单跳为何不够

问题“游乐设施 Lost Gravity 的制造商来自哪个国家？”可能需要

$$
\text{Lost Gravity}
\to \text{manufacturer Mack Rides}
\to \text{Mack Rides country Germany}.
$$

原始问题未必含第二跳实体 Mack Rides。一次用原问题检索可能只找到设施页面，无法直接命中国家公司信息。第一跳观察改变了第二跳信息需求。

## 二、把检索写成状态机

第 $t$ 步状态

$$
s_t=(x,H_t,E_t,B_t),
$$

其中 $H_t$ 是假设/查询历史，$E_t$ 是证据集合，$B_t$ 是剩余预算。策略选择动作

$$
a_t\sim\pi(a\mid s_t).
$$

动作可为 retrieve(query)、lookup(entity)、follow(edge)、read(span)、verify(claim)、answer 或 abstain。工具返回观察 $o_t$，状态更新

$$
s_{t+1}=F(s_t,a_t,o_t).
$$

停止条件必须显式：证据充分、最大跳数、预算耗尽、查询重复、无新增证据或 verifier 达阈值。

## 三、query rewriting 与 decomposition

三种常见策略：

1. decompose-first：先把问题拆成子问题再分别检索；
2. retrieve—reason interleave：用当前证据产生下一查询；
3. graph traversal：从实体/文档节点沿关系边扩展。

第一种可并行，但早期拆错会固定路径；第二种自适应，却可能把一次生成错误带入后续 query；第三种约束关系，但依赖实体链接和图覆盖。

IRCoT 体现第二类：CoT 生成一小步，用它增强下一次检索，再由新文档继续推理。它提高若干多跳基准，不意味着可见 CoT 就是真实内部因果链。

## 四、证据图与支持图

定义证据图 $\mathcal G=(V,E)$。节点可为实体、文档、span 或 claim，边表示引用、实体关系、时间继承或蕴含。一个答案需要支持子图 $G^\star$，而不只是若干独立 top-score chunks。

对两跳链，joint recall

$$
R_{\mathrm{joint}}
=\mathbf 1\{e_1\in \hat E\land e_2\in\hat E\}.
$$

若两跳独立命中率分别为 $r_1,r_2$，理想独立下联合率 $r_1r_2$；实际第二跳依赖第一跳，不能简单相乘，但算例说明多跳会放大单步损失。

HotpotQA 的 supporting facts 允许同时测 answer 与句级证据，但真实任务不总有唯一 gold chain。

## 五、工具接口合同

每次调用至少保存：

- tool/schema/version；
- query 原文、filter、top-$K$；
- corpus/index snapshot；
- 返回 IDs、scores、spans 与时间；
- latency、token/调用成本；
- retry、timeout、error；
- 调用前状态与调用后状态；
- 哪个 claim 使用了哪个 observation。

工具结果是带 provenance 的 observation，不自动提升为系统指令；tool success 也不等于 factual success。

## 六、自适应检索与反思

固定每段都检索会浪费成本并引入无关上下文；从不检索又依赖参数记忆。可学习 gate：

$$
g_t\in\{\text{retrieve},\text{no-retrieve},\text{continue}\}.
$$

Self-RAG 进一步预测 relevance、support 与 utility 类反思 token。它把控制接口显式化，但这些 token 仍是模型预测。评估要测 retrieval-needed gate 的 precision/recall、额外成本、漏检风险、critic 校准和 gate 错误传播。

## 七、循环、漂移与停止

迭代系统常见退化：

- query drift：逐步偏离原问题；
- confirmation loop：只搜支持当前假设的证据；
- duplicate loop：反复命中同一文档；
- context hopping：来源间不稳定切换；
- tool overuse：简单问题消耗大量调用；
- premature stop：看到部分证据就作答。

防护包括 query 与原问题相似度下界、反证查询、已见 ID 集合、最大 hop、最小新增证据、状态去重和 abstain。

## 八、图解：带预算的多跳状态机

**读图问题**：Multi-hop 检索状态、预算与工具接口中的对象、箭头和比较分母怎样对应正文定义，读者应先核对哪一层？

![[00-知识库管理/_assets/figures/language-models/fig-lm-rag-iterative-state-machine-v1.svg|900]]

> [!figure] 图 LM-47　检索—观察—更新—验证状态机
> 图由本库依据 HotpotQA、IRCoT 与 Self-RAG 的问题结构绘制；不是论文原图。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：蓝色为可审计状态，绿色为外部 observation，紫色为 policy，红色为停止/回退；每条边都减少预算并产生日志。

**图没有证明什么**：自然语言中间步骤的可读性不保证其 faithfulness，也不保证图边来自可靠来源。

## 九、多跳评估

同时报告 per-hop Recall@K、joint evidence/graph path recall、supporting fact precision/recall、answer EM/F1、answer-and-evidence joint、hops/calls/tokens/latency、query drift/loop/premature stop，以及 oracle first-hop / oracle all-evidence。

Oracle first-hop 能定位后续策略；oracle all-evidence 能测 generator/reasoner 上界。

## 十、常见错误与出口标准

错误包括：把检索次数多当多跳；只保存最终答案；用答案正确反推中间 query 正确；无 stop rule；把 reflection token 当人工 verifier；图中存在路径就当文本支持。

完成本节后，应能把系统写成状态—动作—观察—转移—停止，设计两跳 evidence graph 与 joint metric，审计自适应 gate，并以 oracle first-hop/all-evidence 定位失败。

## 十一、来源与练习

- [[S-2018-Yang-HotpotQA]]；
- [[S-2023-Trivedi-IRCoT]]；
- [[S-2024-Asai-Self-RAG]]；
- [[S-2023-Su-9632-NBCE]]；
- [[习题 - Multi-hop、Iterative、Graph Retrieval 与 Tool Interface]]；
- [[解答 - Multi-hop、Iterative、Graph Retrieval 与 Tool Interface]]。
