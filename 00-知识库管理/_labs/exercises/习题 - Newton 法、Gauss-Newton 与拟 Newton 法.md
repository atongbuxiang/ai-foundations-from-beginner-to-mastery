---
type: exercise
status: draft
area: [math/optimization, math/second-order-methods, ai/training]
topic: "Newton 法、Gauss-Newton 与拟 Newton 法"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Newton 法、Gauss-Newton 与拟 Newton 法]]"]
related: ["[[优化与凸分析 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - Newton 法、Gauss-Newton 与拟 Newton 法]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - Newton 法、Gauss-Newton 与拟 Newton 法

> [!abstract] 训练目标
> 从“局部模型—曲率对象—线性求解—全局化—外层证书”重建二阶法，而不是背 $H^{-1}g$。

## A. 识别与复述

### OPT-NEWTON-A01

分别从二次 Taylor 模型和线性化驻点方程推导 Newton step。说明两条推导在 indefinite Hessian 时为何有不同的 optimization interpretation。

### OPT-NEWTON-A02

比较 exact Newton、Gauss–Newton、GGN、BFGS、SR1 与 L-BFGS：各自近似什么、是否保证 PSD、需要何种 oracle、memory 与 globalizer。

### OPT-NEWTON-A03

解释 line search、trust region、modified Hessian、damping、inner linear residual 与 outer stationarity residual 的职责。给出一个完整的二阶 iteration contract。

## B. 手算与构造

### OPT-NEWTON-B01

对

$$
f(x_1,x_2)=\frac12(x_1^2+9x_2^2)-2x_1-18x_2
$$

从 $x_0=(0,0)$ 计算 gradient、Hessian、Newton step、Newton decrement 与二次模型预测下降；验证一步到达 minimizer。

### OPT-NEWTON-B02

令 residual

$$
r_1(\theta)=\theta^2-1,
\qquad r_2(\theta)=2\theta-1.
$$

在 $\theta=0$ 计算 gradient、exact Hessian、Gauss–Newton matrix 与两种 step；说明差异来自哪一项。

### OPT-NEWTON-B03

给 $B_0=I$、$s=(1,1)^T$、$y=(2,1)^T$。计算 BFGS Hessian update $B_1$，验证 secant equation、symmetry 与正定性；再说明若换成 $y=(-2,-1)^T$ 会破坏什么。

## C. 推导与证明

### OPT-NEWTON-C01

在 Hessian inverse 有界、Hessian $M$-Lipschitz、full step 且起点足够近的假设下，证明

$$
\|x_{k+1}-x^*\|\le\frac{M}{2m}\|x_k-x^*\|^2.
$$

逐行标注每个假设在哪里使用。

### OPT-NEWTON-C02

对 nonlinear least squares 推导

$$
\nabla f=J^Tr,\qquad
\nabla^2f=J^TJ+\sum_ir_i\nabla^2r_i.
$$

再证明 GN step 等价于最小化 linearized residual；解释 normal equations 为什么平方 condition number。

### OPT-NEWTON-C03

证明若 $B\succ0$ 且 $y^Ts>0$，BFGS update 保持正定。说明 strong Wolfe condition 与 curvature condition 的关系，但不要把 line search 结论外推到 noisy stochastic gradients。

## D. 反例与失败边界

### OPT-NEWTON-D01

构造一个二维 indefinite quadratic，证明 raw Newton direction 不是 descent 或直接跳到 saddle。比较 eigenvalue shift 与 trust-region negative-curvature step。

### OPT-NEWTON-D02

反驳“$J^TJ\succeq0$，所以 Gauss–Newton 总比 exact Newton 准确”。至少覆盖 large residual、rank deficiency、negative curvature、robust/nonconvex output loss 与数值 normal equations。

### OPT-NEWTON-D03

构造 noisy mini-batch gradient 情形，使 $y_k=g_{k+1}-g_k$ 主要反映 batch noise。说明 BFGS/L-BFGS pair filtering、same-batch curvature、damping 或 larger batch 各解决什么、不解决什么。

## E. AI 迁移

### OPT-NEWTON-E01

设计一个 HVP Newton–CG 深网实验：规定 curvature batch、forcing sequence、negative-curvature detection、preconditioner、damping/trust rule、inner/outer residual 和 FLOPs/wall-clock 比较。

### OPT-NEWTON-E02

设计 nonlinear least-squares benchmark，逐步改变 terminal residual、Jacobian rank 与 noise；比较 exact Newton、QR-GN、normal-equation GN、LM 和 L-BFGS，并预注册诊断图。

### OPT-NEWTON-E03

审计一个 $H^{-1}v$ influence/implicit-gradient 管线：说明 damping、CG truncation、HVP batch、indefiniteness、solve residual 与 outer estimate error 怎样形成误差预算。

