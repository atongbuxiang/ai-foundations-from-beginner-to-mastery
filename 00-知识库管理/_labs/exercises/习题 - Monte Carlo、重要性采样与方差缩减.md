---
type: exercise
status: draft
area: [math/probability, math/statistics, ai/probabilistic-computation]
topic: "Monte Carlo、重要性采样与方差缩减"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Monte Carlo、重要性采样与方差缩减]]"]
related: ["[[概率论与数理统计 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - Monte Carlo、重要性采样与方差缩减]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - Monte Carlo、重要性采样与方差缩减

> [!abstract] 训练目标
> 检查能否从目标 measure 推导估计器，区分无偏/一致/有限方差，诊断 support 与权重退化，并从协方差、分层或条件期望真正证明方差降低。

## 使用方式

1. 每题先写目标 $\mu=\mathbb E_p[f]$ 与实际样本分布；
2. estimator 的分子、分母和归一化常数必须明确；
3. 同时检查数学条件、数值稳定和实验复现；
4. 把“结果错、误差条错、权重退化、支持遗漏、随机流错误”分别记录。

## A. 识别与复述

### PROB-MC-A01

对 simple Monte Carlo 估计器，分别陈述无偏性、方差、SLLN 和 CLT 的条件与结论。解释为什么“无偏 + $n$ 很大”仍不足以保证当前结果可靠。

### PROB-MC-A02

比较普通 IS 与 SNIS：何时使用、估计公式、有限样本偏差、一致性和渐近方差分别有什么差别？写出必须满足的支持条件。

### PROB-MC-A03

比较权重 ESS、MCMC autocorrelation ESS 与独立重复数。解释它们为什么不能互换，并给出一个可信 Monte Carlo 报告的最低字段。

## B. 手算与构造

### PROB-MC-B01

用 $X_i\sim U(0,1)$ 估计

$$
\mu=\int_0^1x^2dx.
$$

求估计器的精确均值、方差和 $n=10^4$ 时的理论 MCSE。若某次运行样本标准差为 $0.300$，给出估计 MCSE。

### PROB-MC-B02

目标是 $\mu=\mathbb E_p[X^2]$，$p=N(0,1)$；proposal 为 $q=N(0,2)$，其中第二参数表示方差。写出 $w(x)=p(x)/q(x)$，证明 IS 无偏，并判断二阶矩 $\mathbb E_q[(wX^2)^2]$ 是否有限。

### PROB-MC-B03

归一化权重为

$$
(0.50,0.20,0.10,0.10,0.10).
$$

计算权重 ESS 与最大权重。若对应 $f=(0,0,10,10,10)$，计算 SNIS 估计；解释为什么只看 ESS 无法预测该函数的误差。

## C. 推导与证明

### PROB-MC-C01

从换 measure 推导 IS 的无偏性和方差；用 Cauchy–Schwarz/变分法求 $q^*\propto|f|p$。解释 $f\ge0$ 时零方差 proposal 为什么通常不可直接实现。

### PROB-MC-C02

把 SNIS 写成二维样本均值之比，用多元 CLT 与 Delta 方法推导

$$
\tau^2=
\frac{\operatorname{Var}_q(r(X)[f(X)-\mu])}{(\mathbb E_qr)^2}.
$$

并说明有限样本为何一般有偏。

### PROB-MC-C03

推导 control variate 最优系数与最小方差。随后讨论从同一批样本估计 $\beta$ 会对严格无偏性和 standard error 带来什么问题，提出一种 sample-splitting 方案。

## D. 边界、反例与纠错

### PROB-MC-D01

构造 target $p$ 与 proposal $q$，使 $q$ 漏掉 $p$ 的一个正概率区域。取合适 $f$，说明 IS 估计会稳定收敛到错误值，而且权重在已采区域内可以看起来完全正常。

### PROB-MC-D02

构造一个 IS 例子：估计器无偏但方差无限。说明为什么常规 $s/\sqrt n$ 与 CLT 区间失去依据，以及多 seed/权重图也只能诊断、不能补出缺失的二阶矩。

### PROB-MC-D03

反驳：“使用 logsumexp 后，重要性采样在高维不会再退化。”分别给出数值稳定、统计方差、support mismatch 和维度增长四个层次的解释。

## E. AI 迁移

### PROB-MC-E01

对 latent-variable model

$$
p_\theta(x)=\int p_\theta(x,z)dz,
$$

用 $q_\phi(z\mid x)$ 构造 $K$ 样本 importance estimator。证明密度估计无偏，利用 Jensen 说明 $\mathbb E\log\widehat p_K(x)\le\log p_\theta(x)$，并列出实现中至少五个诊断。

### PROB-MC-E02

在 contextual bandit 离线评估中，行为策略 $q(a\mid s)$、目标策略 $\pi(a\mid s)$。写出 IS 与 SNIS value estimator，说明 positivity、reward boundedness/weight moments、clipping bias 与长 horizon product weights 的问题。

### PROB-MC-E03

设计一次比较两个随机生成算法 A、B 的实验，目标是期望质量差 $\Delta$。使用 common random numbers 降低差值方差，同时给出独立重复、seed 管理、MCSE、计算成本和失败案例的报告格式。说明何时 CRN 反而增大方差。

## 分级提示

### 方向提示

- `B01`：$E[X^2]=1/3,E[X^4]=1/5$；
- `B02`：比较 exponent 中 $x^2$ 的系数；
- `B03`：$\mathrm{ESS}=1/\sum_i\tilde w_i^2$；
- `C02`：对 $g(a,b)=a/b$ 使用 Jacobian $(1/b,-a/b^2)$；
- `D02`：可令 $p$ 比 $q$ 尾更重，使 $p^2/q$ 不可积。

### 结构提示

- `C01`：最小化 $\int f^2p^2/q$，约束 $\int q=1$；
- `D01`：离散两点空间即可构造；
- `E01`：诊断 log-weight、ESS、max weight、seed dispersion、mode coverage。

## 解答入口

完成独立尝试后再打开：[[解答 - Monte Carlo、重要性采样与方差缩减]]。

## 本轮复盘

- 是否把样本来自哪个分布写清楚？
- 是否误把 SNIS 当有限样本无偏？
- 是否把数值稳定当成统计稳定？
- 是否报告 MCSE、ESS、max weight、seed 和失败条件？

