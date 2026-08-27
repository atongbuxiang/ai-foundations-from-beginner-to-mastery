---
type: solution
status: draft
area: [math/convex-analysis, math/inequalities, ai/loss-functions]
topic: "凸函数、Jensen 不等式与上图集"
exercise: "[[习题 - 凸函数、Jensen 不等式与上图集]]"
related: ["[[凸函数、Jensen 不等式与上图集]]", "[[优化与凸分析 MOC]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 凸函数、Jensen 不等式与上图集

> [!warning] 使用顺序
> 对照时不要只看“凸/非凸”标签。每一题都应写 domain、变量、使用的判据和关键不等式；一个 Hessian 点的负方向足以否定凸性，但有限个 PSD samples 不足以证明全局凸性。

## A. 识别与复述

### OPT-FUNC-A01

$f$ convex 要求 $\operatorname{dom}f$ convex，且

$$
f(\theta x+(1-\theta)y)
\le\theta f(x)+(1-\theta)f(y)
$$

对任意 domain 内 $x,y$、$\theta\in[0,1]$。strict convexity 对 $x\ne y,\theta\in(0,1)$ 用严格不等号。

differentiable $f$ 的 $\mu$-strong convexity 可写

$$
f(y)\ge f(x)+\nabla f(x)^T(y-x)
+\frac\mu2\|y-x\|^2,
\quad\mu>0.
$$

concave iff $-f$ convex。

domain 使 convex combinations 与函数值都有定义；extended-value function 还用 $+\infty$ 表示禁区。strong convexity 推 strict convexity并给 uniform quadratic growth；strict convexity 只给 chord strictness/至多一个 minimizer，不必存在统一 $\mu$。

### OPT-FUNC-A02

$$
\operatorname{epi}f=\{(x,t):t\ge f(x)\},
$$

$$
C_\alpha=\{x:f(x)\le\alpha\}.
$$

$f$ convex iff epigraph convex；$f$ convex implies every sublevel set convex。所有 sublevel sets convex 定义 quasiconvex，反向到 convex false，例如 $x^3$。

即使 $f$ convex，level set $\{x:f(x)=0\}$ 也不必 convex：$f(x)=\|x\|_2-1$ 本身不 convex due subtraction? 更直接取 convex $f(x)=\|x\|_2$，level $f=1$ 是 sphere。standard convex program 因此要求 equality functions affine，而不是任意 convex。

### OPT-FUNC-A03

- line：$f$ convex iff $t\mapsto f(x+tv)$ 对所有合法 line restrictions convex；domain convex即可；
- first order：在 open convex domain、$f$ differentiable 时，

$$
f(y)\ge f(x)+\nabla f(x)^T(y-x);
$$

- second order：在 open convex domain、$f$ twice differentiable 时，

$$
\nabla^2f(x)\succeq0
$$

对全部 $x$。

random directions/points 只能发现某些违反；未发现 negative curvature 不覆盖 uncountably many points/directions，也受 finite precision 与 autodiff 实现影响，所以是 diagnostic。

## B. 手算与构造

### OPT-FUNC-B01

1. $e^x$，domain $\mathbb R$，$f''=e^x>0$，strictly convex。
2. $-\log x$，domain $(0,\infty)$，$f''=1/x^2>0$，strictly convex。
3. $x^4$，domain $\mathbb R$，$f''=12x^2\ge0$，convex；且 strictly convex，尽管 $f''(0)=0$。
4. quadratic 的 Hessian 是 symmetric part：

$$
\nabla^2f=\frac{Q+Q^T}{2}.
$$

若先约定 $Q=Q^T$，iff $Q\succeq0$ convex。
5. $\|Ax-b\|_2$ 是 norm 与 affine map 的 composition，convex，domain $\mathbb R^n$。
6. 非凸。令

$$
g(x)=\min\{(x-1)^2,(x+1)^2\}.
$$

$g(-1)=g(1)=0$，但 $g(0)=1$，违反

$$
g(0)\le\frac12g(-1)+\frac12g(1)=0.
$$

pointwise minimum 不保 convexity。

### OPT-FUNC-B02

$E[X]=0$。

对 $f(x)=x^2$：

$$
f(E[X])=0,
\qquad
E[f(X)]=1,
$$

Jensen gap 为 1，恰等于 variance。

对 $f(x)=e^x$：

$$
f(E[X])=1,
$$

$$
E[f(X)]
=\frac{e+e^{-1}}2
=\cosh1
\approx1.543081,
$$

gap 约 $0.543081$。

非严格 equality 例：$X$ 以等概率取 1、2，$f(x)=|x|$。因 support 完全落在 $f(x)=x$ affine region：

$$
f(E[X])=1.5=E[f(X)].
$$

局部 relation

$$
E[f(X)]-f(E[X])
\approx\frac12f''(E[X])\operatorname{Var}(X)
$$

来自 Taylor 且需 concentration/smoothness；若 curvature 在 support 上有上下界才可变成 rigorous inequalities。

### OPT-FUNC-B03

对 $x=(0,0)$：

$$
\operatorname{LSE}(x)=\log(e^0+e^0)=\log2.
$$

softmax

$$
p=(1/2,1/2).
$$

Hessian

$$
H=\operatorname{diag}(p)-pp^T
=\frac14
\begin{pmatrix}
1&-1\\-1&1
\end{pmatrix}.
$$

normalized eigenvectors/eigenvalues：

$$
\frac1{\sqrt2}(1,1),\quad\lambda=0,
$$

$$
\frac1{\sqrt2}(1,-1),\quad\lambda=\frac12.
$$

target class 1（one-hot $(1,0)$）的 CE：

$$
\ell=\operatorname{LSE}(x)-x_1=\log2,
$$

$$
\nabla_x\ell=p-e_1=(-1/2,1/2).
$$

constant shift $x\mapsto x+c\mathbf1$ 使

$$
\operatorname{LSE}(x+c\mathbf1)=c+\operatorname{LSE}(x),
$$

沿该方向 affine，Hessian annihilates $\mathbf1$，所以 full space 不 strictly convex。

## C. 推导与证明

### OPT-FUNC-C01

若 $f$ convex，取 $(x,s),(y,t)\in\operatorname{epi}f$。则

$$
\begin{aligned}
f(\theta x+(1-\theta)y)
&\le\theta f(x)+(1-\theta)f(y)\\
&\le\theta s+(1-\theta)t,
\end{aligned}
$$

所以 epigraph convex。

反向，$(x,f(x)),(y,f(y))$ 都在 epigraph。其 convex combination 在 epigraph，故

$$
f(\theta x+(1-\theta)y)
\le\theta f(x)+(1-\theta)f(y).
$$

sublevel：若 $f(x),f(y)\le\alpha$，则

$$
f(\theta x+(1-\theta)y)\le\alpha.
$$

反向不成立，因为 sublevel geometry 只保 order nesting，不约束 function values 沿 chord 的线性插值；$x^3$ 是显式反例。

### OPT-FUNC-C02

**convex $\Rightarrow$ first order。** 令

$$
g(t)=f(x+t(y-x)).
$$

对 $t\in(0,1]$：

$$
g(t)\le(1-t)g(0)+tg(1).
$$

所以

$$
g(1)\ge g(0)+\frac{g(t)-g(0)}t.
$$

令 $t\downarrow0$，右侧 quotient 趋于 $g'(0)=\nabla f(x)^T(y-x)$。

**first order $\Rightarrow$ convex。** 令 $z=\theta x+(1-\theta)y$。有

$$
f(x)\ge f(z)+\nabla f(z)^T(x-z),
$$

$$
f(y)\ge f(z)+\nabla f(z)^T(y-z).
$$

分别乘 $\theta,1-\theta$ 相加，因

$$
\theta(x-z)+(1-\theta)(y-z)=0,
$$

得到 chord inequality。

若 $\nabla f(x^*)=0$：

$$
f(y)\ge f(x^*)
$$

对所有 $y$，所以 global optimal。

convex feasible set 上，若 local minimizer $x^*$ 不是 global，存在 feasible $y$ 使 $f(y)<f(x^*)$。任意足够小 $t>0$ 的

$$
x_t=(1-t)x^*+ty
$$

既 feasible 又任意靠近 $x^*$，且

$$
f(x_t)\le(1-t)f(x^*)+tf(y)<f(x^*),
$$

矛盾。

### OPT-FUNC-C03

1. **nonnegative sum：** 对每个 $f_i$ 用 chord inequality，乘 $a_i\ge0$ 不翻向，再相加。
2. **affine precomposition：**

$$
A(\theta x+(1-\theta)y)+b
=\theta(Ax+b)+(1-\theta)(Ay+b).
$$

对 $f$ 使用 convexity。
3. **pointwise supremum：**

$$
\operatorname{epi}\sup_i f_i
=\bigcap_i\operatorname{epi}f_i,
$$

intersection convex。
4. **composition：** 若 $h$ convex nondecreasing、$g$ convex：

$$
h(g(\theta x+(1-\theta)y))
\le h(\theta g(x)+(1-\theta)g(y))
\le\theta h(g(x))+(1-\theta)h(g(y)).
$$

perspective $G(x,t)=t f(x/t)$，$t>0$。取 $(x_i,t_i)$、$\lambda\in[0,1]$，令

$$
t=\lambda t_1+(1-\lambda)t_2,
$$

并定义重新归一化权重

$$
\alpha=\frac{\lambda t_1}{t},
\qquad
1-\alpha=\frac{(1-\lambda)t_2}{t}.
$$

则

$$
\frac{\lambda x_1+(1-\lambda)x_2}{t}
=\alpha\frac{x_1}{t_1}
+(1-\alpha)\frac{x_2}{t_2}.
$$

对 $f$ 用 convexity，再乘 $t$，得到 $G$ 的 chord inequality。

## D. 反例与失败边界

### OPT-FUNC-D01

$f(x)=x^3$ 单调递增，所以

$$
\{x:x^3\le\alpha\}
=(-\infty,\alpha^{1/3}]
$$

对每个 $\alpha$ 都 convex。但

$$
f''(x)=6x
$$

在 $x<0$ 为负，所以 $f$ 非 convex。

$g(x)=x^4$ strictly convex：$g'(x)=4x^3$ strictly increasing，或用定义检查。可是

$$
g''(x)=12x^2,
$$

在 0 为 0，不存在 global $\mu>0$ 使 $g''\ge\mu$，故不 globally strongly convex。

### OPT-FUNC-D02

1. composition：$h(u)=u^2$、$g(x)=x^2-1$ 都 convex，但

$$
(h\circ g)(x)=(x^2-1)^2,
$$

$$
(h\circ g)''(x)=12x^2-4,
$$

在 0 为 $-4$。
2. pointwise minimum：

$$
m(x)=\min\{(x-1)^2,(x+1)^2\},
$$

$m(\pm1)=0,m(0)=1$，违反 midpoint convexity。
3. nonlinear reparameterization：原 $f(z)=z^2$ convex，令 $z=u^2-1$：

$$
F(u)=(u^2-1)^2,
$$

同样 $F''(0)=-4$。

三个反例分别显示 monotonicity、pointwise operation 与 coordinate map 条件不能省略。

### OPT-FUNC-D03

对 positive binary label 的 logistic loss

$$
\ell(z)=\log(1+e^{-z})
$$

有

$$
\ell''(z)=\sigma(z)\sigma(-z)>0,
$$

所以对 logit $z$ convex。若 feature $h$ fixed、$z=wh$ affine in $w$，则对最后一层 $w$ convex。

两层标量 network 令

$$
z=w_1w_2,
\qquad
g(w_1,w_2)=\ell(w_1w_2).
$$

在 $(0,0)$，chain rule 给 Hessian

$$
\nabla^2g(0,0)
=\begin{pmatrix}
0&\ell'(0)\\
\ell'(0)&0
\end{pmatrix}
=\begin{pmatrix}
0&-1/2\\
-1/2&0
\end{pmatrix}.
$$

eigenvalues 为 $1/2,-1/2$，所以 parameter objective nonconvex。偷换发生在把 affine logit variable $z$ 换成 bilinear factor parameters。

## E. AI 迁移

### OPT-FUNC-E01

四种平均：

- parameter：$\bar\theta=S^{-1}\sum_s\theta_s$；
- logits：$\bar z(x)=S^{-1}\sum_sz_s(x)$；
- probabilities：$\bar p(x)=S^{-1}\sum_sp_s(x)$；
- losses：$S^{-1}\sum_s\ell(z_s,y)$。

若 loss $\ell(z,y)$ 对 logits convex，Jensen 给

$$
\ell(\bar z,y)
\le\frac1S\sum_s\ell(z_s,y).
$$

但 parameter average 只有在 $z_\theta$ 对 $\theta$ affine 时等于 logit average；深网一般不成立。probability averaging对应 mixture predictive distribution，log-loss 因 $-\log$ convex 有自己的 inequality，不能与 logit average混同。

protocol：同一 held-out samples 上比较四种输出，报告 NLL、Brier、ECE、accuracy、entropy 与 subgroup/shift；对 parameter average 检查 permutation/alignment、function distance；用 paired bootstrap 和 multiple seeds。Jensen 是 pointwise objective inequality，不保证 accuracy、calibration 或 shifted risk。

### OPT-FUNC-E02

令

$$
L_\tau(x)=\tau\log\sum_i e^{x_i/\tau}.
$$

预注册检查：

1. 对 random/structured logits 验证

$$
0\le L_\tau(x)-\max_i x_i\le\tau\log n;
$$

2. 记录 softmax entropy、top weight 和 gradient norm 随 $\tau$；
3. Hessian

$$
H_\tau=\frac1\tau(\operatorname{diag}p-pp^T)
$$

的 zero shift eigenvalue 与最大 eigenvalue；
4. naive `exp(x/tau)` 与 shifted stable implementation 的 overflow/relative error；
5. fp64/fp32/bf16、极端 logits 和 tie cases；
6. finite-difference/HVP cross-check。

$\tau\downarrow0$ 改善 max approximation，但 gradient 更集中、Hessian scale $1/\tau$ 增大并可能出现 underflow。只能称 smooth approximation，有限 $\tau$ 不是 exact max。

### OPT-FUNC-E03

一个例子：

$$
\min_w
\sum_{i=1}^n
\log(1+e^{-y_i(a_i^Tw+b_i)})
+\lambda\|w\|_1
+\gamma\max_{g\in\mathcal G}(c_g^Tw+d_g)
$$

subject to

$$
Aw=q,
\qquad Bw\le r.
$$

DCP audit：

- affine score $a_i^Tw+b_i$；
- $u\mapsto\log(1+e^{-u})$ convex，affine precomposition；
- $\ell_1$ norm convex，$\lambda\ge0$；
- finite maximum of affine functions convex，$\gamma\ge0$；
- equality affine，inequality affine；
- shared domain all $\mathbb R^d$。

可用 epigraph variable $t$ 把 group max 写为 $c_g^Tw+d_g\le t$。

solver acceptance 后仍检查：original-scale primal feasibility、objective recomputation、dual feasibility/gap、KKT residual、solver tolerance、conditioning/scaling、sparsity pattern sensitivity、data split/generalization、class/subgroup calibration 和 shift。DCP certificate 证明 formulation convex，不证明 feasible、attained、well-conditioned 或 population-optimal。

## 完成标准

你应能从 chord 独立推出 epigraph、first-order 与 Jensen；能手算 LSE Hessian 的 zero direction；并在任何“这个 loss 是凸的”声明后立即追问：相对于哪个变量、在哪个 domain、经过什么 composition？

