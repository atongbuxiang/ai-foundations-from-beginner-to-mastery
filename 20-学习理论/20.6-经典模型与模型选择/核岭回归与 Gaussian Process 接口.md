---
type: theorem
status: draft
area: [learning-theory/kernel-ridge, gaussian-processes, spectral-regularization, uncertainty]
aliases: [Kernel Ridge Regression Theory, KRR GP Equivalence, Gaussian Process Regression Interface]
node_id: LT-46
prerequisites: ["[[正定核、RKHS 与表示定理]]", "[[线性回归的统计学习理论]]", "[[多元高斯分布]]", "[[协方差、相关性与条件期望]]", "[[条件概率、全概率与 Bayes 公式]]"]
related: ["[[支持向量机、最大间隔与核方法]]", "[[PCA 的统计估计与主子空间风险]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]", "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
sources: ["[[S-2006-Rasmussen-Williams-GPML]]", "[[S-2007-Caponnetto-DeVito-KRR-Rates]]", "[[S-2009-Hastie-Tibshirani-Friedman-ESL]]"]
exercises: ["[[习题 - 核岭回归与 Gaussian Process 接口]]"]
solutions: ["[[解答 - 核岭回归与 Gaussian Process 接口]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-krr-gp-shared-mean-contract-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 核岭回归与 Gaussian Process 接口

> [!abstract] 本章主问题
> 给定 PSD kernel \(k\)，核岭回归（KRR）与 Gaussian-process regression（GPR）都会出现
>
> $$
> k_x^T(K+cI)^{-1}y.
> $$
>
> 但相同 linear algebra 不等于相同 statistical theory：
>
> - KRR 把未知 regression function视为固定对象，用 empirical squared loss与 RKHS norm regularization定义 estimator；
> - GP 把函数值视为 joint Gaussian random variables，用 prior covariance与 observation likelihood定义 posterior distribution；
> - 匹配 normalization 后，KRR estimator等于 GP posterior mean；
> - GP 还给 posterior covariance、joint samples与 marginal likelihood，但这些 uncertainty statements依 prior、noise与 hyperparameter model；
> - KRR 的 frequentist risk则依 covariance-operator spectrum、target smoothness/source condition、noise与 \(\lambda_n\)。
>
> 本章把 finite Gram system、population operator、Bayesian posterior与 computation分成四层。

> [!question] 初学者读完必须能回答
> 1. representer theorem怎样把无限维 KRR变成 \(n\) 维 linear system？
> 2. \(K+n\lambda I\) 中的 \(n\) 从哪里来？
> 3. kernel eigenvalue shrinkage与 effective degrees of freedom是什么？
> 4. KRR 与 GP posterior mean在什么尺度对应？
> 5. posterior covariance为什么不是无条件 frequentist error bar？
> 6. jitter、noise variance、ridge与 low-rank approximation分别改变哪一层？

## 一、学习目标

1. 从 RKHS regularized ERM推导 finite representer expansion；
2. 推导 Gram coefficient system与 prediction formula；
3. 用 smoother matrix、eigendecomposition解释 bias/variance与 effective dimension；
4. 推导 fixed-hyperparameter KRR LOOCV shortcut；
5. 建立 population covariance operator与 source/capacity条件；
6. 从 joint Gaussian conditioning推导 GP posterior mean/covariance；
7. 精确对齐 \(n\lambda=\sigma^2/\tau^2\)；
8. 区分 posterior uncertainty、frequentist coverage与 model misspecification；
9. 分析 marginal likelihood、CV与 adaptive hyperparameter selection；
10. 审计 Cholesky、jitter、Nyström、random features与 inducing approximations。

## 二、对象合同

数据：

$$
S=\{(x_i,y_i)\}_{i=1}^n,
\qquad
y_i\in\mathbb R.
$$

PSD kernel：

$$
k:\mathcal X\times\mathcal X\to\mathbb R,
$$

对应 RKHS \(\mathcal H_k\)。Gram matrix：

$$
K_{ij}=k(x_i,x_j).
$$

test kernel vector：

$$
k_x
=
[k(x_1,x),\ldots,k(x_n,x)]^T.
$$

这里 \(k_x\in\mathbb R^n\) 是有限 vector；RKHS section \(k(x,\cdot)\in\mathcal H_k\) 是函数。语境中必须区分。

## 三、Kernel Ridge Regression

采用 mean-loss convention：

$$
\boxed{
\widehat f_\lambda
\in
\arg\min_{f\in\mathcal H_k}
\left{
\frac1n\sum_{i=1}^n
(y_i-f(x_i))^2
+\lambda\|f\|_{\mathcal H_k}^2
\right}.}
$$

\(\lambda>0\) 时 RKHS norm平方提供 strong convexity，\(\widehat f_\lambda\) 作为 Hilbert-space element唯一。

### 3.1 为什么不直接在所有函数中拟合

若只最小化 training squared error，任何能插值 finite sample 的函数都同样好；未观察位置没有定义。RKHS norm选择与 kernel geometry相容的低范数 extension，是 explicit inductive bias。

## 四、Representer Theorem 推导

令 sample span：

$$
\mathcal S
=
\operatorname{span}
\{k(x_1,\cdot),\ldots,k(x_n,\cdot)\}.
$$

任意 \(f\in\mathcal H_k\) 可正交分解：

$$
f=f_\parallel+f_\perp,
\qquad
f_\parallel\in\mathcal S,
\quad
f_\perp\perp\mathcal S.
$$

reproducing property给

$$
f_\perp(x_i)
=
\langle f_\perp,k(x_i,\cdot)\rangle
=0.
$$

所以 empirical loss只看 \(f_\parallel\)。同时

$$
\|f\|_{\mathcal H_k}^2
=
\|f_\parallel\|^2
+\|f_\perp\|^2.
$$

若 \(f_\perp\ne0\)，删掉它不改变 fit却严格降低 penalty。因此 minimizer满足

$$
\boxed{
\widehat f_\lambda(\cdot)
=
\sum_{j=1}^n
\alpha_j k(x_j,\cdot).}
$$

无限维优化被压到 finite sample span，但这不代表原 RKHS只有 \(n\) 维。

## 五、Finite Gram Objective

对 \(f=\sum_j\alpha_jk(x_j,\cdot)\)：

$$
f(X)=K\alpha,
$$

且

$$
\|f\|_{\mathcal H_k}^2
=
\alpha^TK\alpha.
$$

因此

$$
J(\alpha)
=
\frac1n\|y-K\alpha\|_2^2
+\lambda\alpha^TK\alpha.
$$

gradient：

$$
\nabla_\alpha J
=
\frac2nK(K\alpha-y)
+2\lambda K\alpha.
$$

normal condition：

$$
K[(K+n\lambda I)\alpha-y]=0.
$$

一个 canonical coefficient solution是

$$
\boxed{
\widehat\alpha
=(K+n\lambda I)^{-1}y.}
$$

因为 \(K\succeq0\) 且 \(\lambda>0\)，\(K+n\lambda I\succ0\)。prediction：

$$
\boxed{
\widehat f_\lambda(x)
=
k_x^T(K+n\lambda I)^{-1}y.}
$$

### 5.1 为什么有 \(n\lambda\)

它来自 mean squared loss的 \(1/n\)。若 objective写成

$$
\sum_i(y_i-f(x_i))^2
+\lambda_{\rm sum}\|f\|^2,
$$

linear system是

$$
K+\lambda_{\rm sum}I,
$$

并有

$$
\lambda_{\rm sum}=n\lambda.
$$

比较论文/library hyperparameters前必须对齐 convention。

## 六、图解：同一 Mean、不同合同

先回答：**为什么中栏的同一个 inverse不能证明右栏的 GP uncertainty自动具有 frequentist coverage？**

![[00-知识库管理/_assets/figures/learning-theory/fig-krr-gp-shared-mean-contract-v2.svg|900]]

> [!figure] 图 20.6.6｜KRR 谱滤波、GP 共享均值公式与不确定性边界
> 左栏把 Gram eigenvalues经过 \(\mu_j/(\mu_j+n\lambda)\) shrinkage并定义 effective dimension；中栏对齐 mean-loss KRR 与 \(n\lambda=\sigma^2/\tau^2\) 的 GP posterior mean；右栏列出 GP 多出的 posterior covariance、marginal likelihood与 joint uncertainty，并把 model misspecification、jitter与低秩误差分开。来源：依据 GPML、Caponnetto–De Vito 与本库 RKHS 节点独立绘制；确定性 SVG，由 [[plot_classical_models_ensemble_v2.py]] 生成。

**怎样读图。** shared Gram inverse是代数桥；KRR从 deterministic regularization出发，GP从 prior–likelihood conditioning出发。只有同时声明 loss normalization、prior amplitude与 noise variance，才可匹配 regularization constant。

**图没有证明什么。** 它没有证明真实函数是 GP sample、GP sample path属于其 covariance RKHS、credible interval有 nominal frequentist coverage、marginal likelihood一定选到 deployment-optimal kernel，或 low-rank approximation只带来计算误差而不改变统计结果。

## 七、Smoother Matrix

training fitted values：

$$
\widehat y
=K(K+n\lambda I)^{-1}y.
$$

定义

$$
\boxed{
S_\lambda
=K(K+n\lambda I)^{-1}.}
$$

这是 linear smoother：

$$
\widehat y=S_\lambda y.
$$

与 OLS hat matrix不同，\(S_\lambda\) 通常不是 idempotent：

$$
S_\lambda^2\ne S_\lambda.
$$

## 八、Finite-Sample Spectral Filter

令

$$
K=U\operatorname{diag}(\mu_1,\ldots,\mu_n)U^T,
\qquad
\mu_j\ge0.
$$

则

$$
S_\lambda
=
U\operatorname{diag}
\left(
\frac{\mu_j}{\mu_j+n\lambda}
\right)U^T.
$$

filter factor：

$$
\boxed{
s_j(\lambda)
=
\frac{\mu_j}{\mu_j+n\lambda}.}
$$

- \(\mu_j\gg n\lambda\)：direction大体保留；
- \(\mu_j\ll n\lambda\)：direction强烈压缩；
- \(\mu_j=0\)：training fitted component为零。

KRR不是“所有 directions统一乘一个常数”，而是 kernel spectrum中的 adaptive shrinkage。

## 九、Effective Degrees of Freedom

定义

$$
\boxed{
\operatorname{df}(\lambda)
=
\operatorname{tr}(S_\lambda)
=
\sum_{j=1}^n
\frac{\mu_j}{\mu_j+n\lambda}.}
$$

它是 smooth effective dimension：

- \(\lambda\to\infty\)，df趋近零；
- \(\lambda\downarrow0\)，df趋近 \(\operatorname{rank}(K)\)；
- 不一定是整数；
- 依 data locations 与 kernel hyperparameters。

df可用于 covariance/optimism/GCV接口，但不是无条件“自由 parameter个数”。

## 十、Fixed-Design Bias 与 Variance

给定 inputs，假设

$$
y=f_0(X)+\varepsilon,
\qquad
E[\varepsilon\mid X]=0,
\quad
\operatorname{Cov}(\varepsilon\mid X)=\sigma^2I.
$$

training fitted mean：

$$
E[\widehat y\mid X]
=S_\lambda f_0(X).
$$

bias vector：

$$
(S_\lambda-I)f_0(X).
$$

covariance：

$$
\boxed{
\operatorname{Cov}(\widehat y\mid X)
=
\sigma^2S_\lambda^2.}
$$

在 eigen-direction \(u_j\)：

- signal bias multiplier是 \(s_j-1\)；
- noise variance multiplier是 \(\sigma^2s_j^2\)。

这解释 regularization trade-off，但不证明 test risk随 \(\lambda\) 是单 U 形。

## 十一、LOOCV Shortcut

对 fixed kernel与 fixed \(\lambda\)，linear smoother的 leave-one-out residual：

$$
\boxed{
y_i-\widehat y_i^{(-i)}
=
\frac{y_i-\widehat y_i}{1-S_{\lambda,ii}}.}
$$

于是 squared LOOCV：

$$
\widehat R_{\rm LOO}(\lambda)
=
\frac1n\sum_i
\left(
\frac{e_i}{1-S_{ii}}
\right)^2.
$$

边界：

- formula针对每个 fixed \(\lambda\)；
- 用同一 LOOCV curve选择最小 \(\lambda\) 后，minimum score有 selection optimism；
- kernel bandwidth/preprocessing也必须 leave-one-out/nested；
- dependent/group/time data不能直接逐 row删除；
- \(S_{ii}\approx1\) 时 residual被强烈放大。

## 十二、Population Covariance Operator

定义 section

$$
k_X=k(X,\cdot)\in\mathcal H_k.
$$

若 \(E[k(X,X)]<\infty\)，定义 covariance operator：

$$
\boxed{
Tf
=
E[
\langle f,k_X\rangle_{\mathcal H_k}
k_X
]
=E[f(X)k_X].}
$$

定义

$$
g=E[Yk_X].
$$

population regularized objective：

$$
E(Y-f(X))^2
+\lambda\|f\|_{\mathcal H_k}^2.
$$

first-order condition：

$$
\boxed{
(T+\lambda I)f_\lambda=g.}
$$

所以

$$
f_\lambda=(T+\lambda I)^{-1}g.
$$

finite KRR是 sample operator对这条 population inverse problem的 regularized approximation。

## 十三、Population Spectral Bias

设

$$
T e_j=\rho_j e_j,
\qquad
\rho_j\downarrow0.
$$

若 regression target在相应 closure中展开：

$$
f_\rho=\sum_j\theta_j e_j,
$$

population ridge filter近似为

$$
f_\lambda
=
\sum_j
\frac{\rho_j}{\rho_j+\lambda}
\theta_j e_j.
$$

小 eigenvalue directions被压缩。bias大小取决于 \(\theta_j\) 与 \(\rho_j\) 的 alignment，不只取决于 eigenvalue decay。

### 13.1 Source Condition

一种 smoothness/target alignment假设：

$$
f_\rho=T^r v
$$

对某 \(r>0\) 与 bounded \(v\)。越大的 \(r\) 表示 target在小-eigenvalue directions衰减更快，regularization bias更易控制。

具体 rate依：

- source exponent convention；
- risk用 RKHS norm还是 \(L^2(P_X)\)；
- eigenvalue/capacity condition；
- noise tails；
- \(\lambda_n\) scaling。

不能只写“target smooth，所以 rate为某幂”而省略 metric与 operator。

## 十四、Population Effective Dimension

定义

$$
\boxed{
\mathcal N(\lambda)
=
\operatorname{Tr}
[T(T+\lambda I)^{-1}]
=
\sum_j
\frac{\rho_j}{\rho_j+\lambda}.}
$$

在适当 bounded-kernel/noise/concentration条件下，stochastic variance常呈

$$
\frac{\sigma^2\mathcal N(\lambda)}n
$$

型量级，加上 sample-operator perturbation terms。选择 \(\lambda_n\) 是在 spectral bias与 effective-dimension variance之间平衡。

这只是 rate architecture；具体 theorem由[[S-2007-Caponnetto-DeVito-KRR-Rates]]及其修正条件承担。

## 十五、Gaussian-Process Prior

设 latent function prior：

$$
f\sim\operatorname{GP}(0,\tau^2k).
$$

意味着任意有限 points的 vector

$$
[f(x_1),\ldots,f(x_m)]^T
$$

joint Gaussian，covariance为 \(\tau^2K\)。observation model：

$$
y_i=f(x_i)+\varepsilon_i,
\qquad
\varepsilon_i\overset{\rm iid}{\sim}
\mathcal N(0,\sigma^2).
$$

于是

$$
y\sim\mathcal N(0,\tau^2K+\sigma^2I).
$$

## 十六、GP Posterior 推导

对 test point \(x\)，joint distribution：

$$
\begin{bmatrix}
y\\ f(x)
\end{bmatrix}
\sim
\mathcal N\left(
0,
\begin{bmatrix}
\tau^2K+\sigma^2I & \tau^2k_x\\
\tau^2k_x^T & \tau^2k(x,x)
\end{bmatrix}
\right).
$$

Gaussian conditioning给 posterior mean：

$$
\begin{aligned}
m_n(x)
&=\tau^2k_x^T
(\tau^2K+\sigma^2I)^{-1}y\\
&=
\boxed{
k_x^T
\left(K+\frac{\sigma^2}{\tau^2}I\right)^{-1}y.}
\end{aligned}
$$

posterior covariance：

$$
\boxed{
c_n(x,x')
=
\tau^2
\left[
k(x,x')
-k_x^T
\left(K+\frac{\sigma^2}{\tau^2}I\right)^{-1}
k_{x'}
\right].}
$$

fresh response predictive variance还要加 \(\sigma^2\)：

$$
\operatorname{Var}(Y(x)\mid S)
=c_n(x,x)+\sigma^2.
$$

latent-function uncertainty与 observation noise不可混写。

## 十七、KRR–GP Mean 对应

KRR mean-loss formula：

$$
\widehat f_\lambda(x)
=k_x^T(K+n\lambda I)^{-1}y.
$$

GP posterior mean：

$$
m_n(x)
=k_x^T
\left(K+\frac{\sigma^2}{\tau^2}I\right)^{-1}y.
$$

所以匹配条件：

$$
\boxed{
n\lambda
=
\frac{\sigma^2}{\tau^2}.}
$$

若 KRR用 sum-loss，则匹配的是

$$
\lambda_{\rm sum}
=
\frac{\sigma^2}{\tau^2}.
$$

### 17.1 相同的是什么

- posterior/estimator mean function；
- finite Gram linear solve；
- kernel hyperparameters进入方式；
- eigenvalue filter。

### 17.2 不同的是什么

- KRR：未知 \(f_0\) fixed，probability来自 repeated samples；
- GP：\(f\) 在 prior下 random，posterior conditional on observed data；
- KRR risk由 \(P_{X,Y}\)、operator与 \(\lambda_n\) 分析；
- GP uncertainty由 prior/likelihood/hyperparameters定义；
- GP有 joint covariance/samples/marginal likelihood，KRR objective本身没有；
- KRR confidence sets需要额外 frequentist construction。

## 十八、GP Sample Path 不等于 RKHS Element

covariance kernel的 RKHS是 GP measure的 Cameron–Martin geometry。对常见 infinite-dimensional GP，drawn sample path往往不属于该 RKHS（概率一），尽管 kernel相同。

直觉：Mercer coordinates中 GP draw有随机 coefficients，其 RKHS norm会要求按 inverse eigenvalues加权平方和，通常发散。

因此不能写：

> “GP prior从 \(\mathcal H_k\) 中均匀抽函数。”

无限维 Hilbert ball上也不存在这种 uniform distribution。KRR norm与 GP prior仍紧密相关，但对象不是“sample path norm等于 regularizer”这么简单。

## 十九、Posterior Credible 与 Frequentist Coverage

GP credible interval：

$$
m_n(x)
\pm
z_{1-\alpha/2}
\sqrt{c_n(x,x)}
$$

是在 declared GP model内的 posterior probability statement。

要获得 frequentist coverage

$$
P_{f_0,S}
\{f_0(x)\in I_n(x)\}
\approx1-\alpha,
$$

需额外研究：

- true \(f_0\) 与 prior smoothness匹配；
- hyperparameter estimation；
- fixed/random design；
- pointwise或 simultaneous coverage；
- undersmoothing/bias correction；
- noise/model misspecification。

posterior variance小可能只是 kernel过平滑或 noise低估，不自动说明真实 error小。

## 二十、Marginal Likelihood

令 hyperparameters \(\theta\) 控制 kernel、amplitude与 noise：

$$
C_\theta
=
\tau^2K_\theta+\sigma^2I.
$$

log marginal likelihood：

$$
\boxed{
\log p(y\mid X,\theta)
=
-\frac12y^TC_\theta^{-1}y
-\frac12\log\det C_\theta
-\frac n2\log(2\pi).}
$$

三项常解释为：

1. data fit；
2. covariance volume/complexity；
3. normalization constant。

### 20.1 Empirical Bayes 边界

若

$$
\widehat\theta
=
\arg\max_\theta\log p(y\mid X,\theta),
$$

然后条件于 \(\widehat\theta\) 报 posterior，通常忽略 hyperparameter uncertainty。objective也可能 multimodal；local optimum、parameter bounds与 initialization影响结果。

marginal likelihood optimization不是 distribution-free test-risk theorem。CV与 marginal likelihood选择的是不同 criterion。

## 二十一、Kernel Design 与 Identifiability

kernel编码：

- smoothness；
- length scale；
- periodicity；
- additivity/interactions；
- invariance；
- nonstationarity；
- input metric。

amplitude \(\tau^2\)、noise \(\sigma^2\) 与 length scale在 finite data上可能 trade off。输入没有 standardize时，各 coordinate length scale不可比较。

deep kernel learning中 \(k_\theta(\phi_\omega(x),\phi_\omega(z))\) 的 representation也由 data学习；classical fixed-kernel posterior不包含 \(\omega\) 的完整 selection uncertainty。

## 二十二、Numerical Linear Algebra

核心 solve：

$$
(K+cI)\alpha=y,
\qquad c>0.
$$

### 22.1 Cholesky

对 SPD matrix优先 Cholesky：

$$
K+cI=LL^T.
$$

成本：

$$
O(n^3)\text{ time},
\qquad
O(n^2)\text{ memory}.
$$

不要显式形成 inverse；solve \(Lz=y\)、\(L^T\alpha=z\)。log determinant：

$$
\log\det(K+cI)
=2\sum_i\log L_{ii}.
$$

### 22.2 Jitter 与 Noise

数值 jitter：

$$
K\leftarrow K+\epsilon_{\rm jit}I
$$

可改善 Cholesky stability。它代数上像增加 diagonal noise/ridge，但语义可能不同：

- statistical noise是 observation model parameter；
- ridge是 estimator regularization；
- jitter是 floating-point stabilization。

如果 jitter大到影响 predictions/uncertainty，就已改变有效模型，必须报告并做敏感性分析。

### 22.3 Condition Number

RBF large length scale、duplicated inputs或 tiny noise会使 Gram nearly singular。仅增加 jitter可能掩盖 duplicate/conflicting observations或 kernel misspecification。

## 二十三、Large-Scale Approximations

### 23.1 Nyström

选择 \(m\ll n\) 个 landmarks，用 low-rank approximation：

$$
K\approx K_{nm}K_{mm}^\dagger K_{mn}.
$$

误差依 landmark sampling、spectrum与 regularization。

### 23.2 Random Features

构造 \(z(x)\in\mathbb R^D\) 使

$$
z(x)^Tz(x')\approx k(x,x').
$$

然后做 finite-dimensional ridge。新增 randomness来自 feature draw；需要把 approximation variance与 data variance分开。

### 23.3 Inducing Variables

GP使用 inducing locations/variables近似 joint covariance与 posterior。不同 variational/sparse objectives不只改变速度，也可能改变 posterior uncertainty与 hyperparameter learning。

### 23.4 Iterative Solves

conjugate gradient配合 matrix–vector product可避免 dense factorization，但 stopping residual、preconditioner与 stochastic log-det approximation进入 error budget。

## 二十四、Interpolation 与 Ridgeless Limit

当 \(\lambda\downarrow0\) 且 \(K\) invertible：

$$
\widehat f_0(x)
=k_x^TK^{-1}y
$$

插值 training labels。是否泛化取决于 kernel spectrum、target alignment、noise与 sample geometry；“插值必过拟合”与“minimum-norm插值必 benign”都不是普遍定理。

GP中 \(\sigma^2\downarrow0\) 给 noiseless interpolation posterior，但若 observations含 noise，这是假设错置；posterior variance在 training points归零也不代表真实 measurement uncertainty消失。

## 二十五、现代 AI 接口

### 25.1 Neural Tangent Kernel

某些 infinite-width/lazy-training regime中，network outputs近似 kernel gradient dynamics；squared-loss limit可连接 kernel regression。有限宽、feature learning、finite time与 optimizer会偏离 fixed NTK。不能把一次 NTK fit当完整 deep-learning theory。

### 25.2 Frozen Representation + KRR/GP Head

在 \(\phi_\omega(x)\) 上定义 RBF/linear kernel，可用于 few-shot regression与 uncertainty head。但 representation selection、pretraining data与 distribution shift不包含在固定 \(K\) 的 posterior covariance内。

### 25.3 Bayesian Optimization / Active Learning

acquisition依 posterior mean与variance。如果 kernel misspecified或 hyperparameters overfit，小 posterior variance会导致错误 exploitation。安全系统应审计 coverage、constraint violation与 shift，而非只画漂亮 uncertainty band。

### 25.4 Structured Kernels

string、graph、sequence kernel必须先满足 PSD；learned similarity不自动合法。将 indefinite matrix投影到 PSD cone会改变 distances、rank与 predictions。

## 二十六、常见误区

> [!warning] 误区 1：KRR 与 GP 是同一个模型
> 只在尺度匹配后 mean公式相同；probability space、uncertainty与risk解释不同。

> [!warning] 误区 2：GP sample 一定属于 covariance RKHS
> 常见 infinite-dimensional GP sample path几乎必然不在其 Cameron–Martin RKHS。

> [!warning] 误区 3：posterior variance就是实际 squared error
> 它是 model-conditional uncertainty；coverage需额外条件与验证。

> [!warning] 误区 4：加 jitter只是无影响实现细节
> 足够大的 jitter改变 effective noise/ridge与 posterior。

> [!warning] 误区 5：kernel PSD，所以适合任务
> PSD只保证 Hilbert geometry；bandwidth、invariance与 target alignment仍可能错误。

> [!warning] 误区 6：low-rank只减少计算量
> approximation改变 Gram spectrum、mean、variance与 hyperparameter objective。

## 二十七、验收清单

1. kernel是否全域 PSD？
2. KRR loss用 mean还是 sum？
3. \(K+n\lambda I\) 的 scale是否正确？
4. intercept/mean function如何处理？
5. Gram spectrum与 effective df怎样？
6. target/source condition与 risk metric是什么？
7. GP prior amplitude与 noise variance分别是什么？
8. KRR–GP match是否满足 \(n\lambda=\sigma^2/\tau^2\)？
9. latent variance与 predictive response variance是否分开？
10. hyperparameters用 marginal likelihood、CV还是 full Bayes？
11. selection uncertainty是否报告？
12. posterior interval是否验证 coverage？
13. Cholesky condition、jitter与 solver residual怎样？
14. low-rank/random-feature approximation误差怎样？
15. representation/kernel在 deployment shift下是否仍匹配？

## 二十八、小结

KRR–GP 接口的完整逻辑链：

1. PSD kernel定义 RKHS geometry；
2. representer theorem把 KRR压到 sample span；
3. mean-loss convention产生 \(K+n\lambda I\)；
4. smoother spectrum用 \(\mu_j/(\mu_j+n\lambda)\) filter directions；
5. trace给 finite effective df，population operator给 \(\mathcal N(\lambda)\)；
6. source condition与 eigenvalue decay共同控制 bias–variance rate；
7. GP prior与 Gaussian noise通过 conditioning给 posterior mean/covariance；
8. \(n\lambda=\sigma^2/\tau^2\) 时 mean与 KRR相同；
9. 同一 mean不等于同一 probability model或 uncertainty guarantee；
10. GP sample path与 covariance RKHS element不可等同；
11. marginal likelihood、CV、full Bayes是不同 hyperparameter procedures；
12. jitter、noise、ridge与 approximation是四种不同干预；
13. Cholesky/iterative/low-rank computation必须进入误差账本；
14. deep kernel、NTK与 uncertainty deployment还含 representation与 shift层。

真正掌握这一章，是能看到 \((K+cI)^{-1}\) 时立刻追问：\(c\) 来自哪里、概率对象是什么、spectrum过滤了什么、uncertainty依什么、计算近似改变了什么。

## 来源与延伸

- [[S-2006-Rasmussen-Williams-GPML]]：GP regression、covariance、marginal likelihood与 RKHS/regularization关系；
- [[S-2007-Caponnetto-DeVito-KRR-Rates]]：KRR population operator、effective dimension与 rate架构，连同 correction caveat；
- [[S-2009-Hastie-Tibshirani-Friedman-ESL]]：kernel smoothing、ridge与model assessment；
- [[正定核、RKHS 与表示定理]]：PSD、Moore–Aronszajn、representer、Mercer、Nyström与随机特征数学底座；
- [[线性回归的统计学习理论]]：fixed/random design、ridge与 prediction-risk坐标；
- [[概率校准、Proper Scoring Rule 与可靠性图]]：从 posterior/predictive distribution进入概率评价。
