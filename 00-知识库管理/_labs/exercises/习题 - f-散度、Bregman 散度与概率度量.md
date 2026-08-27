---
type: exercise
status: draft
area: [math/information-theory, math/statistics, math/geometry, ai/generative-models]
topic: "f-散度、Bregman 散度与概率度量"
difficulty: [A, B, C, D, E]
prerequisites: ["[[f-散度、Bregman 散度与概率度量]]"]
related: ["[[信息论与统计学习接口 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - f-散度、Bregman 散度与概率度量]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - f-散度、Bregman 散度与概率度量

> [!abstract] 训练目标
> 按 density ratio、convex tangent、test-function class 与 ground geometry 区分分布差异；能证明 $f$-divergence 的非负性/DPI，推导 KL–Bregman 与 MMD/Wasserstein，并审计 finite-sample estimator 和 GAN surrogate。

## A. 识别与复述

### INFO-DIST-A01

定义 divergence、pseudometric 与 metric。分别判断 KL、JS、$\sqrt{\rm JS}$、TV、squared Euclidean、$W_p$、MMD 在什么条件下属于哪一类。

### INFO-DIST-A02

定义 $f$-divergence、Bregman divergence 与 IPM。说明它们分别依赖 density ratio、coordinates/convex potential 与 function class 的含义，并举出跨家族成员。

### INFO-DIST-A03

写出 forward KL、reverse KL、Pearson $\chi^2$、squared Hellinger、TV 与 JS 的 $f(t)$。解释向 $f$ 加 $a(t-1)$ 为什么不改变 divergence。

## B. 手算与构造

### INFO-DIST-B01

对

$$
P=(0.75,0.25),\qquad Q=(0.5,0.5),
$$

以 nats 计算 $D(P\|Q)$、$D(Q\|P)$、TV、本章 convention 的 squared Hellinger 与 JS。检查对称性和 Pinsker inequality。

### INFO-DIST-B02

令 $F(u)=\sum_i u_i\log u_i$。对上题 $P,Q$ 计算 $B_F(P,Q)$ 并核对 KL。再令 $G(u)=\tfrac12\|u\|_2^2$，计算 $B_G(P,Q)$，说明数值为何没有 probability-ratio 的不对称性。

### INFO-DIST-B03

$P=\delta_0,Q=\delta_\theta$，ground metric 为 Euclidean，RBF kernel 为

$$
k(x,y)=e^{-(x-y)^2/(2\sigma^2)}.
$$

求 $\theta\ne0$ 时 KL、JS、TV、$W_1$ 与 MMD$^2$；令 $\theta\to0$，比较极限。

## C. 推导与证明

### INFO-DIST-C01

用 Jensen 证明 $D_f(P\|Q)\ge0$，给出严格 equality 条件；再通过 output likelihood ratio 是 conditional expectation，证明相同 Markov kernel 下的 data processing inequality。

### INFO-DIST-C02

从 Fenchel inequality 推导

$$
D_f(P\|Q)\ge E_PT-E_Qf^*(T),
$$

说明何时对 $T$ 取 supremum 得 equality。对 KL 的 $f(t)=t\log t$ 求 conjugate，并写出对应 variational form。

### INFO-DIST-C03

证明 exponential family 中

$$
D(p_\eta\|p_{\eta'})=B_A(\eta',\eta).
$$

再从 RKHS reproducing property 推导 MMD mean-embedding norm 与 kernel expectation 展开。

## D. 边界、反例与纠错

### INFO-DIST-D01

给出一个具体 Bernoulli 数值反例，证明 symmetrized KL 虽对称仍不满足 triangle inequality。说明为什么 symmetry 不是 metric 的充分条件。

### INFO-DIST-D02

从同一 continuous distribution 独立抽取两个无重复 finite samples，形成 empirical measures。证明二者 supports 几乎必然不交，因此 empirical TV=1；解释这为何不表示 population distributions 不同。

### INFO-DIST-D03

令 kernel 为 linear kernel $k(x,y)=xy$。构造两个不同 distributions 具有相同 mean，从而 MMD=0。说明 characteristic kernel 条件为何不是装饰，并比较换 RBF kernel 后的结论。

## E. AI 迁移

### INFO-DIST-E01

某 GAN 报告 discriminator train objective 持续下降，便声称 population JS divergence 精确下降。写出 population divergence、empirical variational objective、restricted critic、inner optimization 与 generator surrogate 五层审计。

### INFO-DIST-E02

为以下三个任务分别选择并论证差异量：图像小平移、语言模型 likelihood、两组高维 embeddings 的 two-sample test。必须讨论 ground metric/kernel、support、sample complexity、units 和 downstream test class。

### INFO-DIST-E03

比较 WGAN 的 weight clipping、spectral normalization、gradient penalty 与 exact 1-Lipschitz function ball。设计一份报告规范，防止把实际 critic value 误称为精确 $W_1$，并纳入 empirical OT/MMD baseline。

## 分级提示

- `B01`：JS 使用 mixture $M=(0.625,0.375)$；
- `B03`：RBF-MMD$^2=2-2e^{-\theta^2/(2\sigma^2)}$；
- `C01`：在 $QK$ joint law 下使用 conditional Jensen；
- `C02`：$f^*(u)=e^{u-1}$；
- `D01`：可复用 Bernoulli probabilities $0.1,0.2,0.9$ 并计算三条边；
- `D03`：linear-kernel mean embedding 只保留 first moment。

## 解答入口

完成独立尝试后再打开：[[解答 - f-散度、Bregman 散度与概率度量]]。
