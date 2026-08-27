---
type: exercise
status: draft
area: [learning-theory/local-complexity, statistical-rates]
topic: "[[局部 Rademacher 复杂度与快收敛率]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Rademacher 复杂度与经验复杂度]]", "[[覆盖数、Metric Entropy 与 Chaining 入口]]"]
related: ["[[解答 - 局部 Rademacher 复杂度与快收敛率]]", "[[正则化 ERM 的稳定性]]"]
solution: "[[解答 - 局部 Rademacher 复杂度与快收敛率]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 局部 Rademacher 复杂度与快收敛率

> [!abstract] 训练目标
> 能从 excess-loss class 定义局部切片，使用 sub-root fixed point闭合误差尺度，识别 Bernstein/curvature 与 peeling 的必要性，并审计 interpolation、fine-tuning 和 kernel claims。

## A. 识别与复述

### LT-LOC-A01

定义 excess loss $g_f$、excess-loss class、二阶矩 local slice 与 star hull。

### LT-LOC-A02

定义 sub-root function，并陈述 positive fixed point 对 $r\ge r^*$ 的支配性质。

### LT-LOC-A03

区分 global complexity、population local complexity 与 empirical local complexity。

## B. 手算与数值判断

### LT-LOC-B01

取 $\psi(r)=0.2\sqrt r+0.01$。求 positive fixed point $r^*$。

### LT-LOC-B02

若 $\psi(r)=2\sqrt{rd/m}+3d/m$、$d=20,m=2000$，用二次方程计算 fixed point。

### LT-LOC-B03

比较 $d=100,m=10^4$ 时 global rate $\sqrt{d/m}$ 与 local fixed-point rate $d/m$；给出数值与倍数。

## C. 推导与证明

### LT-LOC-C01

证明 sub-root $\psi$ 在 $r\ge r^*$ 时满足 $\psi(r)\le\sqrt{rr^*}\le r$。

### LT-LOC-C02

由 $\psi(r)=a\sqrt r+b$ 推导 fixed point closed form，并说明 $a^2,b\asymp d/m$ 时 $r^*\asymp d/m$。

### LT-LOC-C03

设计 dyadic peeling shells 与 summable failure probabilities，说明它如何解除“未知 estimator radius”的 circularity。

## D. 边界、反例与纠错

### LT-LOC-D01

构造逐点 excess loss 可为负但 population excess risk 非负的两点分布例子。

### LT-LOC-D02

说明 strong convex regularized training objective 为什么不自动推出 task population excess risk 的 Bernstein condition。

### LT-LOC-D03

反驳“训练 loss 为 0，所以 estimator 位于一个简单 local class”；给出插值类仍可非常复杂的构造思路。

## E. AI 迁移

### LT-LOC-E01

为 kernel ridge 写 local analysis 审计项：Gram spectrum、regularization、noise/tail、effective dimension、fixed point 与 hyperparameter selection。

### LT-LOC-E02

分析“fine-tuning parameter displacement 很小，所以泛化好”的缺口；列出从 parameter ball 到 local function/loss class 所需条件。

### LT-LOC-E03

区分二维 loss-landscape flatness、Hessian sharpness 与 local Rademacher complexity；说明三者可能相关但不等价。
