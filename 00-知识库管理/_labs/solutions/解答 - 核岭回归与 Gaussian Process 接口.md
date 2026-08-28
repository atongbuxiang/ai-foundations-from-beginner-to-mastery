---
type: solution
status: draft
area: [learning-theory/kernel-ridge, gaussian-processes]
topic: "[[核岭回归与 Gaussian Process 接口]]"
exercise: "[[习题 - 核岭回归与 Gaussian Process 接口]]"
prerequisites: ["[[核岭回归与 Gaussian Process 接口]]"]
related: ["[[正定核、RKHS 与表示定理]]", "[[多元高斯分布]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - 核岭回归与 Gaussian Process 接口

> [!warning] 解题原则
> 看到 \(K+cI\) 先追问 loss normalization与 probability model。相同 inverse可服务于 deterministic regularization、Bayesian conditioning或 numerical stabilization。

## A. 识别与复述

### LT-KGP-A01

- KRR estimator：固定未知 data law下，\(S\mapsto\widehat f_\lambda\) 的 data-dependent point estimate；
- GP prior draw：观测前从 declared stochastic process得到的 random function；
- GP posterior mean：给定 data后 \(E[f(x)\mid S]\)；
- latent posterior variance：\(\operatorname{Var}(f(x)\mid S)=c_n(x,x)\)；
- fresh-response predictive variance：若 \(Y=f(x)+\varepsilon\)，则
  $$
  \operatorname{Var}(Y\mid S,x)=c_n(x,x)+\sigma^2.
  $$

最后一项包含 measurement/observation noise；不能用 latent interval代替新 observation interval。

### LT-KGP-A02

finite df：

$$
\operatorname{tr}[K(K+n\lambda I)^{-1}]
=\sum_j\frac{\mu_j}{\mu_j+n\lambda}.
$$

population effective dimension：

$$
\mathcal N(\lambda)
=\operatorname{Tr}[T(T+\lambda I)^{-1}]
=\sum_j\frac{\rho_j}{\rho_j+\lambda}.
$$

前者依 realized inputs的 Gram spectrum，后者依 \(P_X\) 的 covariance operator。每个方向贡献 \([0,1]\) 的 shrinkage，不必为 0或1，所以总和通常非整数。kernel、bandwidth、inputs与 \(\lambda\) 都改变 eigenvalues/filter。

### LT-KGP-A03

同一 mean只说明 point prediction algebra相同。KRR的 randomness来自 repeated samples，GP的 posterior randomness来自 declared prior/likelihood conditional distribution。GP covariance、credible set、marginal likelihood、joint sampling没有由 KRR objective定义；KRR frequentist coverage也不由 GP covariance无条件给出。\(c\) 在 KRR是 regularization scale，在 GP是 \(\sigma^2/\tau^2\)，hyperparameter selection语义不同。

## B. 手算与数值判断

### LT-KGP-B01

$$
K+n\lambda I
=
\begin{bmatrix}10&0\\0&2\end{bmatrix}.
$$

所以

$$
\widehat\alpha
=
\begin{bmatrix}2/10\\2/2\end{bmatrix}
=
\boxed{(0.2,1)^T}.
$$

fitted values：

$$
K\widehat\alpha
=
\boxed{(1.8,1)^T}.
$$

shrinkage：

$$
s_1=\frac9{10}=0.9,
\qquad
s_2=\frac12=0.5.
$$

df：

$$
\boxed{0.9+0.5=1.4}.
$$

### LT-KGP-B02

$$
y_i-\widehat y_i^{(-i)}
=
\frac{0.3}{1-0.75}
=\boxed{1.2}.
$$

formula精确计算 fixed smoother/hyperparameter的 leave-one-out residual。但从整条 curve中取 minimum \(\lambda\) 是 data-dependent selection；minimum score对自身 procedure optimistic。它还训练在 \(n-1\) samples上，且不能作为最终 full-data fitted function的独立测试。

### LT-KGP-B03

因为 \(\sigma^2/\tau^2=1\)：

$$
(K+I)^{-1}
=
\operatorname{diag}(1/10,1/2).
$$

quadratic reduction：

$$
k_x^T(K+I)^{-1}k_x
=
\frac{0.5^2}{10}
+\frac{0.2^2}{2}
=0.025+0.02
=0.045.
$$

latent posterior variance：

$$
\boxed{c_n(x,x)=1-0.045=0.955}.
$$

fresh-response variance：

$$
\boxed{0.955+1=1.955}.
$$

## C. 推导与证明

### LT-KGP-C01

令 \(\mathcal S=\operatorname{span}\{k_{x_i}\}\)。分解 \(f=f_\parallel+f_\perp\)。因 reproducing property：

$$
f_\perp(x_i)=\langle f_\perp,k_{x_i}\rangle=0.
$$

empirical fit只依 \(f_\parallel\)，而

$$
\|f\|^2=\|f_\parallel\|^2+\|f_\perp\|^2.
$$

\(\lambda>0\) 时 minimizer必有 \(f_\perp=0\)，故 \(f=\sum_i\alpha_i k_{x_i}\)。代入：

$$
J(\alpha)=\frac1n\|y-K\alpha\|^2+\lambda\alpha^TK\alpha.
$$

一阶条件：

$$
K[(K+n\lambda I)\alpha-y]=0.
$$

因为 \(K+n\lambda I\succ0\)，取 canonical solution

$$
\boxed{\alpha=(K+n\lambda I)^{-1}y}.
$$

它满足 bracket为零，并对应唯一 RKHS minimizer；若 kernel sections线性依赖，其他 coefficient representation的零函数成分不改变 \(f\)。

### LT-KGP-C02

joint block Gaussian：

$$
\begin{bmatrix}y\\f_*\end{bmatrix}
\sim N\left(0,
\begin{bmatrix}
C&\tau^2k_*\\
\tau^2k_*^T&\tau^2k_{**}
\end{bmatrix}
\right),
$$

其中 \(C=\tau^2K+\sigma^2I\)。Gaussian conditioning formula给

$$
E[f_*\mid y]
=\tau^2k_*^TC^{-1}y
=k_*^T(K+\sigma^2/\tau^2I)^{-1}y,
$$

$$
\operatorname{Cov}(f_*,f_*'\mid y)
=\tau^2k_{**'}
-\tau^4k_*^TC^{-1}k_*'.
$$

提取 \(\tau^2\) 得正文 formula。若 future observation \(Y_*=f_*+\varepsilon_*\)，且 \(\varepsilon_*\) 与 posterior latent独立、variance \(\sigma^2\)，total variance相加得到 \(c_n(x_*,x_*)+\sigma^2\)。

### LT-KGP-C03

mean-loss KRR：

$$
\widehat f(x)=k_x^T(K+n\lambda I)^{-1}y.
$$

GP mean：

$$
m(x)=k_x^T(K+\sigma^2/\tau^2I)^{-1}y.
$$

对任意 data与 test point相同，需要 diagonal constants相等：

$$
\boxed{n\lambda=\sigma^2/\tau^2}.
$$

若 KRR objective为

$$
\sum_i(y_i-f_i)^2+\lambda_{sum}\|f\|^2,
$$

system是 \(K+\lambda_{sum}I\)，所以

$$
\boxed{\lambda_{sum}=\sigma^2/\tau^2}.
$$

## D. 边界、反例与纠错

### LT-KGP-D01

设 Mercer representation

$$
k(x,x')=\sum_j\rho_j\psi_j(x)\psi_j(x').
$$

形式上 GP draw：

$$
f(x)=\sum_j\sqrt{\rho_j}Z_j\psi_j(x),
\qquad Z_j\overset{iid}{\sim}N(0,1).
$$

RKHS norm要求

$$
\|f\|_{\mathcal H_k}^2
=
\sum_j
\frac{(\sqrt{\rho_j}Z_j)^2}{\rho_j}
=
\sum_jZ_j^2.
$$

在 infinite-dimensional情形该和几乎必然发散。因此 sample path常不在 RKHS；RKHS描述 Cameron–Martin shifts，不是 prior支持中的“uniform finite-norm draws”。

### LT-KGP-D02

- jitter：为 factorization稳定加小 diagonal；
- observation noise：likelihood中的真实/模型化 response variance；
- ridge：frequentist estimator penalty；
- low rank：用另一个 approximate Gram/operator。

错误示例：把 large jitter当真实 noise会夸大 predictive noise并改变 posterior mean；把 low-rank遗漏 directions导致的 posterior variance下降当“更多确定性”会 understate approximation uncertainty。若把 ridge当 noise，却未对齐 \(n\) 与 prior amplitude，也会错误解释尺度。

### LT-KGP-D03

marginal likelihood含 fit与 log-det，但不保证 model class正确。它可能：

- 对 length scale/noise有多个 local modes；
- 在 finite sample偏好错误 smoothness；
- plug-in \(\widehat\theta\) 忽略 hyperparameter uncertainty；
- 在多个 kernels/transformations中 adaptive挑最大而产生 selection optimism；
- 在 deployment shift下优化 training evidence而非 target utility。

需 multi-start/priors、nested prediction evaluation、sensitivity与 shift audit；full Bayes也仍依 model class。

## E. AI 迁移

### LT-KGP-E01

固定 embedding与 kernel hyperparameters时，posterior覆盖 latent GP函数及 declared observation noise的 conditional uncertainty。未覆盖：pretraining data/sample、checkpoint/seed、representation estimation、kernel architecture search、empirical-Bayes plug-in、label process misspecification、domain/prevalence/concept shift及 approximate solver。应通过 ensembles/hierarchical model、nested selection、coverage calibration与 shift tests补充，而非把 GP variance称“总不确定性”。

### LT-KGP-E02

\(n=10^6\) 无法 dense \(O(n^2)\) storage。选择取决于接口：

- shift-invariant kernel且可接受显式 features：random Fourier features，训练 linear ridge；
- spectrum快速衰减/可选 landmarks：Nyström；
- 有 fast MVM/structured kernel：preconditioned CG与 stochastic trace/log-det；
- GP posterior需要 inducing variational objective：inducing variables。

验收字段：rank/features \(m,D\)、sampling scheme、seed、spectral/residual error、held-out risk、uncertainty coverage、memory/time、preconditioner、stopping、jitter、hyperparameter nested selection与 exact small-subset benchmark。

### LT-KGP-E03

安全审计：

1. 预声明 domain与 constraint；
2. synthetic/held-out functions检查 posterior coverage与 calibration；
3. 比较多个 plausible kernels/mean functions；
4. 每轮 hyperparameter refit记录并传播 uncertainty；
5. acquisition是 adaptive data collection，final performance用独立/online-safe protocol；
6. posterior variance floor与 observation noise分开；
7. constraint model采用 conservative bound/feasibility概率；
8. 对 OOD regions设置 abstention/trust region；
9. 记录 failed/censored experiments；
10. 报告 cumulative constraint violations与 worst-case cost，而非只报 best objective。
