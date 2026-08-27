---
type: concept
status: verified
area: [language-models, security, prompt-injection, rag, tools]
node_id: LM-67
aliases: [提示注入与工具安全, Tool-RAG 威胁模型]
prerequisites: ["[[指令、消息、Chat Template 与任务序列化合同]]", "[[RAG 的 Retrieval—Generation—Attribution 评估地图]]"]
related: ["[[Jailbreak、Toxicity、Bias 与安全评估]]", "[[Model、API、Tokenizer、Template 版本与复现合同]]"]
sources: ["[[S-2023-Greshake-Indirect-Prompt-Injection]]", "[[S-2023-Liu-Prompt-Injection-Benchmark]]", "[[S-2024-Chen-StruQ]]", "[[S-2025-NIST-Adversarial-ML]]", "[[S-2024-NIST-SSDF-GenAI]]"]
exercises: ["[[习题 - Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]"]
solutions: ["[[解答 - Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-safety-injection-trust-boundary-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型

> [!abstract] 一句话结论
> Prompt injection 的根因不是“用户说了坏话”，而是模型在同一序列中同时处理高可信指令与低可信数据，却缺少可证明的权限隔离；可靠防御必须把 trust boundary 延伸到检索源、工具参数、凭据、动作审批和事后审计。

## 一、先区分三类现象

- **direct injection**：攻击者直接控制用户输入，试图改变应用指令；
- **indirect injection**：攻击内容藏在网页、文档、邮件或工具返回中，由系统检索后送入模型；
- **jailbreak**：更广义地诱使模型绕过行为/安全政策，不一定涉及工具或外部数据。

三者可重叠，但安全后果不同。纯聊天越界主要影响输出；带邮件、支付、代码执行或数据库工具的 agent 还可能造成真实状态改变。

## 二、威胁模型的六元组

把场景写为

$$
\mathcal T=(A,G,K,C,B,S),
$$

其中 $A$ 是资产，$G$ 是攻击目标，$K$ 是攻击者知识，$C$ 是可控通道，$B$ 是查询/迭代/成本预算，$S$ 是成功条件。例：

- 资产：私有文档、OAuth token、用户邮件、工具写权限；
- 可控通道：公开网页正文，而非系统 prompt；
- 能力：可反复更新网页，观察最终回答；
- 目标：让系统执行未授权工具动作；
- 成功：服务端审计日志出现越权状态变更；
- 预算：每文档最多若干变体、每次会话若干调用。

“模型输出一句不合意文字”不能替代对资产损失的定义。

## 三、为什么自然语言分隔不是强隔离

序列化后，system、user、retrieved data 都成为 token。Chat template 提供位置与角色先验，却不是操作系统式权限边界。即使加上“以下仅为数据”，模型仍可能在分布外组合中遵从数据中的祈使结构。

需要区分：

$$
\text{semantic authority}
\ne
\text{execution authority}.
$$

模型可建议动作；真正能否执行应由确定性 policy engine、schema validation、身份和权限系统决定。把高权限 credential 暴露给模型后再要求它“不要使用”，已经破坏 least privilege。

## 四、Tool-RAG 的数据流分析

对每条边记录 source、trust、parser 与 sink：

$$
\text{web}\to\text{retriever}\to\text{prompt}
\to\text{planner}\to\text{tool args}\to\text{executor}.
$$

关键问题：

1. 谁能改变网页/向量库内容？
2. retriever 是否保留来源和签名？
3. 模型能看见哪些秘密？
4. tool 参数是否受类型、范围和业务规则验证？
5. read 与 write 工具是否隔离？
6. 高风险动作是否需要用户确认？
7. tool result 能否再次成为未标记指令？
8. 失败、重试和回滚是否可审计？

## 五、控制按层组合

| 层 | 代表控制 | 解决什么 | 不能单独解决 |
|---|---|---|---|
| 数据 | provenance、可信源、内容净化 | 降低恶意内容进入率 | 未知表达和可信源被攻陷 |
| 序列化 | structured query、role/data 标记 | 增强指令/数据可分性 | 模型并非形式验证器 |
| 模型 | 安全训练、检测器、拒答 | 降低已知攻击成功 | 自适应攻击和权限后果 |
| 工具 | schema、allowlist、最小权限 | 限制可执行动作 | 合法但有害的组合 |
| 交互 | preview、确认、二人审批 | 把高风险决定交回主体 | 用户疲劳和欺骗性界面 |
| 运行 | sandbox、rate limit、监控、rollback | 限制 blast radius | 单次不可逆损害 |

安全来自多层失效不同时发生，不来自某一层“100% 检出”。

## 六、评估：效用与攻击同时存在

构造 benign set $D_b$ 与 attack set $D_a$。至少报告：

$$
\operatorname{ASR}
=\frac{\#\text{攻击达到预注册后果}}{|D_a|},
\qquad
U_b=\frac{\#\text{正常任务正确完成}}{|D_b|}.
$$

全部拒绝可使 ASR 很低但 $U_b\approx0$。还需分 direct/indirect、read/write、权限级别、攻击族和自适应轮次。对多次尝试，若单次独立成功率 $p$，至少一次成功为 $1-(1-p)^k$；现实相关性使该式只作基线。

## 七、确定性授权参考监视器

推荐把工具调用解释为提案 $a$，服务端执行

$$
\operatorname{allow}(a,u,c)
=\mathbf1[
\text{schema}\land
\text{identity}\land
\text{scope}\land
\text{policy}\land
\text{confirmation}
].
$$

模型文本本身不改变 allow。所有被拒与被执行动作都带 request id、来源文档、模型/模板版本、参数哈希和 policy decision。这样即使模型被诱导，blast radius 仍被权限边界限制。

## 八、图解：不可信文档怎样跨越信任边界

**读图问题**：一段外部文档从检索到工具执行跨过哪些边界，哪些控制应放在模型之外？

![[00-知识库管理/_assets/figures/language-models/fig-lm-safety-injection-trust-boundary-v1.svg|900]]

> [!figure] 图 LM-67　Indirect injection 数据流、信任区与参考监视器
> **生成：**本库以无害占位文本绘制 Tool-RAG 架构；不包含可复用注入载荷。

**怎样读图**：把外部内容始终标为低信任；planner 只能提交 typed proposal；policy/identity/confirmation 位于独立高信任执行边界，credential 不回流到模型上下文。

**图没有证明什么**：架构图不证明控制实现正确；allowlist 也不能发现所有业务逻辑滥用，仍需自适应红队、日志和最小 blast radius。

## 九、常见错误与出口标准

错误包括：系统 prompt 当秘密/权限；只测 direct injection；净化所有“命令语气”；模型自审模型；write tool 默认全权限；工具结果无 provenance；只报 ASR 不报效用；固定攻击集过拟合；无版本/预算。

完成后应能为一个 RAG agent 写六元 threat model、画数据流与 trust boundary、定义 ASR/benign utility、设计 least-privilege reference monitor，并解释 structured prompt 为何只是防御层之一。

## 十、来源与练习

- [[S-2023-Greshake-Indirect-Prompt-Injection]]；
- [[S-2023-Liu-Prompt-Injection-Benchmark]]；
- [[S-2024-Chen-StruQ]]；
- [[S-2025-NIST-Adversarial-ML]]；
- [[S-2024-NIST-SSDF-GenAI]]；
- [[习题 - Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]；
- [[解答 - Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]。
