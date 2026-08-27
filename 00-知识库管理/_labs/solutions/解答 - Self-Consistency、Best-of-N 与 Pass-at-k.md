---
type: solution
status: verified
area: [language-models, reasoning, sampling]
topic: "[[Self-Consistency、Best-of-N 与 Pass-at-k]]"
exercise: "[[习题 - Self-Consistency、Best-of-N 与 Pass-at-k]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Self-Consistency、Best-of-N 与 Pass-at-k

## A. 识别与复述

### LM38-A01
Self-consistency 选规范化答案的经验众数；pass-at-k 用 oracle 判断 $k$ 个候选是否至少一个正确；Best-of-N 用 verifier 排序并输出一个。前者是聚合，第二是覆盖率，第三是选择系统。

### LM38-A02
投票和成功计数发生在答案等价类上。若 1/2、0.5、50% 未合并，众数改变；若 parser 错取步骤数字，正确性改变。因此 canonicalizer/parser 是估计量的一部分并需版本化。

### LM38-A03
Oracle coverage $O_N$ 表示集合有正确解；chosen success $S_N$ 表示 selector 选中正确解；regret $O_N-S_N$ 是“有解却没选中”的损失。它把 generator 与 verifier 瓶颈分开。

## B. 手算与构造

### LM38-B01
A 出现 3 次，B/C 各 1 次，故选 A。众数只反映采样分布，若模型共享同一系统性错误，A 可以稳定错误。

### LM38-B02
至少两票正确：$\binom32(0.6)^2(0.4)+(0.6)^3=0.432+0.216=0.648$。该计算依三次独立同分布。

### LM38-B03
$1-\binom{3}{3}/\binom{5}{3}=1-1/10=0.9$。三失败全被选中的唯一坏组合占十种三选组合之一。

## C. 推导与证明

### LM38-C01
$k$ 次全失败概率为 $(1-p)^k$；“至少一次成功”是其补事件，所以概率 $1-(1-p)^k$。独立/同分布是乘法成立的条件。

### LM38-C02
固定 $n$ 个样本中有 $n-c$ 个失败。均匀无放回取 $k$ 的总组合数 $\binom nk$，全失败组合数 $\binom{n-c}{k}$；补事件即公式。当失败数不足 $k$ 时全失败概率为 0。

### LM38-C03
若 selector 选对，则候选集合必存在正确项，所以事件 $S\subseteq O$，概率/样本均值满足 $S_N\le O_N$。等号当且仅当每次存在正确候选时 selector 都选中至少一个正确候选。

## D. 边界、反例与纠错

### LM38-D01
十个候选中一个正确、九个具有同一漂亮错误；oracle pass@10=1，但系统固定输出第一条或 verifier 总偏好漂亮错误，top-1 仍为 0。覆盖不等于可选择性。

### LM38-D02
多数频率不是预测概率与真实频率的校准关系；样本可相关、sampler 可偏、多个错误路径可汇聚同一答案。需用独立数据画 agreement 与 accuracy 的 reliability curve 才能讨论校准。

### LM38-D03
同模型/同 prompt 常重复同一策略，pairwise correlation $\rho>0$。示意 $N_{eff}=N/[1+(N-1)\rho]$；如 $N=20,\rho=.5$，有效量约 $1.9$，说明表面 20 条并非 20 份独立证据。

## E. AI 迁移

### LM38-E01
每个 $N$ 列生成数、oracle coverage、chosen accuracy、regret、invalid rate、unique answers 与成本。再按题目难度/类别分层，避免平均数把 verifier 失败藏在 coverage 中。

### LM38-E02
答案层用 canonicalized unique count/entropy；策略层用结构化步骤或语义 embedding 聚类；首错层由 step verifier/人工标首个非法步。三者分别报告，文本措辞多样不能替代策略多样。

### LM38-E03
在 $N=1,2,4,8,16$ 保存累计 token、verifier calls、并行/串行延迟，并画 oracle/chosen accuracy 随各成本。相同 policy、sampler 和最大长度，超时/失败请求也计预算。
