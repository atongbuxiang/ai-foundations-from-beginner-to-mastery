---
type: exercise
status: draft
area: [learning-theory/pac-bayes, measure-change]
topic: "[[PAC-Bayes Bound 的测度变换主线]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[交叉熵与 KL 散度]]", "[[浓缩不等式]]"]
related: ["[[解答 - PAC-Bayes Bound 的测度变换主线]]", "[[PAC-Bayes 先验、后验与数据依赖边界]]"]
solution: "[[解答 - PAC-Bayes Bound 的测度变换主线]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - PAC-Bayes Bound 的测度变换主线

> [!abstract] 训练目标
> 能从 fixed-h 二项矩、prior averaging、change of measure 与 joint convexity 独立重建 PAC-Bayes-kl theorem，并准确识别 Gibbs predictor 与 prior/posterior 量词。

## A. 识别与复述

### LT-PBMC-A01

定义 \(\widehat R_S(Q)\)、\(R(Q)\)、\(\operatorname{kl}(q\|p)\) 与 \(\operatorname{KL}(Q\|P)\)，说明两个 KL 分别在哪个空间上计算。

### LT-PBMC-A02

用一句带量词的公式写出 PAC-Bayes-kl theorem，并解释为什么 \(Q\) 可以依赖 \(S\)。

### LT-PBMC-A03

区分 Gibbs predictor、majority vote、posterior mean network 与 MAP hypothesis。

## B. 手算与数值判断

### LT-PBMC-B01

\(\mathcal H=\{h_1,h_2,h_3\}\)，\(P=(1/2,1/3,1/6)\)，\(Q=(1/4,1/2,1/4)\)。计算 \(\operatorname{KL}(Q\|P)\)（nats）。

### LT-PBMC-B02

\(m=1000,\delta=0.05,\widehat R_S(Q)=0,\operatorname{KL}(Q\|P)=8\)。计算
$$
c=\frac{\operatorname{KL}(Q\|P)+\log((m+1)/\delta)}m
$$
以及零经验风险的 exact inverse-kl upper bound \(1-e^{-c}\)。

### LT-PBMC-B03

使用 B02 的 \(c\)，计算 Pinsker corollary \(\sqrt{c/2}\)，与 exact zero-risk bound 比较松弛倍数。

## C. 推导与证明

### LT-PBMC-C01

从 Radon–Nikodym density 与 Jensen inequality 证明
$$
\mathbb E_Qf\le\operatorname{KL}(Q\|P)+\log\mathbb E_Pe^f.
$$

### LT-PBMC-C02

对 fixed \(h\) 证明
$$
\mathbb E_S e^{m\operatorname{kl}(\widehat R_S(h)\|R(h))}\le m+1,
$$
明确每个 binomial type term 为什么不超过 \(1\)。

### LT-PBMC-C03

把 C01、C02、Tonelli、Markov 与 Bernoulli-KL joint convexity 拼成完整 PAC-Bayes-kl proof。

## D. 边界、反例与纠错

### LT-PBMC-D01

设 \(P=\mathcal N(0,I_d)\)、\(Q=\delta_w\)。判断 \(Q\ll P\) 是否成立，并说明 bound 为何 vacuous。

### LT-PBMC-D02

反驳：“训练后取 \(P=Q_S\)，KL 为零，因此任何模型都能得到完美 PAC-Bayes certificate。”

### LT-PBMC-D03

构造一个随机变量 \(G\) 使 \(|\mathbb EG|=0\) 但 \(\mathbb E|G|>0\)，说明 expectation 与 realized/high-probability gap 不可偷换。

## E. AI 迁移

### LT-PBMC-E01

为一个 Gaussian-weight neural posterior 写出最小 certificate report：至少列出 prior、posterior、empirical Gibbs risk、KL、confidence、Monte Carlo uncertainty 与部署 predictor。

### LT-PBMC-E02

某实验只测试 center network \(h_{\mu_Q}\)，却把结果代作 \(\widehat R_S(Q)\)。指出错误并给出合法 estimator。

### LT-PBMC-E03

设计 binary-kl upper inverse 的 robust numerical procedure，包括搜索区间、单调性、边界 \(q=0,1\) 与容差。

