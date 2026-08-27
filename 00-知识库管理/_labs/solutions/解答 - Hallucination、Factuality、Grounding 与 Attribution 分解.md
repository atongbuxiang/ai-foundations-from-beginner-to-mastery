---
type: solution
status: verified
area: [language-models, evaluation, factuality]
topic: "[[Hallucination、Factuality、Grounding 与 Attribution 分解]]"
exercise: "[[习题 - Hallucination、Factuality、Grounding 与 Attribution 分解]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Hallucination、Factuality、Grounding 与 Attribution 分解

## A. 识别与复述

### LM61-A01
Truth 问命题在指定时点的世界状态中是否真；task correctness 问是否符合题目/reference 契约；grounding 问给定 context 是否支持；citation correctness 问具体被引 span 是否蕴含对应 claim；attribution completeness 问所有应引用 claims 中有多少被充分覆盖。它们可独立取不同值。

### LM61-A02
长句可能混合实体、时间、因果和数值，必须拆成可判真的 atomic claims；“现任”“已批准”依赖 as-of 时间；来源之间冲突时，监管原文、同行评议、博客等权威级别不同。不固定这三项，标注者甚至不在判断同一事件。

### LM61-A03
Intrinsic 通常指与输入/context 冲突，extrinsic 指输入未给出、需外部知识判断的断言。但开放域问答允许外部知识，严格摘要可能禁止；同一语句的类别由 task contract 决定，不能脱离任务绝对化。

## B. 手算与构造

### LM61-B01
若每个 claim 等权，atomic factual precision 为 $6/8=.75$。还应报告 claim 拆分规则、不可判定数与标注一致性。

### LM61-B02
Citation precision 为 $4/5=.8$；claim coverage 为 $6/10=.6$。前者分母是实际 citations，后者分母是需证据的 claims，所以高 precision 可以与低 coverage 并存。

### LM61-B03
Unweighted precision 为 $2/3\approx.667$。总权重为 $1+3+2=6$，正确 claim 权重为 $1+2=3$，weighted precision 为 $3/6=.5$。权重必须预注册，不能看到错误后临时调。

## C. 推导与证明

### LM61-C01
令 $J$ 为 citations，$C^\star$ 为所有需引用 claims，$s_j=1$ 表示 citation $j$ 支持其绑定 claim，$a_c=1$ 表示 claim $c$ 至少有充分证据。则
$$
\mathrm{CitPrec}=\frac{\sum_{j\in J}s_j}{|J|},\qquad
\mathrm{Completeness}=\frac{\sum_{c\in C^\star}a_c}{|C^\star|}.
$$
一个以“已经给出的引用”为分母，另一个以“应该支持的命题”为分母。

### LM61-C02
反例即可证明：回答含 10 个需支持 claims，只给其中 1 个配了完全正确的 citation。Citation precision 是 1，但 completeness 只有 $.1$。因此 $\forall j,s_j=1$ 不蕴含 $\forall c,a_c=1$。

### LM61-C03
自动器先检索候选文档 $R(c)$，再切出 spans，最后用 entailment/judge 判支持。真 claim 的假阴性可能来自检索漏召回、文档时间/权限缺失、切分截断关键上下文、共指未解析、蕴含模型领域外或阈值过高。每层都需保存 trace，不能把最终 0 全归因于生成模型。

## D. 边界、反例与纠错

### LM61-D01
True-but-ungrounded：context 只给法国首都，回答额外说“东京是日本首都”；该命题为真但未由给定 context 支持。Grounded-but-false：过期资料写“某人仍任 CEO”，回答忠实复述；它受文档支持，但在当前时点为假。

### LM61-D02
URL 可能不存在、与 claim 无关、只支持邻近主题、来自低权威来源，或被回答曲解。必须解析 claim↔citation 绑定、可访问性、来源权威、时间和 entailment；“有 URL”只是格式事件。

### LM61-D03
若 reference 在 $t_0$ 冻结，而世界在 $t_1$ 更新，按旧 reference 的 EM/事实标签会把当前正确答案判错。需给 benchmark 加 knowledge cutoff/as-of，更新 reference 或把相对时点作为输入，并保留不可判定/冲突类别。

## E. AI 迁移

### LM61-E01
每行保存 response_id、claim_id、原文 span、规范化命题、实体/关系/数值/时点、重要度、citation_ids；证据表保存 source URL/version/accessed、authority tier、evidence span/offset、支持/反驳/不足标签、标注者和置信。用外键保持 claim—evidence 多对多。

### LM61-E02
预先规定来源优先级（如监管原文高于二手博客）、as-of 时间、相互独立来源需求和冲突状态。高权威来源冲突或均过期时输出“证据冲突/无法确定”，不强行多数表决；保存反证并触发人工复核。

### LM61-E03
先按回答抽样，再在回答内按 claim 重要度分层抽样，给高风险 claims 更高纳入率；估计总体时用逆纳入概率加权。盲标系统身份，双人复核，报告不可判定、组内相关和按 claim cluster 的区间。
