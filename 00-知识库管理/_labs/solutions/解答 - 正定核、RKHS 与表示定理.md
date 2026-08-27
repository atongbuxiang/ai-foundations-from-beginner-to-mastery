---
type: solution
status: draft
area: [math/functional-analysis, math/kernel-methods, math/probability-metrics, ai/kernel-learning]
topic: "正定核、RKHS 与表示定理"
exercise: "[[习题 - 正定核、RKHS 与表示定理]]"
prerequisites: ["[[正定核、RKHS 与表示定理]]"]
related: ["[[练习与测验 MOC]]", "[[实验 - Gram 正定性、KRR 表示与随机特征近似审计]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 正定核、RKHS 与表示定理

> [!abstract] 使用方式
> 本文逐题独立作答，不用“见正文”代替证明。先闭卷完成[[习题 - 正定核、RKHS 与表示定理]]并保留原稿；比对时优先检查 PSD 全量词、set/RKHS/operator 三层对象、Mercer 额外条件、表示定理的存在唯一性边界，以及 sampling–kernel approximation–solver–task 四层误差是否分账。

## A01 解答：六种性质的量词审计

1. 实 PSD kernel 是 symmetric $k:\mathcal X^2\to\mathbb R$，且对每个 $n$、每组 $x_1,ldots,x_n$ 和每个 $c\in\mathbb R^n$，$\sum_{ij}c_ic_jk(x_i,x_j)\ge0$。复数版本要求 Hermitian 并用 $c_i\overline{c_j}$。
2. Strictly PD 通常要求 points互异时，对每个非零 $c$ 有严格正二次型。它保证相应 finite Gram matrix nonsingular。
3. Conditionally PD 的一个常见版本只对满足 $\sum_i c_i=0$ 的 $c$ 要求 $c^\top Kc\ge0$。它比 PSD 弱，常与 polynomial side constraints或centering配合。
4. RKHS 是 Hilbert space $\mathcal H$ of functions on $\mathcal X$，其中每个 point evaluation $\delta_x(f)=f(x)$ 都 bounded。由 Riesz theorem，存在唯一 $k_x\in\mathcal H$ 使 $f(x)=\langle f,k_x\rangle$。
5. Characteristic 是相对某个 probability-measure class $\mathcal P$ 的性质：mean embedding $P\mapsto\mu_P$ injective。
6. 在题设版本中，continuous kernel $k$ 在 compact Hausdorff $\mathcal X$ 上 universal，意为 $\mathcal H_k$ 在 $C(\mathcal X)$ 的 sup norm中 dense。

Strict PD、characteristic 与 universal不应无条件互推。它们分别控制 finite point interpolation、probability measure identification和function approximation density；关系依赖 domain、continuity和目标 measure/function class。Conditional PD 更不能直接替代 PSD。某一训练集 Gram positive definite只证明：该特定 finite points上的 quadratic form严格正，因而该矩阵 invertible；它不证明同一公式对任意未见 points仍 PSD或strictly PD。

## A02 解答：三层对象与形状

| 对象 | 定义 | 所在空间/形状 | 层级 |
|---|---|---|---|
| $k_x$ | $k(x,\cdot)$ | $\mathcal H_k$ 中的函数 | set + PSD kernel |
| $K$ | $K_{ij}=k(x_i,x_j)$ | $\mathbb R^{n\times n}$ | finite sample |
| $T_k$ | $(T_kf)(x)=\int k(x,z)f(z)d\mu(z)$ | 常为 $L^2(\mu)\to L^2(\mu)$ | population kernel + measure |
| $\mu_P$ | $\mathbb E_{X\sim P}k_X$ | $\mathcal H_k$ | distribution + Bochner integrability |
| $\widehat C$ | $n^{-1}\sum_i\tilde k_{x_i}\otimes\tilde k_{x_i}$ | finite-rank operator $\mathcal H_k\to\mathcal H_k$ | sample |
| $Z$ | $Z_{ir}=z_r(x_i)$ | $\mathbb R^{n\times D}$ | sample + randomized/deterministic feature scheme |

$k_x$、$K$ 和 Moore–Aronszajn RKHS只需 set + PSD kernel。$T_k$ 需 measure及 integral well-defined/bounded条件；classical Mercer还需 topology、compactness与continuity。$\mu_P$ 需例如 $\mathbb E\sqrt{k(X,X)}<\infty$。$\widehat C$ 还需 centered features具有二阶矩。RFF 特别需要适合的 spectral construction；经典 Bochner RFF 要 continuous shift-invariant PSD kernel。

## A03 解答：Mercer、表示定理与 GP 条件表

| 结论 | 课程版条件 | 结论 | 不保证 |
|---|---|---|---|
| Mercer | compact domain，finite Borel measure，continuous symmetric PSD kernel及support条件 | positive compact self-adjoint $T_k$；$k=\sum_j\lambda_j\psi_j\psi_j$，经典版本有强收敛 | 不是任意 set/kernel 的无条件级数；empirical spectrum不自动等于population |
| Representer | RKHS，loss只依赖有限 bounded observations，$\Omega(\|f\|)$ strictly increasing | 每个已有 minimizer在 representer span | 不自动保证 existence、uniqueness、convexity或sparsity |
| GP regression | $k$ 为合法 PSD covariance，finite observations，joint Gaussian prior；公式中另需 Gaussian iid noise $\sigma^2>0$ | posterior mean/covariance由 Gaussian conditioning给出 | 不保证 kernel/hyperparameters正确、frequentist coverage或大样本可算 |

Finite Gram eigendecomposition只是一组样本矩阵的谱分解，不证明 Mercer 的 population operator、eigenfunctions或uniform convergence。表示定理的条件不含 coercivity/lower-semicontinuity/strict convexity，因此不保证 minimizer存在唯一。任意 symmetric $k$ 不可作 covariance；每个 finite covariance matrix都必须 PSD。

## B01 解答：Polynomial kernel

令 $x=(x_1,x_2)$、$z=(z_1,z_2)$。展开：

$$
(1+x^\top z)^2
=1+2x_1z_1+2x_2z_2+x_1^2z_1^2+2x_1x_2z_1z_2+x_2^2z_2^2.
$$

可取

$$
\phi(x)=
\begin{bmatrix}
1&\sqrt2x_1&\sqrt2x_2&x_1^2&\sqrt2x_1x_2&x_2^2
\end{bmatrix}^{\!\top}\in\mathbb R^6.
$$

三点间 inner products为 $x_1^\top x_2=0$、$x_1^\top x_3=x_2^\top x_3=1$，self inner products为 $1,1,2$，故

$$
K=
\begin{bmatrix}
4&1&4\\
1&4&4\\
4&4&9
\end{bmatrix}.
$$

它是 $\Phi\Phi^\top$，故 PSD。Leading principal minors为 $4$、$15$，而 determinant

$$
4(36-16)-(9-16)+4(4-16)=39>0,
$$

故实际 positive definite。Kernel distance

$$
d_k(x_1,x_2)^2=k(x_1,x_1)+k(x_2,x_2)-2k(x_1,x_2)=4+4-2=6,
$$

所以 $d_k=\sqrt6$。$p=1/2$ 时 binomial expansion不再是有限 nonnegative feature sum；而 $1+x^\top z$ 在全 $\mathbb R^2$ 可为负，平方根甚至不是实函数。因此原 closure proof完全失效。

## B02 解答：Brownian kernel

在 $L^2[0,1]$ 中取 $\phi_t(u)=\mathbf1_{[0,t]}(u)$，则

$$
\langle\phi_s,\phi_t\rangle_{L^2}
=\int_0^1\mathbf1_{u\le s}\mathbf1_{u\le t}du
=\min(s,t),
$$

故 PSD。对 $0<t_1<t_2$，

$$
K=\begin{bmatrix}t_1&t_1\\t_1&t_2\end{bmatrix},
\qquad
\det K=t_1(t_2-t_1)>0.
$$

$\|k_t\|^2=k(t,t)=t$，故 $\|k_t\|=\sqrt t$。并且

$$
d_k(s,t)^2=s+t-2\min(s,t)=|s-t|,
\qquad
d_k(s,t)=\sqrt{|s-t|}.
$$

候选空间是 Cameron–Martin/Sobolev 型空间

$$
\mathcal H={f:f(0)=0, f\text{ absolutely continuous}, f'\in L^2[0,1]},
$$

配

$$
\langle f,g\rangle_{\mathcal H}=\int_0^1f'(u)g'(u)du.
$$

对 $k_t(s)=\min(t,s)$，其对 $s$ 的 weak/classical-a.e. derivative 是 $\mathbf1_{[0,t]}(s)$，所以

$$
\langle f,k_t\rangle_{\mathcal H}
=\int_0^tf'(u)du=f(t)-f(0)=f(t).
$$

这验证 reproducing property，也给 $|f(t)|\le\sqrt t\|f\|_{\mathcal H}$。

## B03 解答：KRR 与 GP 同均值

这里 $n=2$。由于 $y=(1,-1)^\top$ 是 $K$ 的 eigenvector，对应 eigenvalue $1-r$，

$$
\alpha=(K+2\lambda I)^{-1}y
=\frac1{1-r+2\lambda}
\begin{bmatrix}1\\-1\end{bmatrix}.
$$

因此

$$
\hat y=K\alpha
=\frac{1-r}{1-r+2\lambda}
\begin{bmatrix}1\\-1\end{bmatrix}.
$$

测试预测

$$
\hat f_*=(a,b)\alpha
=\frac{a-b}{1-r+2\lambda}.
$$

GP 取 $\sigma^2=2\lambda$ 时 posterior mean为 $k_*^\top(K+\sigma^2I)^{-1}y$，完全相同。Latent posterior variance为

$$
v_*=k(x_*,x_*)-k_*^\top(K+2\lambda I)^{-1}k_*.
$$

若要求 noisy observation variance，再加 $2\lambda$。KRR point predictor本身没有由此自动得到的 posterior variance。

## C01 解答：Moore–Aronszajn 构造

先取 formal finite sums的 vector space $V$，元素写成 $u=\sum_i a_i[x_i]$。定义

$$
[u,v]_k=\sum_{i,j}a_i\overline{b_j}k(x_i,z_j).
$$

Sesquilinearity由有限和直接得到，Hermitian symmetry来自 $k$ Hermitian；PSD 定义给 $[u,u]_k\ge0$。令 null space

$$
N=\{u\in V:[u,u]_k=0\}.
$$

Semidefinite Cauchy–Schwarz给 $|[u,v]_k|^2\le[u,u]_k[v,v]_k$，所以 $u\in N$ 时与所有 $v$ pairing为零。故 $[\cdot,\cdot]_k$ 在 quotient $V/N$ 上良定义并成为 inner product。

把 class $[x]+N$ 映成 section $k_x$；更一般地，$u=\sum_i a_i[x_i]$ 映成函数

$$
f_u(z)=\sum_i a_i k(x_i,z).
$$

若 $u-v\in N$，则

$$
|f_{u-v}(z)|^2=|[u-v,[z]]_k|^2
\le[u-v,u-v]_kk(z,z)=0,
$$

故函数表示良定义。并且

$$
\langle f_u,k_x\rangle=f_u(x).
$$

完成 $V/N$ 得 Hilbert space $\mathcal H_k$。对任意 pre-Hilbert Cauchy sequence $(f_m)$，

$$
|f_m(x)-f_l(x)|\le\sqrt{k(x,x)}\|f_m-f_l\|,
$$

所以点值 Cauchy并定义 completion element的函数值；evaluation norm不超过 $\sqrt{k(x,x)}$。Reproducing identity由 density连续延伸。

若同一 RKHS 有 kernels $k$ 和 $\tilde k$，则对任意 $x$、任意 $f$，

$$
\langle f,k_x-\tilde k_x\rangle=f(x)-f(x)=0.
$$

取 $f=k_x-\tilde k_x$ 得二者相同，故 kernel唯一。

若另有 feature map $\phi:\mathcal X\to\mathcal F$ 生成同一 kernel，定义

$$
U\left(\sum_i a_i\phi(x_i)\right)=\sum_i a_i k_{x_i}.
$$

两边 norm平方都等于 $\sum_{ij}a_i\overline{a_j}k(x_i,x_j)$，所以 $U$ 良定义且 isometry；延伸后把 $\overline{\operatorname{span}\phi(\mathcal X)}$ 等距映到 $\mathcal H_k$。$\mathcal F$ 中与 feature span正交的冗余方向不影响 kernel。

## C02 解答：广义表示定理

令 $S=\operatorname{span}\{r_1,ldots,r_m\}$。任意 $f$ 唯一分解为 $f=f_S+f_\perp$。Riesz representation给

$$
\ell_i(f_\perp)=\langle f_\perp,r_i\rangle=0,
$$

所以 $L$ 在 $f$ 与 $f_S$ 上相同，而

$$
\|f\|^2=\|f_S\|^2+\|f_\perp\|^2.
$$

若 $\Omega$ strictly increasing且 $f_\perp\ne0$，删除 $f_\perp$ 严格降低 objective，和 minimizer矛盾。因此每个 minimizer在 $S$ 中。

若 $\Omega$ 仅 nondecreasing，删除 $f_\perp$ 不增加 objective，所以从任一 minimizer可获得一个 $S$ 中 minimizer；但 plateau 允许其他 minimizer保留 $f_\perp$。

对 $\ell_i(f)=f(x_i)$，$r_i=k_{x_i}$。若 derivative evaluation $f\mapsto f'(x_i)$ bounded，其 Riesz representer为相应 kernel derivative（在足够 smooth且 convention一致时可写 $\partial_1k(x_i,\cdot)$ 或 $\partial_2$ 版本），因此表示基扩展为

$$
\{k(x_i,\cdot),\ \partial_1k(x_i,\cdot)}_{i=1}^n.
$$

非单调反例：取 loss恒为 $0$，令 $\Omega(r)=(r-1)^2$。若 $S=\{0\}$ 或很小，任何 norm为 $1$ 的 orthogonal vector都是 minimizer，却不在 $S$。所以 norm dependence本身不够，单调性是证明删除 orthogonal component的关键。

## C03 解答：KRR 全推导

表示定理给 $f=\sum_i\alpha_i k_{x_i}$，所以

$$
J(\alpha)=\frac1n\|K\alpha-y\|^2+\lambda\alpha^\top K\alpha.
$$

Gradient为

$$
\nabla J(\alpha)=\frac2nK(K\alpha-y)+2\lambda K\alpha
=\frac2nK[(K+n\lambda I)\alpha-y].
$$

取 $\alpha_*=(K+n\lambda I)^{-1}y$ 使 bracket为零。因 $K\succeq0$、$\lambda>0$，$K+n\lambda I\succ0$，该 linear system 的解唯一。若 $v\in\ker K$，则 $K(\alpha_*+v)=K\alpha_*$ 且 $(\alpha_*+v)^\top K(\alpha_*+v)=\alpha_*^\top K\alpha_*$，所以 coefficient objective 仍可能有冗余 minimizers；它们代表同一个函数。Objective作为 $f$ 的 functional含 strictly convex Hilbert norm平方与 convex square loss，故函数 minimizer唯一；canonical system选择其中一组唯一、稳定的 coefficients。

令 $K=U\operatorname{diag}(\kappa_j)U^\top$，则

$$
S_\lambda=K(K+n\lambda I)^{-1}
=U\operatorname{diag}\left(
\frac{\kappa_j}{\kappa_j+n\lambda}
\right)U^\top.
$$

因此

$$
\operatorname{df}(\lambda)=\operatorname{tr}S_\lambda
=\sum_j\frac{\kappa_j}{\kappa_j+n\lambda}.
$$

它是被保留 empirical directions 的软计数。

Label perturbation给

$$
\delta\alpha=(K+n\lambda I)^{-1}\delta y,
\qquad
\|\delta\alpha\|_2\le\frac1{n\lambda}\|\delta y\|_2.
$$

训练预测 perturbation为 $\delta\hat y=S_\lambda\delta y$，因 smoother eigenvalues在 $[0,1)$，

$$
\|\delta\hat y\|_2\le\|\delta y\|_2.
$$

数值上应 factor/solve而非形成 inverse，以降低 rounding和成本。Jitter是防止 factorization因微小数值非正定而失败的工程项；$\lambda$ 定义 statistical objective与bias–variance。它们虽都加 diagonal，却必须分别记录和调节。

## D01 解答：十二个错误命题

十二项均错：

1. 在 $\{0,1\}$ 上令 $K=\begin{bmatrix}1&2\\2&1\end{bmatrix}$，symmetric且diagonal正，但 eigenvalues为 $3,-1$。
2. Linear kernel可取 $x=1,z=-1$ 得 $k=-1$，仍 PSD。
3. 可修改一个从未出现点与其他点的 kernel values，使已测 Gram不变而新 Gram indefinite。
4. Strict PD只控制 finite signed point masses；characteristic要求整个 probability class injection，不能无条件推出。
5. Characteristic相对 measures，universal相对 function topology；没有“任意 function space”的 universal。
6. $L^2$ point evaluation一般不良定义/不 bounded。
7. Moore–Aronszajn只需非空 set和PSD kernel。
8. Mercer强展开还需 topology、measure、continuity/compactness等。
9. 表示定理假定 minimizer时给其形式；existence/uniqueness另需条件。
10. Infinite-dimensional GP sample paths常以概率一不在 covariance RKHS；RKHS更像 Cameron–Martin directions。
11. 新随机 features可能使 realized error上升；只有 expectation/high-probability趋势。
12. 每个固定 $t$ 的 Jacobian Gram PSD，但 gradients随参数变化，$\Theta_t$ 可漂移。

## D02 解答：非法相似度与修复

Squared-distance matrix为

$$
D^2=\begin{bmatrix}0&1&4\\1&0&1\\4&1&0\end{bmatrix},
$$

所以

$$
K_1=-D^2=
\begin{bmatrix}0&-1&-4\\-1&0&-1\\-4&-1&0\end{bmatrix}.
$$

取 $c=(1,0,1)^\top$ 得 $c^\top K_1c=-8<0$；取 $c=(1,-2,1)^\top$ 得 $c^\top K_1c=12>0$，故 indefinite。

令 $H=I-\mathbf1\mathbf1^\top/3$。若 points来自 Euclidean coordinates并令 centered coordinate vector $x_c=Hx$，classical multidimensional scaling identity给

$$
B=-\frac12HD^2H=x_cx_c^\top\succeq0.
$$

它是 centered coordinates的 Gram matrix。更高维时 $B=X_cX_c^\top$。

给当前 $K_1$ 加 $\tau I$ 且 $\tau\ge-\lambda_{\min}$ 会使该 finite matrix PSD，但它没有说明新测试点与训练点的 cross-kernel，也不构造全域 $k(x,z)$。它只是 finite matrix repair。

$k_2$ 可用 Bochner theorem：Gaussian $\kappa(h)=e^{-h^2/(2\ell^2)}$ 的 Fourier transform是 nonnegative Gaussian measure，所以是 continuous shift-invariant PSD kernel。也可用 power-series/tensor features构造。

Floating-point 下先：强制/检查 symmetry；核公式、dtype、overflow和distance计算；估计 negative eigenvalue相对 $\|K\|$ 与 solver tolerance；用高精度或独立 factorization复核；确认 kernel理论上合法。只有确认是 rounding-level noise后才用 minimal jitter或eigenvalue clipping，并记录改变量；显著负值应视为模型/实现错误。

## D03 解答：Bandwidth、centering 与泄漏

对互异样本，RBF $\ell\to0$ 时 $K\to I$：rank接近 $n$，训练点几乎独立记忆；KRR smoother接近 $(1+n\lambda)^{-1}I$，小 $\lambda$ 时接近插值。$\ell\to\infty$ 时 $K\to\mathbf1\mathbf1^\top$：rank趋近 $1$，只保留 constant direction；无 intercept/centering处理时可能只预测全局平均型信号。

Kernel PCA 要 center feature vectors，故用 $K_c=HKH$；否则第一主方向可能主要是 feature mean。HSIC 要测 centered cross-covariance，未center的 $KL$ trace混入 means。测试点 centering必须使用训练 feature mean：对 test–train kernel vector $k_*$，应用由训练均值导出的 cross-centering公式，不能用测试集自身全局统计，更不能把测试数据混入训练 centering。

Bandwidth若看了测试 labels/metrics后选择，测试集已经参与 model selection；之后同一测试性能不再是独立泛化估计。应用 nested CV、validation split或重新保留 untouched test。

Jitter在 linear algebra层；$\lambda$ 在 statistical objective层；early stopping在 optimization/implicit regularization层。三者可能相互作用但语义不同。Gram condition number只描述某一数值线性系统的敏感性，不能单独推出 good kernel choice、calibration、generalization、causal validity或characteristic性。

## E01 解答：MMD/HSIC 合同

由 $\mu_P=\mathbb E k_X$，

$$
\|\mu_P-\mu_Q\|^2
=\mathbb E k(X,X')+\mathbb E k(Y,Y')-2\mathbb E k(X,Y),
$$

其中 $X,X'$ iid $P$，$Y,Y'$ iid $Q$。

Biased estimator保留 diagonal：

$$
\widehat{\mathrm{MMD}}_b^2
=\frac1{m^2}\sum_{i,j}k(x_i,x_j)
+\frac1{n^2}\sum_{i,j}k(y_i,y_j)
-\frac2{mn}\sum_{i,j}k(x_i,y_j).
$$

它是 empirical embeddings距离平方，必非负但有有限样本bias。Unbiased U-statistic删同样本项：

$$
\widehat{\mathrm{MMD}}_u^2
=\frac1{m(m-1)}\sum_{i\ne j}k(x_i,x_j)
+\frac1{n(n-1)}\sum_{i\ne j}k(y_i,y_j)
-\frac2{mn}\sum_{i,j}k(x_i,y_j).
$$

它可因 sampling fluctuation为负。Paired sample biased HSIC为

$$
\widehat{\mathrm{HSIC}}_b=N^{-2}\operatorname{tr}(KHLH),
\qquad H=I-\mathbf1\mathbf1^\top/N.
$$

MMD反向需要 $k$ 在指定 measure class characteristic；HSIC反向需要 product/joint embedding足够rich，常由对边际 domains选 characteristic/universal kernels并满足相应条件保证。

IID null下，两样本检验可随机置换 pooled sample labels；independence test可置换一侧 pairing，重复计算 statistic形成 empirical null。Time-series中 arbitrary permutation破坏 autocorrelation并产生错误 null；需 block permutation、wild bootstrap或针对依赖结构的方法。

报告至少包括：kernel公式、normalization与bandwidth选择是否嵌套；biased/unbiased statistic；iid/paired/time-dependent assumptions；permutations数与随机种子；p-value/calibration流程；sample sizes；effect statistic与不确定性；多重比较；预处理和缺失值；是否用测试数据调参。

## E02 解答：Exact、Nyström 与 RFF

Dense exact Gram memory $O(n^2)$ 不可行。若 kernel matvec不借助特殊结构，单次仍 $O(n^2d)$，iterative solve即使不存矩阵也可能过慢；若有 fast multipole/structured approximation，才可能成为 exact-like方案。Nyström存 $K_{nm}$，memory $O(nm)$，build约 $O(nmd)$，solve/feature化常见 $O(nm^2+m^3)$ 或依实现降低。RFF build $Z$ 约 $O(ndD)$、memory可 streaming到 $O(D^2)$ sufficient statistics或 minibatch，线性 ridge直接在 $D$ 维求解。

Nyström audit：uniform/k-means/leverage landmark策略；landmarks只能由training选；扫描 $m$；报告 $K_{mm}$ spectrum、jitter/$\lambda$、effective rank、pseudoinverse threshold；多seed/selection variability；held-out blocks上的 spectral/Frobenius或regularized solve error。

RFF audit：RBF 对应 $\omega\sim\mathcal N(0,\ell^{-2}I)$；$b\sim U[0,2\pi]$；$\sqrt{2/D}$ normalization；训练/测试复用同一 features；记录 seed、$D$、dtype；多seed报告 kernel error均值/分位数和 downstream variation；检查 bandwidth与input scaling。

双重验收可在未用于选近似的 held-out points 上比较 exact kernel entries/submatrices的 relative Frobenius、max、spectral proxy和PSD；同时在独立 validation/test 上比较 risk、calibration、wall time、peak memory。Kernel Frobenius error对所有 eigendirections平均，而 prediction更依赖 labels、regularization及 task-relevant directions，所以最小 Frobenius error不保证最小 risk。

规则示例：$D$ 可容纳且需 streaming/SGD时优先RFF；effective rank低且可存 $nm$ 时Nyström；存在快速 exact matvec且高精度要求强时迭代exact-like。Budget扩大时同时增 $m/D$ 并检查 approximation error是否已低于 sampling和solver error；不要把资源全花在已经不主导总误差的一层。

## E03 解答：Linear Attention 与 NTK

若 $a(q,k)=\phi(q)^\top\phi(k)$，对同一 token set形成 $\Phi\Phi^\top\succeq0$，并 symmetric。若 $\phi\ne\varphi$，cross matrix $\Phi(Q)\Psi(K)^\top$ 一般 rectangular或非 symmetric，不能称同一域 PSD Gram；它仍可用于 factorized computation。

设 exact positive weights $w_j$、approximations $\tilde w_j$，输出

$$
o=\frac{\sum_jw_jv_j}{s},\quad s=\sum_jw_j,
\qquad
\tilde o=\frac{\sum_j\tilde w_jv_j}{\tilde s}.
$$

误差 bound需要 $s,\tilde s$ 有正 lower bound，否则很小 affinity error会被 denominator放大；还需 value norms和 numerator total error。Causal mask使每个 query只聚合 prefix；仍可通过 prefix sums维护 $\sum_{j\le i}\varphi(k_j)v_j^\top$ 与 $\sum_{j\le i}\varphi(k_j)$，但 arbitrary mask未必有这种递推结构。

固定 $t$ 和 samples $x_i$，令 row-feature $g_i=\nabla_\theta f_{\theta_t}(x_i)$。则

$$
c^\top\Theta_tc
=\sum_{ij}c_ic_jg_i^\top g_j
=\left\|\sum_ic_ig_i\right\|^2\ge0.
$$

因此 empirical NTK PSD。要把训练等价为固定 kernel regression，还需明确 infinite-width limit、parameterization与初始化、learning-rate/time scaling、loss和limit交换，并证明 $\Theta_t$ 接近 deterministic $\Theta_0$。Finite width、large feature motion、normalization和optimizer可破坏近似。

实验应同时记录：

1. Kernel drift $\|\Theta_t-\Theta_0\|_F/\|\Theta_0\|_F$，最好加 spectral proxy；
2. Linearization gap $\|f_{\theta_t}(X)-[f_{\theta_0}(X)+J_0(\theta_t-\theta_0)]\|/\|f_{\theta_t}(X)\|$；
3. Train/test task loss 与 predictions差异，并与用固定 $\Theta_0$ 的 kernel dynamics对照。

扫描 width、learning rate和训练时间；多 seed报告。即使 task curves接近，也不能省略 kernel drift；即使 drift小，也不能自动推出 generalization相同。
