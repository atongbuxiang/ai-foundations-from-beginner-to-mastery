---
type: exercise
status: draft
area: [math/convex-analysis, math/nonsmooth-optimization, ai/regularization]
topic: "次梯度、共轭函数与 Fenchel 对偶"
difficulty: [A, B, C, D, E]
prerequisites: ["[[次梯度、共轭函数与 Fenchel 对偶]]"]
related: ["[[优化与凸分析 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - 次梯度、共轭函数与 Fenchel 对偶]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 次梯度、共轭函数与 Fenchel 对偶

> [!abstract] 训练目标
> 能把 kink 的几何、次微分集合、Fenchel 共轭和 primal–dual equality 组织成一条证书链；每次使用 calculus 或 strong duality 都写资格条件。

## A. 识别与复述

### OPT-SUBG-A01

定义 proper extended-real convex function 的 subgradient 与 subdifferential。解释它与 classical gradient、directional derivative、autodiff convention 的区别，并说明 $\partial f(x)$ 为什么是 closed convex set。

### OPT-SUBG-A02

陈述以下结论及条件：relative interior 上的 nonempty subdifferential；differentiability 与 singleton subdifferential；convex Fermat rule；sum rule 与 affine precomposition rule。指出哪些结论在 domain boundary 可能失效。

### OPT-SUBG-A03

定义 Fenchel conjugate、biconjugate 与 Fenchel–Young gap。陈述 equality、subgradient inverse relation 和 Fenchel–Moreau theorem；区分 weak duality、strong duality 与 attainment。

## B. 手算与构造

### OPT-SUBG-B01

逐点求下列次微分：

1. $|x|$；
2. $\max\{0,x\}$；
3. $\max\{0,1-x\}$；
4. $\|x\|_1$；
5. $\|x\|_2$ 在 $x=0$；
6. $f(x)=\max\{2x-1,-x+2\}$ 在两条 affine pieces 的交点。

### OPT-SUBG-B02

手算以下共轭并写 domain：

1. $f(x)=\frac a2x^2$，$a>0$；
2. $f(x)=bx+c$；
3. $f(x)=|x|$；
4. $f=\delta_{[-r,r]}$；
5. $f(x)=e^x$。

### OPT-SUBG-B03

令

$$
f(x)=\frac12x^2,
\qquad
f^*(y)=\frac12y^2.
$$

1. 计算 Fenchel–Young gap；
2. 描述 gap 为零的集合；
3. 对 $f(x)=|x|$ 与其共轭，分别讨论 $x=0$、$x\ne0$ 的 equality conditions；
4. 解释 equality 如何编码 $y\in\partial f(x)$。

## C. 推导与证明

### OPT-SUBG-C01

证明 pointwise maximum rule：若 $f=\max_i f_i$ 且各 $f_i$ differentiable convex，则

$$
\partial f(x)=
\operatorname{conv}\{\nabla f_i(x):i\in I(x)\}.
$$

至少证明“凸包包含于次微分”和反向结论的几何/方向导数骨架；再用于推导 $\ell_\infty$ norm 的次微分。

### OPT-SUBG-C02

从定义证明 Fenchel–Young inequality 及

$$
f(x)+f^*(y)=y^Tx
\Longleftrightarrow
y\in\partial f(x).
$$

若 $f$ proper closed convex，再证明等价于 $x\in\partial f^*(y)$。解释 biconjugacy 在哪一步被使用。

### OPT-SUBG-C03

对

$$
\min_x\;g(x)+f(Ax)
$$

通过 variable splitting 推导 Fenchel dual

$$
\max_y\;-g^*(-A^Ty)-f^*(y).
$$

用两次 Fenchel–Young 直接证明 weak duality，并给一个足以保证 strong duality 的 relative-interior condition。

## D. 反例与失败边界

### OPT-SUBG-D01

构造一个 proper convex function，在 domain boundary 的 subdifferential 为空。证明 convexity 和 empty subdifferential，说明为什么“convex function 每点都有 subgradient”错误。

### OPT-SUBG-D02

用具体 convex nonsmooth function 和具体点、次梯度 $g$，证明 $-g$ 未必是 function-value descent direction。计算 directional derivative，解释 subgradient method 的典型证明为何改为控制 distance/best iterate。

### OPT-SUBG-D03

给一个 nonconvex function $f$ 使 $f^{**}\ne f$，求或画出 $f^{**}$ 的 closed convex envelope。再给一个 formal dual 但不能无条件宣布 zero gap/attainment 的论证，指出缺失的 qualification。

## E. AI 迁移

### OPT-SUBG-E01

对 Lasso-type objective

$$
\frac1{2n}\|Xw-y\|^2+\lambda\|w\|_1
$$

写逐坐标最优性证书。设计 active/zero coordinates 的 residual 检查，并区分“subgradient update”“proximal soft-thresholding”和“framework 在零点选 sign=0”。

### OPT-SUBG-E02

从 negative entropy 与 logsumexp conjugacy 推导 softmax，并把 temperature 纳入。列出 simplex domain、additive-shift invariance、Fenchel–Young gap、numerical stabilization 和 deep-parameter nonconvexity 的验证项。

### OPT-SUBG-E03

审计一个用 variational critic 估计 $f$-divergence 的实验。区分 unrestricted Fenchel equality、critic-class restriction、optimization gap、finite-sample gap 和 evaluation reuse；设计能报告 lower-bound direction与不确定性的协议。
