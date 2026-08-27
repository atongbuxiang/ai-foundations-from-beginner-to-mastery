---
type: exercise
status: draft
area: [math/functional-analysis, math/hilbert-spaces, ai/operator-learning]
topic: "Banach 空间、Hilbert 空间与正交投影"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Banach 空间、Hilbert 空间与正交投影]]", "[[度量空间、拓扑与连续映射]]", "[[内积空间]]"]
related: ["[[练习与测验 MOC]]", "[[实验 - 完备化、最佳逼近与条件期望投影审计]]"]
solution: "[[解答 - Banach 空间、Hilbert 空间与正交投影]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - Banach 空间、Hilbert 空间与正交投影

> [!abstract] 训练目标
> 能从 finite-dimensional intuition 进入 function spaces：检查 norm/completeness，区分 Banach/Hilbert，重建 projection/Riesz theorem，处理 orthogonal series与 weak convergence，并把条件期望、HiPPO、RKHS和 neural operator写成可审计的空间合同。

> [!warning] 作答合同
> 每次写“收敛、闭、连续、最优、正交、基、梯度”，必须标明 ambient space、norm/topology、measure、closure与量词；不得用 sampled-vector直觉替代 continuum theorem。

## A. 定义、类型与无限维边界

### GEO-HIL-A01

建立下列对象的“定义—依赖结构—最小例子—失效边界—AI 对应”表：normed space、Banach、pre-Hilbert、Hilbert、completion、continuous dual、closed span、Hamel/Schauder/orthonormal basis、strong/weak convergence、orthogonal projection、Riesz map。

判断并纠错：所有 Cauchy sequences收敛；所有 subspaces closed；closed bounded set compact；所有 linear maps continuous；Banach space都有唯一 nearest-point projection；ONB expansion逐点成立。

### GEO-HIL-A02

对 $\ell^1,\ell^2,\ell^\infty,c_0,c_{00},C([0,1]),L^1,L^2,H^1$ 分别说明：元素是什么、是否 quotient by a.e.、norm、complete性、是否 inner-product norm、point evaluation是否定义良好/连续。至少给三个“同一集合换 norm后结论改变”的例子。

### GEO-HIL-A03

比较：finite/infinite dimension；algebraic/topological direct sum；dense/closed；best approximation/projection/proximal map；$L^2$/pointwise/uniform convergence；strong/weak/weak-* convergence；population function norm/discrete sample norm。每组给一条不可逆 implication或反例。

## B. 手算、构造与函数逼近

### GEO-HIL-B01

令 $x^{(N)}=(1,1/2,\ldots,1/N,0,\ldots)\in c_{00}$：

1. 证明它在 $\ell^2$ norm中 Cauchy；
2. 证明它在 $c_{00}$ 无 limit、在 $\ell^2$ 的 limit是什么；
3. 证明它在 $\ell^1$ norm中非 Cauchy；
4. 给出 $\ell^2$ tail norm的 asymptotic order；
5. 说明 $c_{00}$ 在 $\ell^1,\ell^2,\ell^\infty$ norm下的 completions；
6. 构造 continuous polynomials在某 norm下 Cauchy但 limit不再 polynomial。

### GEO-HIL-B02

在 $H=L^2([0,1])$ 中取 $V=\operatorname{span}\{1,t\}$、$f(t)=t^2$：

1. 写 Gram/normal equations并求 $P_Vf$；
2. 验证 residual与 $1,t$ orthogonal；
3. 计算 projection error；
4. 写 Pythagorean identity；
5. 将 basis换成 shifted Legendre orthonormal basis重算；
6. 比较用均匀 sample ordinary least squares得到的离散系数，说明何时逼近 continuum projection。

### GEO-HIL-B03

1. 在 $\ell^1(\mathbb R^2)$ 中求 $(1,0)$ 到 $\operatorname{span}(1,1)$ 的全部 nearest points；
2. 在 Euclidean norm中求唯一 nearest point；
3. 构造一个 idempotent但非 self-adjoint的 oblique projection并求 norm；
4. 对 $M=c_{00}\subset\ell^2$ 和 $x=(1/k)$ 证明 distance为0但 minimizer不存在；
5. 逐项指出 uniqueness/existence/linearity分别依赖哪些条件。

## C. 核心定理证明链

### GEO-HIL-C01

完整证明 Hilbert projection theorem：从 minimizing sequence、midpoint convexity与 parallelogram law证明 Cauchy；用 completeness/closedness得到 existence；用 midpoint证明 uniqueness；再推 variational inequality。标注删去 closed、convex、complete、inner-product geometry各会断在哪一步。

### GEO-HIL-C02

对 closed subspace $M\subset H$：

1. 证明 nearest point等价于 residual orthogonal；
2. 证明 $P_M$ linear、bounded、$\|P_M\|=1$；
3. 证明 $P_M^2=P_M=P_M^*$；
4. 证明 $H=M\oplus M^\perp$；
5. 证明 $(M^\perp)^\perp=\overline M$；
6. 证明 self-adjoint idempotent的 converse；
7. 推导 nested closed subspaces $M\subset N$ 时 $P_MP_N=P_M$，并判断 $P_NP_M$。

### GEO-HIL-C03

1. 用 projection theorem证明 Hilbert-space Riesz representation与 norm equality；
2. 由 finite orthogonal projections证明 Bessel；
3. 证明 complete ON system下 norm-convergent expansion与 Parseval；
4. 证明 coefficient map是到 $\ell^2$ 的 isometry（complete时 onto）；
5. 解释 complex inner-product convention怎样改变 Riesz map线性方向。

## D. 反例、收敛与数值边界

### GEO-HIL-D01

构造：weak-not-strong sequence；closed unit ball非 compact；proper dense subspace；bounded但无 strongly convergent subsequence；Bessel strict inequality；$L^2$ convergence但无全序列 pointwise convergence的例子或标准构造说明。每例指出被否定的有限维直觉。

### GEO-HIL-D02

证明/反驳：

1. $L^2$ point evaluation bounded；
2. $L^2$ norm小蕴含 sup norm小；
3. Fourier partial sums的 $L^2$ convergence蕴含 uniform convergence；
4. 增加 basis数量使 sampled least-squares test error单调下降；
5. bounded function sequence总有 strongly convergent subsequence；
6. weak convergence保 norm；
7. finite-grid Euclidean gradient自动逼近 continuum $L^2$ gradient。

每项给最小反例或缺失条件。

### GEO-HIL-D03

设计 function-approximation audit：区分 approximation、quadrature/sampling、conditioning、optimization、floating-point与generalization errors；报告 $L^2$、weighted $L^2$、sup norm和pointwise probes；做 basis size与mesh refinement。解释为什么单一训练 MSE不能证明 continuum best approximation或discretization invariance。

## E. AI 与研究型迁移

### GEO-HIL-E01

在 $L^2(\Omega)$ 中把 $\mathbb E[Y\mid\mathcal G]$ 证明为 closed-subspace projection，并推 MSE Pythagorean decomposition、tower property的projection解释。比较 linear regression、unrestricted conditional mean、conditional median/quantile；指出 a.s. equivalence与finite-data estimator边界。

### GEO-HIL-E02

以 HiPPO/SSM 为对象写 derivation audit：指定 time-dependent measure、orthogonal polynomial family、projection coefficients、basis normalization、continuous coefficient dynamics与discretization。说明 changing measure为何改变“最优记忆”，并设计实验区分 continuum projection error、recurrence error与downstream task accuracy。

### GEO-HIL-E03

为 neural operator/RKHS/function-space optimization三选一写 research contract：input/output Banach/Hilbert spaces、norm、compact/regularity assumptions、sampling/encoder/decoder、Riesz gradient或bounded evaluation、approximation/generalization/discretization claim，并给一个会让 finite-grid结果无法提升为 continuum theorem的反例。

## 作答记录

| 题号 | 首次用时 | 状态 | 主要断点 | 48 小时重做 | 14 天迁移 |
|---|---:|---|---|---|---|
| A01 |  | not-attempted |  |  |  |
| A02 |  | not-attempted |  |  |  |
| A03 |  | not-attempted |  |  |  |
| B01 |  | not-attempted |  |  |  |
| B02 |  | not-attempted |  |  |  |
| B03 |  | not-attempted |  |  |  |
| C01 |  | not-attempted |  |  |  |
| C02 |  | not-attempted |  |  |  |
| C03 |  | not-attempted |  |  |  |
| D01 |  | not-attempted |  |  |  |
| D02 |  | not-attempted |  |  |  |
| D03 |  | not-attempted |  |  |  |
| E01 |  | not-attempted |  |  |  |
| E02 |  | not-attempted |  |  |  |
| E03 |  | not-attempted |  |  |  |

> [!important] 状态语义
> 题集已 `composed`，学习状态仍是 `not-attempted`；没有首次闭卷原稿、重做和迁移证据，不升级正文的 `draft` 状态。
