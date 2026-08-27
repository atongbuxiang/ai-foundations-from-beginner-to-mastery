---
type: solution
status: draft
area: [math/convex-analysis, math/nonsmooth-optimization, ai/regularization]
topic: "次梯度、共轭函数与 Fenchel 对偶"
exercise: "[[习题 - 次梯度、共轭函数与 Fenchel 对偶]]"
related: ["[[次梯度、共轭函数与 Fenchel 对偶]]", "[[优化与凸分析 MOC]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 次梯度、共轭函数与 Fenchel 对偶

> [!warning] 使用顺序
> 每个“等号”都核对 closedness、convexity、domain 与 relative-interior qualification。框架返回的单个 backward value 不是整个次微分，formal dual expression 也不是 strong-duality certificate。

## A. 识别与复述

### OPT-SUBG-A01

对 proper convex $f:\mathbb R^n\to\mathbb R\cup\{+\infty\}$，$g$ 是 $x\in\operatorname{dom}f$ 的 subgradient，当

$$
f(y)\ge f(x)+g^T(y-x),\qquad\forall y.
$$

$$
\partial f(x)=\{g:\text{上式对所有 }y\text{ 成立}\}.
$$

区别：

- classical gradient 是唯一的局部线性一阶近似；
- subgradient 是 global affine lower-bound slope，可以不唯一；
- directional derivative $f'(x;d)$ 对方向通常正齐次但未必线性；对 convex $f$，它是 $\partial f(x)$ 的 support function；
- autodiff convention 是程序在 branch/kink 处选择的一个返回值，不证明数学可微，也未必展示整个 $\partial f(x)$。

固定 $x$，每个 $y$ 给 $g$ 一个 closed halfspace：

$$
g^T(y-x)\le f(y)-f(x).
$$

$\partial f(x)$ 是这些 halfspaces 的 intersection，所以 closed convex；但可能 empty 或 unbounded。

### OPT-SUBG-A02

对 proper convex $f$：

- $x\in\operatorname{ri}(\operatorname{dom}f)$ 时通常有 $\partial f(x)\ne\varnothing$；
- 在 interior 标准条件下，$f$ differentiable at $x$ iff $\partial f(x)=\{\nabla f(x)\}$；
- Fermat rule：

$$
x^*\in\arg\min f
\Longleftrightarrow0\in\partial f(x^*);
$$

- 总有 $\partial f(x)+\partial g(x)\subseteq\partial(f+g)(x)$；若 relative interiors of domains 相交等 qualification 成立，则取 equality；
- 若 $h(x)=f(Ax+b)$，总有 $A^T\partial f(Ax+b)\subseteq\partial h(x)$，适当 qualification 下取 equality。

domain boundary 可能出现 empty/unbounded subdifferential；singleton 与 differentiability 的简洁结论、sum/chain equality 也可能需要额外条件。

### OPT-SUBG-A03

$$
f^*(y)=\sup_x\{y^Tx-f(x)\},
$$

$$
f^{**}(x)=\sup_y\{y^Tx-f^*(y)\}.
$$

Fenchel–Young gap：

$$
\mathcal G_f(x,y)=f(x)+f^*(y)-y^Tx\ge0.
$$

$$
\mathcal G_f(x,y)=0
\Longleftrightarrow y\in\partial f(x).
$$

若 $f$ proper closed convex：

$$
y\in\partial f(x)
\Longleftrightarrow x\in\partial f^*(y),
$$

且 Fenchel–Moreau 给 $f^{**}=f$。

weak duality 是每个 dual value 不超过每个 primal value；通常不需 constraint qualification。strong duality 是 optimal values 相等，需要相应条件。primal/dual attainment 分别表示 infimum/supremum 被某点取得；zero gap 不自动给两侧 attainment。

## B. 手算与构造

### OPT-SUBG-B01

1. 绝对值：

$$
\partial|x|=
\begin{cases}
\{1\},&x>0,\\[-2pt]
[-1,1],&x=0,\\[-2pt]
\{-1\},&x<0.
\end{cases}
$$

2. ReLU：

$$
\partial\max\{0,x\}=
\begin{cases}
\{0\},&x<0,\\
[0,1],&x=0,\\
\{1\},&x>0.
\end{cases}
$$

3. hinge $h(x)=\max\{0,1-x\}$：

$$
\partial h(x)=
\begin{cases}
\{-1\},&x<1,\\
[-1,0],&x=1,\\
\{0\},&x>1.
\end{cases}
$$

4. $\ell_1$ norm：

$$
\partial\|x\|_1
=\prod_i S_i,
$$

其中 $S_i=\{\operatorname{sign}(x_i)\}$ 若 $x_i\ne0$，而 $S_i=[-1,1]$ 若 $x_i=0$。

5. Euclidean norm at zero：

$$
\partial\|0\|_2=\{g:\|g\|_2\le1\}.
$$

因为 $\|y\|_2\ge g^Ty$ 对所有 $y$ iff $\|g\|_2\le1$。

6. 两 affine pieces 在

$$
2x-1=-x+2
$$

处相交，所以 $x=1$。active slopes 为 $2,-1$：

$$
\partial f(1)=\operatorname{conv}\{-1,2\}=[-1,2].
$$

### OPT-SUBG-B02

1. $f(x)=ax^2/2$：stationarity $y-ax=0$，所以

$$
f^*(y)=\frac{y^2}{2a},\qquad y\in\mathbb R.
$$

2. $f(x)=bx+c$：

$$
f^*(y)=\sup_x[(y-b)x-c]
=\begin{cases}
-c,&y=b,\\
+\infty,&y\ne b.
\end{cases}
$$

3. $f(x)=|x|$：若 $|y|\le1$，$yx-|x|\le0$ 且 $x=0$ 取 0；若 $|y|>1$，沿相应符号送 $|x|\to\infty$：

$$
f^*(y)=\delta_{[-1,1]}(y).
$$

4. $f=\delta_{[-r,r]}$：

$$
f^*(y)=\sup_{|x|\le r}yx=r|y|.
$$

5. $f(x)=e^x$。若 $y>0$，stationarity $y-e^x=0$ 给 $x=\log y$：

$$
f^*(y)=y\log y-y.
$$

$y=0$ 时 supremum of $-e^x$ 是 0，但不 attained；$y<0$ 时令 $x\to-\infty$，$yx-e^x\to+\infty$。因此

$$
f^*(y)=
\begin{cases}
y\log y-y,&y>0,\\
0,&y=0,\\
+\infty,&y<0.
\end{cases}
$$

采用 $0\log0=0$ 可合写 domain $y\ge0$。

### OPT-SUBG-B03

quadratic gap：

$$
\mathcal G_f(x,y)
=\frac12x^2+\frac12y^2-xy
=\frac12(x-y)^2.
$$

因此 gap zero iff $x=y$；同时 $\partial f(x)=\{x\}$，正是 $y=x$。

对 $f(x)=|x|$，$f^*=\delta_{[-1,1]}$。finite gap 要 $|y|\le1$：

$$
\mathcal G_f(x,y)=|x|-yx.
$$

- $x=0$：所有 $y\in[-1,1]$ 都 equality；
- $x>0$：gap $=x(1-y)$，equality iff $y=1$；
- $x<0$：gap $=(-x)(1+y)$，equality iff $y=-1$。

这些集合正好是 $\partial|x|$。

## C. 推导与证明

### OPT-SUBG-C01

令 active set $I(x)=\{i:f_i(x)=f(x)\}$。若

$$
g=\sum_{i\in I(x)}\alpha_i\nabla f_i(x),
\quad \alpha_i\ge0,\quad\sum_i\alpha_i=1,
$$

则对任意 $y$：

$$
\begin{aligned}
f(y)&\ge\sum_i\alpha_i f_i(y)\\
&\ge\sum_i\alpha_i
[f_i(x)+\nabla f_i(x)^T(y-x)]\\
&=f(x)+g^T(y-x).
\end{aligned}
$$

所以 active gradients 的 convex hull 包含于 $\partial f(x)$。

反向骨架：finite maximum 的 directional derivative 是

$$
f'(x;d)=\max_{i\in I(x)}\nabla f_i(x)^Td.
$$

而 $g\in\partial f(x)$ 蕴含 $g^Td\le f'(x;d)$ 对所有 $d$。若 $g$ 不在 active gradients 的 convex hull，strong separation 给某个 $d$ 使

$$
g^Td>max_{i\in I(x)}\nabla f_i(x)^Td,
$$

矛盾。因此等号成立。

$\|x\|_\infty=\max_i\{x_i,-x_i\}$。若 $M=\{i:|x_i|=\|x\|_\infty\}$ 且 $x\ne0$：

$$
\partial\|x\|_\infty
=\operatorname{conv}
\{\operatorname{sign}(x_i)e_i:i\in M\}.
$$

在 $x=0$，全部 $\pm e_i$ active，其 convex hull 是 $\ell_1$ unit ball。

### OPT-SUBG-C02

共轭定义直接给

$$
f^*(y)=\sup_z(y^Tz-f(z))\ge y^Tx-f(x),
$$

所以

$$
f(x)+f^*(y)\ge y^Tx.
$$

equality iff $x$ 达到 supremum，即对任意 $z$：

$$
y^Tx-f(x)\ge y^Tz-f(z).
$$

移项：

$$
f(z)\ge f(x)+y^T(z-x),
$$

恰为 $y\in\partial f(x)$。

若 $f$ proper closed convex，则 $f=f^{**}$。对 pair $(y,x)$ 应用同一 equality：

$$
f^*(y)+f^{**}(x)=x^Ty
\Longleftrightarrow x\in\partial f^*(y).
$$

用 $f^{**}=f$，它与原 equality相同。若没有 biconjugacy，不能无条件把 inverse relation 写成等价。

### OPT-SUBG-C03

引入 $z=Ax$：

$$
\min_{x,z}\;g(x)+f(z)
\quad\text{s.t. }Ax-z=0.
$$

Lagrangian：

$$
L(x,z,y)=g(x)+f(z)+y^T(Ax-z).
$$

对 $x,z$ 分开取 infimum：

$$
\inf_x[g(x)+(A^Ty)^Tx]=-g^*(-A^Ty),
$$

$$
\inf_z[f(z)-y^Tz]=-f^*(y).
$$

所以 dual 是

$$
\max_y\;-g^*(-A^Ty)-f^*(y).
$$

weak duality可直接由

$$
g(x)+g^*(-A^Ty)\ge-x^TA^Ty
$$

与

$$
f(Ax)+f^*(y)\ge y^TAx
$$

相加得到。一个常用 strong-duality qualification 是 $f,g$ proper closed convex 且

$$
\operatorname{ri}(A\operatorname{dom}g)
\cap\operatorname{ri}(\operatorname{dom}f)
\ne\varnothing.
$$

精确版本还需对应有限维/连续性表述；不能只写“both convex”。

## D. 反例与失败边界

### OPT-SUBG-D01

定义

$$
f(x)=
\begin{cases}
-\sqrt{x},&x\ge0,\\
+\infty,&x<0.
\end{cases}
$$

在 $(0,\infty)$ 上

$$
f''(x)=\frac1{4x^{3/2}}>0,
$$

加上 lower-semicontinuous boundary value，$f$ proper convex。若 $g\in\partial f(0)$，则对任意 $y>0$：

$$
-\sqrt y\ge gy.
$$

除以 $y$：

$$
g\le-\frac1{\sqrt y}.
$$

当 $y\downarrow0$，右侧趋于 $-\infty$，不存在 finite $g$ 同时满足，所以

$$
\partial f(0)=\varnothing.
$$

$0$ 是 domain boundary，不在 relative interior $(0,\infty)$。

### OPT-SUBG-D02

取

$$
f(x_1,x_2)=|x_1|+2|x_2|,
\qquad x=(1,0).
$$

$$
\partial f(1,0)=\{1\}\times[-2,2].
$$

选择 $g=(1,2)$，则 $d=-g=(-1,-2)$。directional derivative：

$$
f'(x;d)=d_1+2|d_2|=-1+4=3>0.
$$

事实上对充分小 $t>0$：

$$
f((1,0)+t(-1,-2))
=|1-t|+4t=1+3t>f(1,0).
$$

原因是 directional derivative 使用整个 $\partial f(x)$ 的 support，而不是只看选中的 $g$。subgradient method 常展开

$$
\|x_{k+1}-x^*\|^2
=\|x_k-x^*\|^2-2\eta_k g_k^T(x_k-x^*)
+\eta_k^2\|g_k\|^2
$$

并用 subgradient inequality 控制 distance/best or average objective；它不要求 objective monotone。

### OPT-SUBG-D03

取 double-well lower envelope

$$
f(x)=\min\{(x-1)^2,(x+1)^2\}
=(|x|-1)^2.
$$

它在 $-1,1$ 取 0，却在 $0$ 取 1，所以非凸。closed convex envelope 是

$$
f^{**}(x)=
\bigl(\max\{|x|-1,0\}\bigr)^2.
$$

在 $[-1,1]$ 上用连接两个 minima 的水平 chord 填成 0；区间外保留 convex outer branches。因此 $f^{**}(0)=0\ne1=f(0)$。

attainment 分离例：

$$
\inf_x e^x=0
$$

但无 finite primal minimizer。把它写成 $g(x)=0$、$f(x)=e^x$、$A=I$ 的 Fenchel form，formal dual 可给相同 optimal value，仍不能凭 zero gap 宣布 primal attained。一般 strong-duality theorem 还要求 relative-interior/continuity qualification；若 domains 不满足条件，只写出 dual expression最多证明 weak duality。

## E. AI 迁移

### OPT-SUBG-E01

令

$$
\ell(w)=\frac1{2n}\|Xw-y\|^2,
\qquad
\nabla\ell(w)=\frac1nX^T(Xw-y).
$$

最优性为

$$
0\in\nabla\ell(w^*)+\lambda\partial\|w^*\|_1.
$$

逐坐标：

$$
w_i^*\ne0
\Rightarrow
\nabla_i\ell(w^*)=-\lambda\operatorname{sign}(w_i^*),
$$

$$
w_i^*=0
\Rightarrow
|\nabla_i\ell(w^*)|\le\lambda.
$$

检查协议：报告 active coordinates 的 equality residual

$$
r_i=\nabla_i\ell+\lambda\operatorname{sign}(w_i),
$$

zero coordinates 的 violation

$$
v_i=(|\nabla_i\ell|-\lambda)_+,
$$

以及 global max/RMS residual、objective、scaling 与 tolerance。

subgradient update 是 $w^+=w-\eta(\nabla\ell+\lambda g)$；proximal gradient 是先 smooth step 再 soft-threshold；framework `sign(0)=0` 只选了一个 $g_i$，不能替代“存在某个 $g_i\in[-1,1]$ 抵消 smooth gradient”的证书。

### OPT-SUBG-E02

在 simplex 上令

$$
\phi(p)=\tau\sum_i p_i\log p_i.
$$

共轭：

$$
\phi^*(z)=\tau\log\sum_i e^{z_i/\tau}.
$$

最大化 stationarity 加 simplex multiplier 给

$$
p_i=\frac{e^{z_i/\tau}}{\sum_j e^{z_j/\tau}}.
$$

Fenchel–Young gap：

$$
\phi(p)+\phi^*(z)-p^Tz\ge0,
$$

equality iff $p=\operatorname{softmax}(z/\tau)$。验证项：

1. $p\ge0,\mathbf1^Tp=1$；
2. $z\mapsto z+c\mathbf1$ 不改变 $p$；
3. gap nonnegative/equality residual；
4. 用 $m=\max z_i$ 做 stable logsumexp；
5. 小 $\tau$ 下 overflow、underflow 与 Hessian scaling；
6. conjugacy 对 logits，不推出 logits generator 的 deep parameters convex。

### OPT-SUBG-E03

若 formal representation 是

$$
D_f(P\|Q)=\sup_T
\{E_PT-E_Qf^*(T)\},
$$

实际 neural critic 只在 $\mathcal T_\theta$ 中优化，因此得到

$$
\sup_{T\in\mathcal T_\theta}
\{E_PT-E_Qf^*(T)\}
\le D_f(P\|Q).
$$

gap 至少分为：

- representation/equality 的正式条件；
- critic-class approximation gap；
- finite optimization gap；
- empirical-to-population sampling gap；
- train/evaluation reuse 的 selection bias；
- numerical/domain clipping bias。

协议：固定 $f$ 与 orientation，记录 critic class/regularization/optimizer；train 与 evaluation samples 分离或 cross-fit；报告 empirical train bound、held-out bound、多 seed/bootstrapped uncertainty、optimization traces 和 known-distribution calibration；始终标注这是 lower bound，除非证明 unrestricted equality 与所有 gaps 可控。
