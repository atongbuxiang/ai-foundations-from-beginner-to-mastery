---
type: solution
status: draft
area: [math/optimization, math/constrained-optimization, ai/learning]
topic: "Lagrange 乘子与 KKT 条件"
exercise: "[[习题 - Lagrange 乘子与 KKT 条件]]"
related: ["[[Lagrange 乘子与 KKT 条件]]", "[[优化与凸分析 MOC]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - Lagrange 乘子与 KKT 条件

> [!warning] 使用顺序
> 先固定 inequality 方向，再检查 feasibility/active set/CQ；之后才解 multiplier。最后必须区分 necessity、convex sufficiency 与 second-order type。

## A. 识别与复述

### OPT-KKT-A01

对 $g_i\le0,h_j=0$：

$$
\mathcal L=f+\lambda^Tg+\nu^Th,
\quad \lambda\ge0,
\quad\nu\text{ free}.
$$

KKT：

1. primal：$g(x)\le0,h(x)=0$；
2. dual：$\lambda\ge0$；
3. stationarity：$\nabla f+J_g^T\lambda+J_h^T\nu=0$；
4. complementarity：$\lambda_i g_i(x)=0$。

inequality multiplier 非负，因为 outward normal 的 nonnegative conic combination 形成法锥；equality 的两个方向都不可行，normal span 允许任意系数。active set 是 $g_i=0$；positive-multiplier set 是 $\lambda_i>0$，后者包含于前者，但 active 可有 $\lambda_i=0$。

### OPT-KKT-A02

- LICQ：active inequality 与 equality gradients jointly independent；非线性 local CQ，较强，常给 multiplier uniqueness；
- MFCQ：equality gradients independent，且存在保持 equality tangent 并严格减小所有 active inequalities 的方向；弱于 LICQ，支持 multiplier existence/boundedness 和 tangent-linearization bridge；
- Slater：convex problem 中有 relative-interior strictly feasible point；是 global convex CQ，常给 strong duality、dual attainment/KKT existence。

三者不是一条简单可互换的强弱链：Slater 借助 convexity，是全局可行性条件；LICQ/MFCQ 是点上的 differential conditions。在线性/凸特例它们有联系，但应用定理时必须按 theorem 使用。

### OPT-KKT-A03

- necessity：local optimum + differentiability + CQ $\Rightarrow$ 存在 KKT multipliers；
- convex sufficiency：convex $f,g_i$ + affine equalities + KKT $\Rightarrow$ global optimum；
- multiplier existence：需 CQ/duality regularity，不能从 primal optimum 无条件推出；
- strong duality：convexity + Slater 等 regularity 常给 zero gap；详细方向见下一章；
- second-order sufficiency：KKT + CQ + Lagrangian Hessian 对 nonzero critical directions 正定 $\Rightarrow$ strict local minimum。

这些是五个不同逻辑箭头。“convex KKT sufficiency”不等于“每个 convex optimum 都自动有 multiplier”；后者还需 existence 条件。

## B. 手算与构造

### OPT-KKT-B01

写 constraints

$$
g_1=x+y-2\le0,\quad g_2=-x\le0,\quad g_3=-y\le0.
$$

unconstrained center $(2,1)$ 违反第一项；到 halfspace boundary 的 Euclidean projection 是

$$
(x^*,y^*)=(2,1)-\frac{3-2}{2}(1,1)=(3/2,1/2).
$$

两坐标正，故 $g_2,g_3$ inactive，$\lambda_2=\lambda_3=0$。objective gradient：

$$
\nabla f=(-1,-1).
$$

stationarity

$$
(-1,-1)+\lambda_1(1,1)=0
$$

给 $\lambda_1=1$。primal/dual 可行；$\lambda_1g_1=0$，其余 multipliers 为零。几何上负 objective gradient $(1,1)$ 正是 active face outward normal，边界阻止继续向 center 走。

### OPT-KKT-B02

令 $H=\operatorname{diag}(2,4),q=(2,8)^T,A=(1,1),b=2$：

$$
\begin{bmatrix}
2&0&1\\
0&4&1\\
1&1&0
\end{bmatrix}
\begin{bmatrix}x_1\\x_2\\\nu\end{bmatrix}
=\begin{bmatrix}2\\8\\2\end{bmatrix}.
$$

前两行：

$$
x_1=1-\nu/2,\qquad x_2=2-\nu/4.
$$

constraint 给 $3-3\nu/4=2$，所以

$$
\nu^*=4/3,\qquad x^*=(1/3,5/3).
$$

primal residual $x_1+x_2-2=0$；dual/stationarity residual

$$
Hx-q+A^T\nu=(0,0)^T.
$$

KKT matrix symmetric indefinite；$H$ SPD 不使整个 block matrix SPD。

### OPT-KKT-B03

可定义 scaled measures：

$$
e_p=\max\left\{
\max_i\frac{[g_i(x)]_+}{1+s_{g_i}},
\max_j\frac{|h_j(x)|}{1+s_{h_j}}
\right\},
$$

$$
e_d=\frac{\|[-\lambda]_+\|}{1+\|\lambda\|},
$$

$$
e_s=\frac{\|\nabla f+J_g^T\lambda+J_h^T\nu\|}
{1+\|\nabla f\|+\|J_g^T\lambda\|+\|J_h^T\nu\|},
$$

$$
e_c=\max_i\frac{|\lambda_i g_i(x)|}
{1+|\lambda_i|s_{g_i}}.
$$

$s_g,s_h$ 取物理/tolerance scale 而非随意常数。若约束换为 $\tilde g=1000g$，同一 stationarity 的 multiplier 变为 $\tilde\lambda=\lambda/1000$；raw feasibility $[\tilde g]_+$ 放大 $1000$，但 normalized residual 若 $s_{\tilde g}=1000s_g$ 保持可比；product $\tilde\lambda\tilde g=\lambda g$ 不变。必须存原单位与缩放 map。

## C. 推导与证明

### OPT-KKT-C01

equality case：feasible tangent 是 $\ker J_h$（此等号需 regularity）。local optimum 给 $\nabla f\perp\ker J_h$，所以

$$
\nabla f\in(\ker J_h)^\perp=\operatorname{range}(J_h^T),
$$

即存在 $\nu$ 使 $\nabla f+J_h^T\nu=0$。

inequality case：在 CQ 下真实 tangent cone 等于/可由 linearized active constraints 表示。其 polar 由 active inequality normals 的 nonnegative cone 与 equality-normal span 构成。因此

$$
-\nabla f=J_g^T\lambda+J_h^T\nu,\quad\lambda\ge0,
$$

且 inactive $\lambda=0$，得到 stationarity 与 complementarity。CQ 正用在“真实 tangent 的 polar = linearized normals generated cone”这一步；没有它，linearized cone 可能太大，normal representation 失败。

### OPT-KKT-C02

对任意 feasible $x$，convexity：

$$
f(x)-f(x^*)\ge\nabla f(x^*)^T(x-x^*).
$$

stationarity 代入：

$$
=-\sum_i\lambda_i^*\nabla g_i(x^*)^T(x-x^*)
-\sum_j\nu_j^*\nabla h_j(x^*)^T(x-x^*).
$$

affine equalities 对两个 feasible points 的 difference 为零。convexity of $g_i$ 给

$$
\nabla g_i(x^*)^T(x-x^*)\le g_i(x)-g_i(x^*).
$$

故

$$
f(x)-f(x^*)
\ge-\sum_i\lambda_i^*[g_i(x)-g_i(x^*)]
=-\sum_i\lambda_i^*g_i(x)+\sum_i\lambda_i^*g_i(x^*)\ge0.
$$

最后用 feasible $g_i(x)\le0$、dual feasible 与 complementarity。证明从“已有 KKT triple”出发，所以不需要 Slater；Slater 用于保证 optimum 附近存在这样的 multipliers/zero duality gap。

### OPT-KKT-C03

critical cone 保留 tangent 中 first-order objective change 为零的方向。代表性 KKT 表达：equalities $\nabla h^Td=0$；positive-multiplier active inequalities 取 equality；zero-multiplier active inequalities允许 $\le0$。

二阶必要：对 $d\in\mathcal C$，

$$
d^T\nabla_{xx}^2\mathcal Ld\ge0.
$$

若对所有 nonzero critical directions 严格正，加相应 CQ/regularity，得到 quadratic growth/strict local minimum。

例：

$$
f(x,y)=x^2-y^2,\qquad h(x,y)=y=0.
$$

在原点 stationarity，tangent directions 是 $(d_x,0)$。full Hessian $\operatorname{diag}(2,-2)$ indefinite，但 reduced quadratic form

$$
(d_x,0)H(d_x,0)^T=2d_x^2>0
$$

对 nonzero feasible directions 为正，所以原点在约束集上是 strict minimum。full-space negative $y$ direction 不可行。

## D. 反例与失败边界

### OPT-KKT-D01

feasible condition $x^2\le0$ 只允许 $x=0$，故它是 global minimum。active gradient $g'(0)=0$，stationarity 要求

$$
1+\lambda\cdot0=0,
$$

无解。LICQ 失败（active gradient 为零）；MFCQ 要某 $d$ 使 $0\cdot d<0$，不可能；Slater 要 $x^2<0$，也不可能。linearized cone 是全实线，真实 tangent 只有 $0$，正是 CQ gap。

### OPT-KKT-D02

- local maximum：unconstrained $f(x)=-x^2$，$x=0$ 满足 KKT/stationarity，但 Hessian $-2<0$；
- saddle：unconstrained $f(x,y)=x^2-y^2$，原点满足 stationarity，Hessian 有正负 eigenvalues。

在无约束情形 critical cone 是全空间。second-order necessary 要 Hessian PSD：maximum 和 saddle 均失败；strict positive definite 是 local minimum 的充分条件。约束情形需看 Lagrangian Hessian 在 critical cone，不能看全空间。

### OPT-KKT-D03

问题

$$
\min_x(x-1)^2\quad\text{s.t. }h_1(x)=x=0, h_2(x)=2x=0
$$

的 optimizer 唯一 $x=0$。stationarity：

$$
-2+\nu_1+2\nu_2=0,
$$

有无穷多 multipliers；LICQ 失败。若只保留 $\epsilon x=0$，multiplier 为 $2/\epsilon$，可任意大而 primal geometry 未变。

因此 shadow price 对 redundant representation 不唯一；implicit differentiation 的 KKT Jacobian singular；raw dual residual/multiplier norm 可能误导 stopping。需去冗余、rank-revealing factorization、constraint normalization，或解释选取的 minimum-norm multiplier。

## E. AI 迁移

### OPT-KKT-E01

constraints：

$$
1-\xi_i-y_i(w^Tx_i+b)\le0,\qquad-\xi_i\le0.
$$

Lagrangian 对 $w,b,\xi_i$ stationarity 给

$$
w=\sum_i\alpha_i y_ix_i,
\quad\sum_i\alpha_i y_i=0,
\quad C-\alpha_i-\mu_i=0.
$$

因 $\alpha_i,\mu_i\ge0$，$0\le\alpha_i\le C$。complementarity：

$$
\alpha_i[1-\xi_i-y_if_i]=0,
\qquad\mu_i\xi_i=0.
$$

- $\alpha_i=0$：通常严格在 margin 外，非 support（退化时可恰在 margin）；
- $0<\alpha_i<C$：$\mu_i>0\Rightarrow\xi_i=0$，且 first constraint active，故 $y_if_i=1$；
- $\alpha_i=C$：$\mu_i=0$，通常在 margin 内/有 slack，可能 misclassified；退化时也可在 margin。

只有明确 complementarity 才能正确处理边界例外。

### OPT-KKT-E02

最小化 negative entropy

$$
\sum_xp_x\log(p_x/r_x)
$$

满足 $\sum p=1,\sum pT=\tau,p\ge0$。若 $p_x>0$，nonnegativity multiplier 为零。stationarity：

$$
1+\log(p_x/r_x)+\nu+\eta^TT(x)=0,
$$

所以

$$
p_x=r_x\exp[-1-\nu-\eta^TT(x)]
=\frac{r_xe^{-\eta^TT(x)}}{Z(\eta)}.
$$

若 $\tau$ 在 moment polytope boundary，某些 $p_x=0$，finite $\eta$ 可能不存在，必须保留 nonnegativity normal cone/limit；reference $r$ 决定坐标/base measure；strict positive feasible distribution 是相应 Slater 类型条件。只写 interior derivative 会漏掉 boundary solutions。

### OPT-KKT-E03

协议分四层：

1. 建模：写 $g_i(\theta)$ 的方向、单位、estimator、confidence interval 与可行性 baseline；
2. 训练：记录 primal feasibility、$[-\lambda]_+$、stationarity 与 complementarity，constraint normalization、multiplier optimizer/clip、penalty/dual schedule；
3. 验收：在独立 held-out/deployment-like sample 上报告 constraint point estimate+uncertainty，检测 infeasible trade-off，并做 tolerance/multiplier sensitivity；
4. 理论边界：deep network nonconvex，small KKT residual 只表示 approximate local stationarity；noisy estimates 使 residual 本身随机；还需 second-order/escape checks、multiple seeds/initializations 与 utility/generalization gap。

若 empirical constraint 可行但 held-out violation，不能靠继续降低 numerical KKT residual 修复 statistical gap；应增加数据、robust constraint 或重设 estimand。

