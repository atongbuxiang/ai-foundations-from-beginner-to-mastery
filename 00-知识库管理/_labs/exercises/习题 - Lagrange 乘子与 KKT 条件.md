---
type: exercise
status: draft
area: [math/optimization, math/constrained-optimization, ai/learning]
topic: "Lagrange 乘子与 KKT 条件"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Lagrange 乘子与 KKT 条件]]"]
related: ["[[优化与凸分析 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - Lagrange 乘子与 KKT 条件]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - Lagrange 乘子与 KKT 条件

> [!abstract] 训练目标
> 能从约束几何推到 KKT，检查 CQ/二阶条件，求解 KKT system，并把证书迁移到 SVM、最大熵与 noisy AI constraints。

## A. 识别与复述

### OPT-KKT-A01

对 $g_i(x)\le0,h_j(x)=0$ convention 写出 Lagrangian 与四组 KKT。解释 inequality/equality multiplier 的符号、active 与 positive-multiplier set 的区别。

### OPT-KKT-A02

比较 LICQ、MFCQ 与 Slater condition：定义、适用范围、相对强弱/角色，以及它们分别帮助证明什么。

### OPT-KKT-A03

区分：(a) KKT necessity；(b) convex KKT sufficiency；(c) multiplier existence；(d) strong duality；(e) second-order sufficiency。每一项写出不能省略的代表性条件。

## B. 手算与构造

### OPT-KKT-B01

求解

$$
\min_{x,y}(x-2)^2+(y-1)^2
\quad\text{s.t. }x+y\le2, x\ge0, y\ge0.
$$

写出全部 multipliers、active set、KKT 四组条件，并解释 geometry。

### OPT-KKT-B02

对 equality-constrained quadratic

$$
\min_x\frac12x^T\begin{bmatrix}2&0\\0&4\end{bmatrix}x-
\begin{bmatrix}2\\8\end{bmatrix}^Tx
\quad\text{s.t. }[1\ \ 1]x=2,
$$

写 KKT system，求 $x^*,\nu^*$，并计算 primal/dual residual。

### OPT-KKT-B03

给 approximate point $x$、multipliers $\lambda,\nu$ 的通用 smooth problem，设计 scale-aware 的四类 KKT residual。再说明 constraint 乘 $1000$ 后 raw multiplier/residual 怎样变化、怎样归一化。

## C. 推导与证明

### OPT-KKT-C01

从 equality tangent null space 推导 multiplier stationarity；再用 active normal cone 推出 inequality multipliers。明确指出需要 CQ 的步骤。

### OPT-KKT-C02

完整证明 convex differentiable $f,g_i$ 与 affine $h_j$ 下，任一 KKT point 都是 global minimum。解释 Slater 在这一充分性证明中为何不出现。

### OPT-KKT-C03

定义 critical cone，推导/解释 Lagrangian Hessian 上的二阶必要与充分条件。用一个 equality-constrained example 展示 full-space Hessian indefinite 但 reduced Hessian positive 的情形。

## D. 反例与失败边界

### OPT-KKT-D01

分析

$$
\min_x x\quad\text{s.t. }x^2\le0.
$$

证明 $x^*=0$ 是 global minimum 但不存在 KKT multiplier；指出 LICQ/MFCQ/Slater 哪些失败。

### OPT-KKT-D02

给出满足 KKT 但分别是 local maximum、saddle 的 nonconvex examples；再说明二阶条件如何区分。

### OPT-KKT-D03

构造 redundant/poorly scaled constraints，使 primal optimizer 唯一但 multipliers 不唯一或很大。解释这对 shadow price、implicit differentiation 与 solver stopping 的影响。

## E. AI 迁移

### OPT-KKT-E01

从 soft-margin SVM primal 推导 $w=\sum_i\alpha_i y_ix_i$、$0\le\alpha_i\le C$ 与 support-vector complementarity；分类 $\alpha_i=0,0<\alpha_i<C,\alpha_i=C$。

### OPT-KKT-E02

从 finite-support maximum entropy 的 normalization、moment 与 nonnegativity constraints 推导 exponential form；讨论 boundary moment、zero probabilities、reference measure 和 CQ。

### OPT-KKT-E03

为 fairness/resource-constrained neural training 设计 primal-dual 验收：经验/held-out constraints、estimation uncertainty、KKT residual、multiplier scaling、feasibility failure、二阶/非凸边界与部署 gap。

