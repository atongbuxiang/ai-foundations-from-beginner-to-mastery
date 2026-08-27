---
type: solution
status: verified
area: [language-models, masked-language-modeling, pseudo-likelihood]
topic: "[[Masked LM 的 Corruption Law、伪似然与 BERT]]"
exercise: "[[习题 - Masked LM 的 Corruption Law、伪似然与 BERT]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Masked LM 的 Corruption Law、伪似然与 BERT

## A. 识别与复述

### LM11-A01
Clean sequence $X$ 是未破坏监督真值；mask set $M$ 是被选作预测目标的索引；corrupted input $\widetilde X$ 是模型实际观察的序列；targets 是 $\{X_i:i\in M\}$ 及其位置。$M$ 与 $\widetilde X$ 由两个 sampler 关联但不等同。

### LM11-A02
BERT 80/10/10 中选入 $M$ 的位置有 10% 随机替换、10% 保持原值，输入并不显示 `[MASK]`，却照样计 loss。反过来，特殊流程中出现的 mask 字面 token也未必都是监督 target。

### LM11-A03
随机 MLM risk 对随机 mask/corruption 求期望；PLL 对一条 clean sequence 逐位置只遮一个并求条件 log score；normalized joint likelihood 是对完整序列事件求和为 1 的 $p(x)$。前两者不自动提供第三者。

## B. 手算与构造

### LM11-B01
期望选中 15 个 target；其中 `[MASK]` 12 个、随机替换 1.5 个、保持原 token 1.5 个。单条有限序列的整数计数取决于 rounding 与随机抽样，期望可非整数。

### LM11-B02
三次输入是 `[MASK] red fox`、`the [MASK] fox`、`the red [MASK]`。总分
$$\log p(the\mid [MASK],red,fox)+\log p(red\mid the,[MASK],fox)+\log p(fox\mid the,red,[MASK]).$$
符号上简写为 $\sum_i\log p(x_i\mid x_{-i})$。

### LM11-B03
样本 1 平均 $2/1=2$，样本 2 平均 $4/4=1$；先样本平均为 $(2+1)/2=1.5$。全 token mean 为 $(2+4)/(1+4)=1.2$。前者每样本等权，后者每 masked token 等权。

## C. 推导与证明

### LM11-C01
固定事件 $(\widetilde X=\tilde x,i\in M)$，令真实 target 条件为 $q(v)$。条件期望 loss 是 $H(q)+KL(q\|p_\theta)$，故在充分模型类中 $p_\theta^*(v\mid\tilde x,i)=q(v)$，即联合 data–corruption law 诱导的 posterior。

### LM11-C02
若 $i$ 与 $j$ 同时 mask，模型条件中既缺 $X_i$ 也缺 $X_j$，最优为 $p(X_i\mid X_{-(i,j)},\text{corruption metadata})$；逐位置 clean conditional 则为 $p(X_i\mid X_{-i})$，额外知道 $X_j$。除非条件独立或信息冗余，两者不同。

### LM11-C03
对二元正概率联合表，两个方向条件必须诱导相同 odds ratio：
$$\frac{P(X=1\mid Y=1)/P(X=0\mid Y=1)}{P(X=1\mid Y=0)/P(X=0\mid Y=0)}
=\frac{P(Y=1\mid X=1)/P(Y=0\mid X=1)}{P(Y=1\mid X=0)/P(Y=0\mid X=0)}.$$
任意独立输出的神经条件表没有强制满足该环一致性，故未必存在共同联合表。

## D. 边界、反例与纠错

### LM11-D01
MLM 只要求从 corrupted context 预测选定 clean targets。80/10/10、15% rate、WordPiece 和特殊 token exclusions 是 BERT 实例的 sampler 配置；可换成 whole-word、span、100% mask 或不同 rate 而仍是 MLM 类目标。

### LM11-D02
PPPL 条件于双向 $x_{-i}$，CLM PPL 条件于 $x_{<i}$；前者还是条件表的伪似然，后者对应链式联合概率。条件信息、forward 次数、denominator 与概率对象均不同，数值大小没有直接胜负含义。

### LM11-D03
同一模型每次验证面对不同 corruption，验证 loss 含额外 Monte Carlo 噪声；checkpoint 排名可能由 mask 抽样而非参数质量决定。应固定 validation corruptions/seed，或多次抽样报告均值和不确定性。

## E. AI 迁移

### LM11-E01
断言：特殊/pad token 不被非法选中；targets 永远等于 clean token；未选中位置保持不变；80/10/10 长期频率在容差内；同 seed 完全复现；至少一个 mask/零可选位置行为明确；loss denominator 等于 mask-set 大小而非 `[MASK]` 数。

### LM11-E02
独立 subword mask 让 fertility 高的词拥有更多被部分遮蔽机会，模型可能从同词未遮 subword轻易恢复；whole-word mask 同时遮整词，减少此泄漏但使每词 target 数随 fertility 增加。跨语言比较要同时按原词/字节和 target token 统计，不能只固定 15% token。

### LM11-E03
高 MLM accuracy 只表明特定 corruption 下的条件恢复好，还可能受 unchanged 分支和频率词影响。要声称 joint distribution，需给出兼容性结构或规范化能量模型及 partition function；否则最多报告 MLM risk/PLL 与下游经验。

## 无提示重做

- [ ] 从 mask-set sampler 写到 loss denominator，不遗漏随机变量。
- [ ] 用一句话区分 PPPL 与 PPL 的条件信息。

