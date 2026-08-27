---
type: exercise
status: draft
area: [learning-theory/pac-bayes, data-dependent-priors]
topic: "[[PAC-Bayes 先验、后验与数据依赖边界]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[PAC-Bayes Bound 的测度变换主线]]", "[[多元高斯分布]]"]
related: ["[[解答 - PAC-Bayes 先验、后验与数据依赖边界]]", "[[互信息与信息论泛化界]]"]
solution: "[[解答 - PAC-Bayes 先验、后验与数据依赖边界]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - PAC-Bayes 先验、后验与数据依赖边界

> [!abstract] 训练目标
> 能审计 prior independence、sample splitting、mixture selection 与 continuous support，推导 Gaussian KL，并把 neural PAC-Bayes 实验写成可复现概率合同。

## A. 识别与复述

### LT-PBPP-A01

分别列出 prior \(P\) 可以与不可以依赖的五类信息；“独立于训练数据”应相对哪一批数据解释？

### LT-PBPP-A02

解释 posterior hyperparameters 可以在 \(S\) 上优化，而 prior hyperparameters 若在同一 \(S\) 上选择为什么要付额外代价。

### LT-PBPP-A03

比较 independent pretraining prior、sample-split prior、fixed mixture prior 与 DP data-dependent prior 的合法性依据和代价。

## B. 手算与数值判断

### LT-PBPP-B01

\(P=\mathcal N(0,4I_2)\)，\(Q=\mathcal N((1,-1)^\top,I_2)\)。计算 \(\operatorname{KL}(Q\|P)\)。

### LT-PBPP-B02

对 \(P=\mathcal N(0,I_d)\)、\(Q_\sigma=\mathcal N(\mu,\sigma^2I_d)\)，写出 KL，并求固定 \(\mu\) 时使 KL 最小的 \(\sigma^2\)。

### LT-PBPP-B03

有三个预声明 priors，weights 为 \((1/2,1/3,1/6)\)。若选第三个，计算额外选择代价 \(\log(1/\pi_3)\)；当 \(m=1000\) 时它对 numerator-per-sample 的贡献是多少？

## C. 推导与证明

### LT-PBPP-C01

从 Gaussian log density 推导一般 multivariate KL 公式。

### LT-PBPP-C02

严格证明：用 \(S_0\) 构造 \(P_{S_0}\)，只在独立 \(S_1\) 上做 PAC-Bayes certificate，joint success probability 仍至少 \(1-\delta\)。

### LT-PBPP-C03

证明 mixture prior \(P_{\rm mix}=\sum_j\pi_jP_j\) 满足
$$
\operatorname{KL}(Q\|P_{\rm mix})
\le\operatorname{KL}(Q\|P_j)+\log(1/\pi_j).
$$

## D. 边界、反例与纠错

### LT-PBPP-D01

解释为什么“pretraining dataset 与 fine-tuning dataset 文件名不同”不足以证明 prior independence，列出至少四种 leakage。

### LT-PBPP-D02

某人用 \(S_0\) 训练 prior，又把 \(S_0\cup S_1\) 的 empirical risk 放入 denominator \(m_0+m_1\)。指出 conditional proof 的断点。

### LT-PBPP-D03

给出一个 support mismatch 导致 \(\operatorname{KL}(Q\|P)=+\infty\) 的离散例子和一个 Gaussian/degenerate 例子。

## E. AI 迁移

### LT-PBPP-E01

审计“预训练 checkpoint 为 prior center、微调解为 posterior center”的完整流程，给出至少十项记录字段。

### LT-PBPP-E02

设计一个 prior-scale grid \(\{\tau_j\}\) 与 Kraft-style weights \(\pi_j\)，使训练后选 \(\tau_j\) 合法；写出最终 complexity。

### LT-PBPP-E03

说明如何对 Monte Carlo empirical Gibbs risk 增加独立 confidence correction，并怎样与 PAC confidence 合并。

