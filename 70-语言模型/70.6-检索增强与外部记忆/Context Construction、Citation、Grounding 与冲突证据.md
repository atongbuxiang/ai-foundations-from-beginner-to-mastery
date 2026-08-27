---
type: concept
status: verified
area: [language-models, rag, grounding, citations]
node_id: LM-46
aliases: [RAG 上下文构造, 引用与证据支持]
prerequisites: ["[[长上下文利用、Lost-in-the-Middle 与推理证据地图]]", "[[ANN Recall、Latency、Reranker 与两阶段检索]]"]
related: ["[[RAG 的 Retrieval—Generation—Attribution 评估地图]]", "[[Chain-of-Thought、Scratchpad 与 Faithfulness]]"]
sources: ["[[S-2021-Izacard-Grave-FiD]]", "[[S-2023-Gao-ALCE]]", "[[S-2021-Petroni-KILT]]", "[[S-2023-Su-9632-NBCE]]"]
exercises: ["[[习题 - Context Construction、Citation、Grounding 与冲突证据]]"]
solutions: ["[[解答 - Context Construction、Citation、Grounding 与冲突证据]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-rag-claim-citation-layout-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Context Construction、Citation、Grounding 与冲突证据

> [!abstract] 一句话结论
> 检索到正确证据只是必要条件。系统还要在有限 token 预算下去重、排序、保留 provenance、表达冲突，并让每个可核查命题指向真正蕴含它的 span；“有引用”不等于“被引用内容支持这句话”。

## 一、retrieved set 不是最终 context

候选集合 $D=\{d_1,\ldots,d_K\}$ 还要经过

$$
X=B(\operatorname{order}(\operatorname{dedup}(
\operatorname{filter}(D)))).
$$

$B$ 是 token budget allocator。filter 处理权限/时间/质量，dedup 合并同源重叠，order 决定位置，allocator 选择 span 与截断。任一环节可丢失原本已召回的证据。

上下文 manifest 至少保存：输入候选及分数、过滤原因、去重簇、最终顺序、每段 token range、被截断 span、来源 ID 与 prompt 模板。

## 二、预算分配

设段落 $i$ 长度为 $\ell_i$，估计效用 $u_i$，总预算 $L$。理想化选择是背包问题：

$$
\max_{a_i\in\{0,1\}}\sum_i a_i u_i,
\qquad
\sum_i a_i\ell_i\le L.
$$

实际效用不是独立可加：两个段落可能重复，也可能必须联合才回答。可加入

$$
U(S)=\sum_{i\in S}u_i
-\lambda\sum_{i<j}\operatorname{sim}(d_i,d_j)
+\gamma\,\operatorname{coverage}(S).
$$

这提醒我们 top-score 截断只是启发式，不是最优定理。

## 三、融合位置与证据竞争

FiD 将每个 question—passage 对独立编码，再让 decoder 跨所有编码状态融合；普通 concat 则先拼接。二者的 token 间交互、位置、复杂度和截断行为不同。

无论架构如何，都要测试：gold 单独输入；gold + irrelevant distractors；gold 放在头/中/尾；相互重复与相互矛盾；增加段落数时 evidence use 与 latency。

## 四、从答案拆到原子命题

令输出拆成可核查 claims

$$
Y=\{c_1,\ldots,c_m\},
$$

每个 claim 引用若干 evidence spans $E(c_i)$。定义 $\operatorname{support}(e,c)$ 为证据是否支持命题。

Citation correctness 可写为

$$
\frac{\sum_i\sum_{e\in E(c_i)}
\mathbf 1\{\operatorname{support}(e,c_i)=1\}}
{\sum_i|E(c_i)|}.
$$

Citation completeness 可写为

$$
\frac{\sum_i\mathbf 1\{\exists e\in E(c_i):
\operatorname{support}(e,c_i)=1\}}
{|\{c_i:\ c_i\text{ 需要外部验证}\}|}.
$$

二者不同：每句话放一个无关引用，完整性表面高但正确性低；只给少量精准引用，正确性高但覆盖不全。

## 五、五个容易混淆的事件

- factuality：命题在世界中是否为真；
- grounding/support：给定证据是否足以支持命题；
- attribution：输出是否连接到正确来源；
- relevance：文档是否与问题有关；
- faithfulness：生成决策是否因这些证据而发生。

真实命题可以未被当前证据支持；被旧来源蕴含的命题可能在当前世界为假；正确引用也不能证明模型因该证据才作答。

## 六、冲突证据

两个来源对命题给相反断言时，不应把 top score 较高直接当真值。协议应考虑：

1. 时间与查询时点；
2. 第一方、同行评议、转述等权威层级；
3. 地区、定义、统计口径；
4. 多个页面是否复制同一上游；
5. 是否应呈现争议而非强行合并。

可输出“来源 A 在 $t_A$ 称……；来源 B 在 $t_B$ 称……”并分别引用。要求唯一值时要说明选择规则和残余不确定性。

## 七、NBCE 给出的边界提醒

科学空间的 NBCE 分析把每个生成片段动态关联到一个 context，并用熵选择与转移惩罚控制跳转。它提供局部 context 选择视角，也明确指出有序 context 与必须耦合多个 context 的困难。

因此“每步选择最自信的一段”不能替代多证据联合推理；低熵也不等于来源真实或命题被支持。

## 八、图解：命题—引用—span 的排版合同

**读图问题**：Context construction、claim、citation 与冲突证据中的对象、箭头和比较分母怎样对应正文定义，读者应先核对哪一层？

![[00-知识库管理/_assets/figures/language-models/fig-lm-rag-claim-citation-layout-v1.svg|900]]

> [!figure] 图 LM-46　从候选卡片到 claim-level citation
> 图由本库按上下文预算和 ALCE 的引用质量维度绘制，采用教材式批注版面。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：左栏是来源卡和有效时间，中栏是去重/排序后的 context，右栏把原子命题连到精确 span；红线表示只相关但不蕴含。

**图没有证明什么**：该图只解释Context construction、claim、citation 与冲突证据的结构和本节样例，不证明任意模型、数据、语言或部署环境都会得到同一性能；真实结论仍需独立实验、区间与版本化工件。


**图没有证明什么**：自动 entailment 分数不能替代高风险场景的人类核验。

## 九、安全与注入

外部文档是不可信数据，不是系统指令。上下文模板应明确数据边界，过滤主动指令式文本，限制工具调用；引用 verifier 不执行文档中的命令。访问控制必须在检索前后验证，日志避免存储无权内容。

## 十、常见错误与出口标准

错误包括：引用整页而非 span；把相关性当支持性；去重后丢 provenance；只留最终 prompt；冲突时多数投票；用低熵当真值；把引用存在率当 correctness。

完成本节后，应能写预算选择目标，区分五个语义事件，手算 citation precision/completeness，设计冲突与注入协议，并用 gold-only / distractor / position 对照识别 context failure。

## 十一、来源与练习

- [[S-2021-Izacard-Grave-FiD]]；
- [[S-2023-Gao-ALCE]]；
- [[S-2021-Petroni-KILT]]；
- [[S-2023-Su-9632-NBCE]]；
- [[习题 - Context Construction、Citation、Grounding 与冲突证据]]；
- [[解答 - Context Construction、Citation、Grounding 与冲突证据]]。
