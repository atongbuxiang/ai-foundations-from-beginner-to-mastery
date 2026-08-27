---
type: exercise
status: draft
area: [learning-theory/algorithmic-stability, regularization, convex-optimization]
topic: "[[正则化 ERM 的稳定性]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[算法稳定性与替换一个样本]]", "[[光滑性、强凸性与条件数]]"]
related: ["[[解答 - 正则化 ERM 的稳定性]]", "[[随机梯度算法的稳定性接口]]"]
solution: "[[解答 - 正则化 ERM 的稳定性]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 正则化 ERM 的稳定性

> [!abstract] 训练目标
> 能独立完成 strong-convexity cancellation proof，按目标函数归一化追踪常数，并把 approximate optimization、一般 norm 与实际 AI regularization 纳入完整账本。

## A. 识别与复述

### LT-RERM-A01

陈述本章 regularized ERM stability theorem 的全部假设、parameter displacement 与 loss-stability 结论。

### LT-RERM-A02

解释 strong convexity、smoothness 与 Lipschitzness 的差别；指出主证明具体用了哪两个。

### LT-RERM-A03

为什么只写 $F_S(w_{S'})-F_S(w_S)\ge0$ 不足以得到 $1/(\lambda m)$？strong-convexity 下界增加了什么信息？

## B. 手算与数值判断

### LT-RERM-B01

$L=3,\lambda=0.2,m=500$。计算 parameter displacement 与 loss-stability 上界。

### LT-RERM-B02

logistic regression 满足 $\|x\|\le5$，$m=2000$。若希望 $\beta_m\le0.01$，本章 bound 要求 $\lambda$ 至少多大？

### LT-RERM-B03

$L=2,\lambda=0.5,m=1000,\varepsilon_{\rm opt}=10^{-8}$。计算 exact stability term、approximate-optimization term 与总上界。

## C. 推导与证明

### LT-RERM-C01

逐项展开两个 strong-convexity inequalities 之和，证明 $m-1$ 个共享 loss 项与 regularizer 抵消，并推出 $\|w_S-w_{S'}\|\le2L/(\lambda m)$。

### LT-RERM-C02

把证明推广到 norm $\|\cdot\|$、dual norm $\|\cdot\|_*$ 与 $\lambda$-strongly convex regularizer $\Omega$。

### LT-RERM-C03

若 $F_S(\widetilde w_S)-F_S(w_S)\le\varepsilon_S$、$F_{S'}(\widetilde w_{S'})-F_{S'}(w_{S'})\le\varepsilon_{S'}$，推导不假设两边误差相同的 approximate stability bound。

## D. 边界、反例与纠错

### LT-RERM-D01

证明 squared loss 在无界 parameter domain 上不是 global Lipschitz；给出一种使它在受限域上 Lipschitz 的显式常数。

### LT-RERM-D02

反驳：“非凸 neural network loss 加 $\lambda\|w\|^2/2$ 后一定是 $\lambda$-strongly convex。”用 Hessian 说明错误。

### LT-RERM-D03

解释为何增大 $\lambda$ 可令 stability bound 任意小，却不能令 learning risk 任意小；给出一个退化极限。

## E. AI 迁移

### LT-RERM-E01

对 RKHS objective 写出由 $k(x,x)\le\kappa^2$ 与 scalar loss 的 $\sigma$-Lipschitzness 得到的 stability bound，并标明使用的 norm。

### LT-RERM-E02

审计一个使用 weight decay、BatchNorm 与早停的深网：逐条列出为什么不能直接套本章 exact RERM theorem。

### LT-RERM-E03

设计一个 $\lambda$ 扫描报告：除 validation risk 外，至少报告哪些量，才能同时审计 fit、stability、bias 与 optimization？

