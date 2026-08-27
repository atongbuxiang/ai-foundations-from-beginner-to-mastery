---
type: solution
status: draft
area: [math/functional-analysis, math/hilbert-spaces, ai/operator-learning]
topic: "Banach 空间、Hilbert 空间与正交投影"
exercise: "[[习题 - Banach 空间、Hilbert 空间与正交投影]]"
prerequisites: ["[[Banach 空间、Hilbert 空间与正交投影]]"]
related: ["[[练习与测验 MOC]]", "[[实验 - 完备化、最佳逼近与条件期望投影审计]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - Banach 空间、Hilbert 空间与正交投影

> [!abstract] 使用方式
> 本文逐题独立作答，不用“见正文”代替证明。正式阅读前应先保留闭卷原稿；比对时重点检查 ambient space、norm/topology、closure、measure与 convergence mode。

## A01 解答：对象合同与有限维错觉

Normed space给 vector operations与 norm-induced metric；Banach再要求 norm-Cauchy completeness。Pre-Hilbert的 norm来自 inner product但未必 complete；Hilbert是其 complete版本。Completion是含原空间等距稠密副本的 complete space。

$X^*$ 由 bounded linear functionals组成；closed span是 finite combinations的 norm closure。Hamel basis只许 finite sums；Schauder basis给有序 norm-convergent series；ONB是 orthonormal且 closed span为全 Hilbert space。Strong是 norm convergence；weak是所有 $f\in X^*$ 上 convergence。Orthogonal projection需 Hilbert inner product与 closed subspace；Riesz map把 $H^*$ functional表示为 inner product vector。

六个判断全错：Cauchy需 complete；infinite-dimensional subspace可不 closed；closed bounded不 compact；linear map可 unbounded；general Banach nearest point可不存在/不唯一；ONB expansion只默认 norm convergence。

## A02 解答：空间分类

| 空间 | 元素/norm | complete | inner-product/point value |
|---|---|---|---|
| $\ell^1$ | absolutely summable sequences | 是 | standard norm非内积；coordinate bounded |
| $\ell^2$ | square summable | 是 | Hilbert；coordinate bounded |
| $\ell^\infty$ | bounded sequences/sup | 是 | 非Hilbert |
| $c_0$ | converging-to-zero/sup | 是 | 非Hilbert |
| $c_{00}$ | finite support | 否 in standard $p$ norms | $\ell^2$ inner product下pre-Hilbert |
| $C[0,1]$ | continuous functions/sup | 是 | 通常非Hilbert；evaluation bounded |
| $L^1$ | a.e. classes/integral | 是 | 非Hilbert；point value不定义 |
| $L^2$ | a.e. classes/square integral | 是 | Hilbert；point evaluation不定义/不bounded |
| $H^1$ | weak derivative in $L^2$ | 是 | standard Sobolev inner product给Hilbert；特定dimension/domain下才有continuous representative/evaluation |

同一 $c_{00}$ 用 $p=1,2,\infty$ completion分别为 $\ell^1,\ell^2,c_0$；$C[0,1]$ 用 sup norm complete，用 inherited $L^1$ norm不 complete；finite vectors用 $\ell^1/\ell^2$ topology等价但 projection geometry不同。

## A03 解答：层级与反例

Finite dimension中 norms equivalent、subspaces closed、bounded sequences有convergent subsequence；infinite dimension均可失败。Dense不蕴含closed：$c_{00}$ dense in $\ell^2$；closed proper subspace不 dense。Topological direct sum要求addition inverse连续，强于algebraic unique decomposition。

Projection是到subspace的线性idempotent（orthogonal时self-adjoint）；proximal map可投到nonlinear convex set且通常非linear。Uniform convergence蕴含 pointwise；在finite-measure domain还蕴含 $L^2$，反向均失败。Strong蕴含weak，反向失败；weak-*测试predual且与weak对象不同。Sample vector norm只有配 quadrature/encoder后才能对应 continuum norm。

## B01 解答：$c_{00}$ 与三种 completion

对 $M>N$：

$$\|x^{(M)}-x^{(N)}\|_2^2
=\sum_{k=N+1}^M k^{-2}\le\sum_{k>N}k^{-2}\le N^{-1}.$$

故 Cauchy。Coordinatewise limit必须是 $x=(1/k)$，它属于 $\ell^2$ 因 $\sum k^{-2}<\infty$，但不属于 $c_{00}$。Integral comparison给

$$
\frac1{N+1}\le\sum_{k>N}k^{-2}\le\frac1N,
$$

所以 tail norm $\asymp N^{-1/2}$。

$\ell^1$ 中

$$\|x^{(2N)}-x^{(N)}\|_1=\sum_{N<k\le2N}k^{-1}\to\log2,$$

故非 Cauchy。Completions分别是 $\ell^1,\ell^2,c_0$。多项式例：由 Weierstrass theorem取 polynomials uniformly approximating $|t-1/2|$；它们在 sup norm Cauchy但 limit不是 polynomial。

## B02 解答：$t^2$ 到 affine functions

设 projection $a+bt$。Normal equations：

$$
\begin{bmatrix}1&1/2\\1/2&1/3\end{bmatrix}
\begin{bmatrix}a\\b\end{bmatrix}
=\begin{bmatrix}1/3\\1/4\end{bmatrix},
$$

得 $a=-1/6,b=1$。Residual $r=t^2-t+1/6$ 满足 $\int r=\int tr=0$，且

$$\|r\|_2^2=\int_0^1r^2dt=\frac1{180}.$$

任意 $g\in V$：

$$\|f-g\|_2^2=\frac1{180}+\|t-1/6-g\|_2^2.$$

Orthonormal basis $\phi_0=1,\phi_1=\sqrt3(2t-1)$；coefficients为 $1/3,\sqrt3/6$，重建仍是 $t-1/6$。Uniform sample OLS的 empirical Gram/RHS在 mesh refinement且 quadrature一致时趋于上述 integrals；finite mesh、weights与conditioning决定偏差，不能直接等同。

## B03 解答：非Hilbert与非closed反例

$\ell^1$ distance

$$d(t)=|1-t|+|t|$$

在 $t\in[0,1]$ 恒为1，全部 $t(1,1)$ 都是 nearest points。Euclidean squared distance $(1-t)^2+t^2$ 在 $t=1/2$ 唯一最小，projection为 $(1/2,1/2)$。

取

$$P=\begin{bmatrix}1&2\\0&0\end{bmatrix}.$$

$P^2=P$，但 $P^\top\ne P$；Euclidean operator norm为 $\sqrt5$。其 range是 $x$轴，kernel为 $\operatorname{span}(-2,1)$，两者不orthogonal。

对 $M=c_{00}$，truncations逼近 $x=(1/k)$，所以 distance为0；若有 minimizer $m$，则 $\|x-m\|=0$ 给 $m=x\notin M$。Existence需closed/completeness结构；uniqueness依Hilbert strict geometry/convexity；linearity只对subspace projection成立。

## C01 解答：projection theorem

令 $d=\inf_C\|x-z\|$，取 $y_n$ 使 distance趋于 $d$。Convexity保证 midpoint在 $C$。Parallelogram给

$$
\|y_n-y_m\|^2
=2\|x-y_n\|^2+2\|x-y_m\|^2
-4\left\|x-\frac{y_n+y_m}{2}\right\|^2
\le2\|x-y_n\|^2+2\|x-y_m\|^2-4d^2\to0.
$$

故 Cauchy。Hilbert completeness给 limit $p$，closedness给 $p\in C$，norm continuity给最小。若 $p,q$ 都最小，同式与 midpoint给 $\|p-q\|^2\le0$。

对 $z\in C$，$p+t(z-p)\in C$。展开

$$\|x-p-t(z-p)\|^2$$

在 $t=0$ 的右导数非负，得 $\operatorname{Re}\langle x-p,z-p\rangle\le0$；反向展开平方即得 optimality。删 convex midpoint失效；删 inner product无 parallelogram；删 completeness limit可逃出ambient；删closedness limit可不在 $C$。

## C02 解答：closed subspace投影

若 $m=P_Mx$，对任意 $v\in M$，$m+tv$均可行，平方距离在0最小；real/imaginary $t$ 给 $\langle x-m,v\rangle=0$。反向由 Pythagoras得最优。

分解 $x=m+r$ 唯一且 linear operations分别保 $M,M^\perp$，故 $P_M$ linear。$\|Px\|\le\|x\|$；在非零 $m\in M$ 上 equality，故 norm 1。Range/kernel给 $P^2=P$；用正交分解验证 $\langle Px,y\rangle=\langle x,Py\rangle$。

每个 $x$ 均在 $M+M^\perp$，intersection为0，故 direct sum。$M\subset(M^\perp)^\perp$，后者closed；对 $x\notin\overline M$，投到 $\overline M$ 后 residual给一个把 $x$ 排除的 orthogonal vector，故双补为closure。

若 $P=P^*=P^2$，对 $u=Px$、$v=(I-P)y$，$\langle u,v\rangle=\langle x,P(I-P)y\rangle=0$，故orthogonal projection。若 $M\subset N$，$P_M(P_Nx)=P_Mx$，所以 $P_MP_N=P_M$；且 $P_NP_M=P_M$ 因 $P_Mx\in N$。

## C03 解答：Riesz、Bessel与Parseval

若 $f\ne0$，$M=\ker f$ closed proper。取 $u\in M^\perp\setminus\{0\}$。每个 $x$ 唯一写 $m+\alpha u$，且 $\alpha=f(x)/f(u)$。在第一变量线性 convention下取

$$y_f=\overline{f(u)}u/\|u\|^2,$$

便有 $f(x)=\langle x,y_f\rangle$。Uniqueness取差自身；Cauchy–Schwarz与测试 unit $y_f$ 给 norm equality。

对 finite ON family，Pythagoras给

$$\|x\|^2=\sum_{k\le n}|\langle x,e_k\rangle|^2+\|x-P_nx\|^2,$$

故 Bessel。Coefficients在 $\ell^2$，partial sums Cauchy并收敛到某 $z$；若system complete，$x-z$ orthogonal所有 $e_k$，只能为0，得到 expansion与Parseval。Coefficient map保 inner product/norm；任意 $c\in\ell^2$ 的series在 complete $H$ 收敛，故 onto。Riesz map在本 convention下对 functional到representer是 conjugate-linear；换 convention方向翻转。

## D01 解答：六个无限维反例

- $e_n\rightharpoonup0$ in $\ell^2$，但 norm恒1：weak非strong。
- $\|e_n-e_m\|=\sqrt2$：unit ball无convergent subsequence，非compact。
- $c_{00}\subset\ell^2$ proper dense且非closed。
- 同一 $(e_n)$ bounded却无strongly convergent subsequence。
- 在 $\ell^2$ 只取 ON system $\{e_{2k}\}$，对 $x=e_1$，Bessel left为0而 norm为1。
- Typewriter sequence：按层枚举 dyadic interval indicators。Support lengths趋零，故 $L^2$ norm趋零；但几乎每点每层恰落入一个interval，值反复为1/0，全序列不pointwise converge。

分别否定 finite-dimensional weak=strong/Heine–Borel/subspace closed/bounded precompact/Bessel=Parseval/$L^2$ implies pointwise。

## D02 解答：七个错误命题

1. 错：$L^2$ 是a.e. classes；narrow unit-norm spikes使chosen point value无界。
2. 错：宽度 $\varepsilon$、高度1的spike有 $L^2=\sqrt\varepsilon$、sup=1。
3. 错：$L^2$ theorem不含uniform；discontinuous function不可能被 continuous partial sums uniformly逼近。
4. 错：training residual可降，test error受noise/conditioning/overfit影响。
5. 错：orthonormal sequence bounded无strong subsequence。
6. 错：$e_n\rightharpoonup0$ 却 norms不趋0；只 lower semicontinuity。
7. 错：需要 quadrature mass matrix；raw coordinates的 Euclidean pairing一般随mesh scaling变化。

缺失条件依次是 bounded evaluation/RKHS、regularity、stronger convergence theorem、statistical controls、compactness、norm convergence、consistent discretization。

## D03 解答：六项误差账本

选 continuum $H=L^2(\mu)$、subspace $V_N$。报告

$$
\|f-P_{V_N}f\|_H
$$

作为 approximation error；用 independent high-order quadrature比较 exact/empirical Gram与RHS；报告 Gram condition number和solve residual；单列optimizer gap、floating precision与held-out distribution error。扫描 $N$、mesh $h$、noise/seed。

Norm report至少含 target weighted $L^2$、unweighted $L^2$、sup/quantile pointwise error，并解释各自measure。Training MSE只是在有限 sample/reduction下的 objective；不证明 exact coefficients、population norm最优、mesh convergence或unseen distribution generalization。

## E01 解答：conditional expectation

$M=L^2(\mathcal G)$ 对 $L^2$ limit closed：取a.s.-convergent subsequence或调用measurable limit closure。Projection $Z=P_MY$ 满足 $Z\in M$ 且

$$\mathbb E[(Y-Z)W]=0\quad\forall W\in M,$$

这等价于 conditional expectation的 integral characterization。于是对任意 $g\in M$：

$$\mathbb E[(Y-g)^2]
=\mathbb E[(Y-Z)^2]+\mathbb E[(Z-g)^2].$$

若 $\mathcal G\subset\mathcal H$，nested projections给

$$P_\mathcal GP_\mathcal H=P_\mathcal G,
\qquad P_\mathcal HP_\mathcal G=P_\mathcal G,$$

第一式即 tower property的 $L^2$ 版本。Linear regression投到有限linear span；conditional mean投到所有 $\sigma(S)$ measurable square-integrable functions。Absolute/quantile loss的Bayes acts是median/quantile，非orthogonal projection。所有随机变量只到a.s. class；finite samples只估计population object。

## E02 解答：HiPPO audit

先定义 history domain和 $\mu_t$，inner product

$$\langle f,g\rangle_t=\int f(s)\overline{g(s)}d\mu_t(s).$$

选在该measure下 orthonormal的 $\phi_n^{(t)}$，coefficients $c_n(t)=\langle u,\phi_n^{(t)}\rangle_t$；$P_Nu=\sum_{n<N}c_n\phi_n$ 是该时刻唯一 $L^2(\mu_t)$ best approximation。对 $t$ 求导时须同时微分 signal变换、basis和measure，得到 continuous dynamics；选 solver/step得到 recurrence。

Changing measure改变 inner product与“过去”的权重，所以 coefficients和best approximation目标一起变。实验分三层：高精度quadrature测 $\|u-P_Nu\|_{L^2(\mu_t)}$；把 recurrence coefficients与 direct projection比测discretization error；最后单独报告task metric。三者不可互相替代。

## E03 解答示例：neural operator contract

设 $X=H^s(D)$、$Y=L^2(D)$，目标 solution operator $\mathcal G:X\to Y$。必须给 compact input set或probability support、PDE well-posedness与 continuity norm。Encoder $E_h$采样/投影到mesh coefficients，decoder $D_h$重建；discrete network $G_h$ 要通过

$$\|D_hG_hE_hu-\mathcal G(u)\|_Y$$

与 continuum比较，并分 projection、model、optimization、sampling/generalization errors。

反例：只在固定 grid points上定义两个 continuous functions可采样完全相同，却在points之间有不同高频振荡和 $L^2/H^1$ norm；因此 finite-grid zero error不识别 continuum function/operator。若选 RKHS，则还需 kernel使 evaluation bounded；若做 function-space gradient，则需 Riesz map/mass matrix。

## 最终核对

应能独立重建：$c_{00}$ completion反例；parallelogram判据；closed-convex projection theorem；closed-subspace operator characterization；Riesz theorem；Bessel–Parseval；weak-not-strong；conditional expectation projection；continuum/discrete norm账本。

> [!important] 状态不自动升级
> 详解存在只表示验收工具 `composed`。未完成首次闭卷、错误分类、48小时重做、14天迁移与实验改参，仍为 `draft / not-attempted`。
