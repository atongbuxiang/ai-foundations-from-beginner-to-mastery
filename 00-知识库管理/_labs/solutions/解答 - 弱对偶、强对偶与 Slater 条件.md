---
type: solution
status: draft
area: [math/optimization, math/duality, ai/certification]
topic: "弱对偶、强对偶与 Slater 条件"
exercise: "[[习题 - 弱对偶、强对偶与 Slater 条件]]"
related: ["[[弱对偶、强对偶与 Slater 条件]]", "[[优化与凸分析 MOC]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 弱对偶、强对偶与 Slater 条件

> [!warning] 使用顺序
> 先固定 constraint sign 与 domain，再对全部 domain 取 infimum。任何 gap certificate 都先检查 primal/dual feasibility；value equality 与 optimizer existence 分开验收。

## A. 识别与复述

### OPT-DUAL-A01

对

$$
p^*=\inf\{f_0(x):f_i(x)\le0,\ h_j(x)=0,\ x\in\mathcal D\},
$$

定义

$$
L(x,\lambda,\nu)
=f_0(x)+\lambda^Tf(x)+\nu^Th(x),
\qquad\lambda\ge0,
$$

$$
g(\lambda,\nu)=\inf_{x\in\mathcal D}L(x,\lambda,\nu),
\qquad
d^*=\sup_{\lambda\ge0,\nu}g(\lambda,\nu).
$$

primal feasible 指 $x\in\mathcal D$ 且满足全部 constraints；dual feasible 指 $\lambda\ge0$ 且 $g(\lambda,\nu)>-\infty$（若把 $-\infty$ 也留在 domain，则它不给有效有限下界）。对 feasible pair：

$$
\operatorname{gap}
=f_0(x)-g(\lambda,\nu)\ge0.
$$

$p^*$ 可为 $\pm\infty$；$g$ 可为 $-\infty$；$d^*$ 可为 extended value。attainment 只有在值由某个 finite point 取得时成立。

### OPT-DUAL-A02

- weak duality：总有 $d^*\le p^*$；
- strong duality：$d^*=p^*$；
- primal/dual attainment：分别存在点取得 infimum/supremum；
- Slater：convex inequalities、affine equalities下存在 relative-interior strict-feasible point；
- 标准有限维 convex/Slater 条件通常给 strong duality、dual attainment 与 KKT multiplier existence。

但逆向一般不成立：

$$
\text{Slater}\Longrightarrow
\text{zero gap + dual attainment}
$$

是带 theorem assumptions 的充分箭头；zero gap 不推出 Slater，也不推出任一侧 attainment。KKT 已存在时在 convex problem 中可证明 primal optimality，但“optimal”不无条件推出 KKT。

### OPT-DUAL-A03

对固定 $x$，$L(x,\cdot)$ 是 affine。任意 $t\in[0,1]$：

$$
\begin{aligned}
g(tz_1+(1-t)z_2)
&=\inf_x[tL(x,z_1)+(1-t)L(x,z_2)]\\
&\ge t\inf_xL(x,z_1)+(1-t)\inf_xL(x,z_2).
\end{aligned}
$$

故 $g$ concave，与 $f_0,f_i$ 是否 convex 无关。最大化 concave $g$ over convex set $\lambda\ge0$ 在形式上是 convex optimization；但一次 $g$ evaluation 可能要求求解 nonconvex global infimum，$g$ 也可能 nonsmooth、无 closed form 或 dimension 巨大，所以形式类别不保证计算容易。

## B. 手算与构造

### OPT-DUAL-B01

Lagrangian：

$$
L(x,\nu)
=\frac12\|x-c\|^2+\nu^T(Ax-b).
$$

对 $x$ stationarity：

$$
x-c+A^T\nu=0
\quad\Longrightarrow\quad
x(\nu)=c-A^T\nu.
$$

代回：

$$
g(\nu)
=\nu^T(Ac-b)-\frac12\|A^T\nu\|^2.
$$

dual 是 $\max_\nu g(\nu)$。若 $A$ full row rank：

$$
AA^T\nu^*=Ac-b,
$$

$$
\nu^*=(AA^T)^{-1}(Ac-b),
$$

$$
x^*=c-A^T(AA^T)^{-1}(Ac-b).
$$

$x^*$ 是 $c$ 到 affine set 的 projection。因 primal objective strongly convex，feasible 时 $x^*$ unique。rank deficient 时可用

$$
x^*=c-A^T(AA^T)^\dagger(Ac-b);
$$

primal 仍 unique，但 $\nu^*+z$ 对任何 $z\in\ker A^T$ 产生同一 $x^*$，故 multiplier 可不唯一。若 $b\notin\operatorname{range}A$，primal infeasible，以上不再是 primal solution。

### OPT-DUAL-B02

引入 $r=Ax-b$，取 multiplier $u$：

$$
L(x,r,u)
=\frac12\|r\|^2+\lambda\|x\|_1
+u^T(Ax-b-r).
$$

对 $r$ 取 infimum得到 $r=u$ 与贡献 $-\frac12\|u\|^2$；对 $x$ 取 infimum有限当且仅当

$$
\|A^Tu\|_\infty\le\lambda.
$$

故

$$
\max_u-\frac12\|u\|^2-b^Tu
\quad\text{s.t. }\|A^Tu\|_\infty\le\lambda.
$$

给定 $x$，令 $r=Ax-b$。若 $A^Tr=0$，取 $u=r$；否则取

$$
\alpha=\min\left\{1,\frac{\lambda}{\|A^Tr\|_\infty}\right\},
\qquad u=\alpha r.
$$

则 $u$ dual feasible。certificate：

$$
\mathcal G
=\frac12\|r\|^2+\lambda\|x\|_1
+\frac12\|u\|^2+b^Tu.
$$

exact optimum 满足 $-A^Tu^*\in\lambda\partial\|x^*\|_1$，所以

$$
|A_j^Tu^*|<\lambda\Longrightarrow x_j^*=0.
$$

不能把 current $u$ 直接替代 $u^*$。dual objective 可写为

$$
\frac12\|b\|^2-\frac12\|u+b\|^2,
$$

具有 $1$-strong concavity，因而可由 gap 得到保守半径

$$
\|u-u^*\|\le\sqrt{2\mathcal G}.
$$

于是 safe rule 为

$$
|A_j^Tu|+\|A_j\|\sqrt{2\mathcal G}<\lambda
\Longrightarrow x_j^*=0.
$$

### OPT-DUAL-B03

最小化目标：

$$
f(x)=-C(x)
=-\frac32+\frac12(x_1x_2+x_2x_3+x_3x_1).
$$

binary signs 对三角形最多切两条边，故 $\max C=2$，即

$$
p^*=-2.
$$

对 equalities $x_i^2=1$ 引入 free $\nu_i$：

$$
L(x,\nu)
=-\frac32-\sum_i\nu_i
+x^TM(\nu)x,
$$

其中

$$
M(\nu)=
\begin{bmatrix}
\nu_1&1/4&1/4\\
1/4&\nu_2&1/4\\
1/4&1/4&\nu_3
\end{bmatrix}.
$$

若 $M\succeq0$，对 $x$ 的 infimum在 $x=0$ 为

$$
g(\nu)=-\frac32-\sum_i\nu_i;
$$

否则沿 negative-eigenvalue direction 得 $g=-\infty$。dual：

$$
\max_\nu-\frac32-\sum_i\nu_i
\quad\text{s.t. }M(\nu)\succeq0.
$$

problem 对任意 coordinate permutation invariant。将任一 feasible $\nu$ 的所有 permutation 平均，PSD 与 objective 保持，故可取 $\nu_i=a$。此时 eigenvalues 为

$$
a+\frac12,\quad a-\frac14,\quad a-\frac14.
$$

PSD 要 $a\ge1/4$。objective 随 $a$ 减小而增大，故 $a=1/4$：

$$
d^*=-\frac32-\frac34=-\frac94.
$$

于是

$$
d^*=-\frac94<-2=p^*,
\qquad p^*-d^*=\frac14.
$$

gap 来自 quadratic/semidefinite convex relaxation，清楚展示 nonconvex formulation-dependent duality gap。

## C. 推导与证明

### OPT-DUAL-C01

concavity 见 A03。weak duality：任取 primal-feasible $\tilde x$ 和 $\lambda\ge0$，

$$
g(\lambda,\nu)
=\inf_xL(x,\lambda,\nu)
\le L(\tilde x,\lambda,\nu)
$$

使用 infimum；再由 $f_i(\tilde x)\le0,\lambda_i\ge0,h(\tilde x)=0$：

$$
L(\tilde x,\lambda,\nu)\le f_0(\tilde x).
$$

对 feasible $\tilde x$ 取 infimum得 $g\le p^*$，再对 dual-feasible multipliers 取 supremum：

$$
d^*\le p^*.
$$

没有一步使用 convexity。

### OPT-DUAL-C02

定义

$$
\mathcal A=
\left\{(u,v,t):
\exists x,\ f_i(x)\le u_i,\ h(x)=v,\ f_0(x)\le t
\right\}.
$$

convex assumptions 使 $\mathcal A$ convex；$t<p^*$ 时 $(0,0,t)\notin\mathcal A$。分离得到 nonzero coefficient $(\lambda,\nu,\mu)$。upper-set 方向迫使 $\lambda\ge0,\mu\ge0$。Slater/relative-interior regularity排除 $\mu=0$ 的 abnormal separator，于是可正规化 $\mu=1$。分离式重排得到

$$
\inf_xL(x,\lambda,\nu)\ge p^*.
$$

weak duality给反向 inequality，因此 equality。relative interior 让“内部”相对于真实 affine hull 定义；否则 lower-dimensional domain 的 ordinary interior 为空，分离/normalization 条件会被误判。完整 theorem 还需 properness/closure 与 finite value。

### OPT-DUAL-C03

引入 $z=Ax$：

$$
L(x,z,y)=f(z)+g(x)+y^T(Ax-z).
$$

分别取 infimum：

$$
\inf_z[f(z)-y^Tz]=-f^*(y),
$$

$$
\inf_x[g(x)+(A^Ty)^Tx]=-g^*(-A^Ty).
$$

故 dual：

$$
\max_y-f^*(y)-g^*(-A^Ty).
$$

一个常用 qualification 是存在

$$
\bar x\in\operatorname{ri}(\operatorname{dom}g),
\qquad
A\bar x\in\operatorname{ri}(\operatorname{dom}f).
$$

optimal pair 满足

$$
y^*\in\partial f(Ax^*),
\qquad
-A^Ty^*\in\partial g(x^*).
$$

等价的 Fenchel–Young equalities：

$$
f(Ax^*)+f^*(y^*)={y^*}^TAx^*,
$$

$$
g(x^*)+g^*(-A^Ty^*)=-{y^*}^TAx^*.
$$

相加为零 gap。

## D. 反例与失败边界

### OPT-DUAL-D01

constraint 只允许 $x=0$，故 primal attained 且 $p^*=0$。Lagrangian：

$$
L(x,\lambda)=x+\lambda x^2,\qquad\lambda\ge0.
$$

当 $\lambda>0$：

$$
g(\lambda)
=\inf_x(\lambda x^2+x)
=-\frac1{4\lambda}.
$$

$\lambda=0$ 时 $g=-\infty$。因此

$$
d^*=\sup_{\lambda>0}-\frac1{4\lambda}=0=p^*,
$$

但只有 $\lambda\to\infty$ 才趋近 $0$，不存在 finite maximizer。KKT stationarity at $x=0$ 要

$$
1+\lambda(2x)=1=0,
$$

无解。Slater/MFCQ 失败；这是“zero value gap 不推出 dual attainment/KKT existence”的完全手算反例。

### OPT-DUAL-D02

(a)

$$
\min x^2\quad\text{s.t. }x^2\le0
$$

只有 $x=0$，Slater 不成立。dual $g(\lambda)=\inf_x(1+\lambda)x^2=0$，故 zero gap且 dual attained。反驳“Slater 必要”。

(b) 将 extended objective 定为 $f(x)=x$ on $(0,\infty)$、否则 $+\infty$，并加 $x\le1$。$x=1/2$ strict feasible，但 $p^*=0$ 只由 $x\downarrow0$ 趋近，未 attained；extended objective 不 closed。反驳“Slater 保证 primal attainment”。Slater主要给 value duality/dual multiplier，primal existence还需 closedness/coercivity/compact level set 等。

(c)

$$
\min x^2\quad\text{s.t. }x^2=1
$$

非凸但 $p^*=1$。dual $g(\nu)=-\nu$ for $\nu\ge-1$，否则 $-\infty$；最大在 $\nu=-1$ 得 $1$。反驳“nonconvex 必 positive gap”。

### OPT-DUAL-D03

例一：$\min x^2$ s.t. $x\ge1$。拿 $x=0$ 与合法 dual lower bound $0$ 相减会报告 gap $0$，但 $x$ 不可行，真实 optimum是 $1$。修复：先报告 violation $[1-x]_+$；只有 primal feasible objective 才构成 upper bound。

例二：nonconvex dual function定义为 global $\inf_xL$，若 inner solver只找到 local value $\tilde g>g$，用 $f_0(x)-\tilde g$ 可能过小或为负。修复：inner solver必须提供 certified lower bound $\underline g\le g$，或给误差方向

$$
\tilde g-\epsilon\le g\le\tilde g
$$

并使用 $\tilde g-\epsilon$。同时验证 multiplier sign/domain、primal residual 和 floating-point tolerance。

## E. AI 迁移

### OPT-DUAL-E01

以 reference measure $r_i>0$ 最小化 negative entropy：

$$
\min_{p\ge0}
\sum_ip_i\log\frac{p_i}{r_i}
\quad\text{s.t. }\sum_ip_i=1,\quad\sum_ip_iT_i=\tau.
$$

interior stationarity给

$$
p_i(\eta)
=\frac{r_i e^{\eta^TT_i}}
{\sum_jr_je^{\eta^TT_j}},
$$

符号可随 multiplier convention 改变。消去 normalization 后，dual 等价于优化

$$
\eta^T\tau-\log\sum_jr_je^{\eta^TT_j}.
$$

若 $\tau$ 在 moment polytope relative interior，通常存在 finite $\eta^*$ 且 $p_i^*>0$；若在 boundary，最优 distribution可有 zero support，表达它的 parameter sequence可能 $\|\eta_k\|\to\infty$，value 仍可收敛但 finite dual parameter 不 attained。必须保留 relative interior、support 与 base measure。

### OPT-DUAL-E02

报告至少包含：

1. 被验证 property、perturbation set 与 input；
2. primal adversarial maximization/minimization方向；
3. relaxation（LP/SDP/convex envelope）及其包含关系；
4. dual value 是 upper bound 还是 lower bound；
5. dual-feasible residual、rounding 与 interval safety margin；
6. found adversarial witness 的 primal feasibility/value；
7. primal–dual/relaxation gap；
8. inner solve tolerance 与 numerical precision；
9. bound 对单 sample、有限 dataset 还是 population；
10. 不通过验证是“property false”还是“relaxation inconclusive”。

只有 primal witness 能证明 violation；loose dual bound通常只能表示未证成，不能反向证明模型不安全。

### OPT-DUAL-E03

若 local variables $x_s$ 满足 coupling

$$
\sum_sA_sx_s=b,
$$

Lagrangian 分解为

$$
\sum_s\big(f_s(x_s)+\nu^TA_sx_s\big)-\nu^Tb.
$$

给定 $\nu$，各 shard 独立求 $x_s(\nu)$。dual subgradient：

$$
\partial g(\nu)\ni\sum_sA_sx_s(\nu)-b.
$$

dual ascent更新 multiplier。若 local solve inexact，subgradient 与 lower-bound value 都带误差；需 summable/controlled errors。dual iterate的 local minimizers未必满足 coupling，需 averaging、projection 或 primal recovery。若 constraints 是 sample estimates，dual feasibility/value只证明 empirical problem；heterogeneity、privacy noise 与 held-out violation属于 statistical layer，不能由 numerical zero gap 消除。

