---
type: theorem
status: draft
area: [learning-theory/latent-variable-models, mixture-models, em, incomplete-data]
aliases: [Latent Variable Models, Mixture Models and EM, Expectation Maximization Theory]
node_id: LT-51
prerequisites: ["[[最大似然估计与 MAP]]", "[[交叉熵与 KL 散度]]", "[[凸函数、Jensen 不等式与上图集]]", "[[多元高斯分布]]", "[[K-Means、聚类风险与不可辨识性]]"]
related: ["[[模型可辨识性、选择与 Misspecification]]", "[[变分推断、ELBO 与证据分解]]", "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]", "[[表示坍缩、非坍缩与可辨识边界]]"]
sources: ["[[S-1977-Dempster-Laird-Rubin-EM]]", "[[S-1983-Wu-EM-Convergence]]", "[[S-1963-Teicher-Finite-Mixture-Identifiability]]", "[[S-2018-Su-5239-从最大似然到EM]]", "[[S-2009-Hastie-Tibshirani-Friedman-ESL]]"]
exercises: ["[[习题 - 潜变量模型、混合模型与 EM]]"]
solutions: ["[[解答 - 潜变量模型、混合模型与 EM]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-latent-mixture-em-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 潜变量模型、混合模型与 EM

> [!abstract] 本章主问题
> 潜变量模型声明一个没有直接观测的随机变量 \(Z\)，通过
>
> $$
> p_\theta(x)=\sum_zp_\theta(x,z)
> $$
>
> 或积分得到 observed-data likelihood。难点是 log 放在求和外：
>
> $$
> \log\sum_zp_\theta(x,z),
> $$
>
> component assignment与parameter互相依赖。EM 用当前 parameter下的 latent posterior构造 auxiliary distribution，再优化 expected complete-data log-likelihood。
>
> 但必须分清：
>
> - latent variable \(Z\) 不是 parameter \(\theta\)；
> - E-step posterior responsibility不是“已发现真实类别”；
> - likelihood monotonicity不是global optimality；
> - likelihood values收敛不自动给parameter iterates收敛；
> - finite mixtures常有label switching、weak separation与Gaussian variance collapse；
> - exact EM、generalized EM、variational EM与amortized inference合同不同。

> [!question] 初学者读完必须能回答
> 1. complete-data likelihood与observed-data likelihood差在哪里？
> 2. ELBO/KL恒等式怎样推出 E-step？
> 3. M-step改善 \(Q\) 为什么使observed likelihood不降？
> 4. Gaussian mixture responsibilities与参数updates如何推导？
> 5. label switching与variance collapse分别是什么问题？
> 6. EM收敛到stationary point需要哪些额外条件？

## 一、学习目标

1. 区分 observed variable、latent variable、parameter与posterior；
2. 从 joint model推导 marginal likelihood；
3. 推导一般 ELBO/KL恒等式；
4. 证明 exact E-step使 bound tight；
5. 证明 exact/generalized M-step的 likelihood monotonicity；
6. 手推 finite Gaussian mixture的E/M updates；
7. 区分 algorithm convergence、MLE existence、identifiability与statistical consistency；
8. 解释 label permutation、singularity、local maxima与slow convergence；
9. 比较 EM、variational EM、Monte Carlo EM与gradient optimization；
10. 审计 mixture-of-experts、latent routing与AI pseudo-semantics。

## 二、对象合同

观测数据：

$$
X_1,\ldots,X_n.
$$

每个 observation关联 latent variable：

$$
Z_1,\ldots,Z_n.
$$

parameter：

$$
\theta\in\Theta.
$$

joint model：

$$
p_\theta(x,z).
$$

observed/marginal model：

$$
\boxed{
p_\theta(x)
=
\sum_zp_\theta(x,z)
}
$$

或 continuous latent时

$$
p_\theta(x)
=
\int p_\theta(x,z)\,dz.
$$

observed log-likelihood：

$$
\ell_n(\theta)
=
\sum_{i=1}^n\log p_\theta(X_i).
$$

complete-data log-likelihood：

$$
\ell_c(\theta;x,z)
=
\sum_{i=1}^n\log p_\theta(x_i,z_i).
$$

complete data是一个 mathematical augmentation；在 ordinary mixture fitting中 \(z_i\) 没有被观测。

## 三、Finite Mixture Model

令 \(Z\in\{1,\ldots,K\}\)，mixing weights：

$$
P_\theta(Z=k)=\pi_k,
\qquad
\pi_k\ge0,
\qquad
\sum_{k=1}^K\pi_k=1.
$$

conditional component density：

$$
X\mid Z=k
\sim
f(\cdot;\eta_k).
$$

joint：

$$
p_\theta(x,z=k)
=
\pi_k f(x;\eta_k).
$$

marginal：

$$
\boxed{
p_\theta(x)
=
\sum_{k=1}^K
\pi_k f(x;\eta_k).
}
$$

parameter：

$$
\theta
=
(\pi_1,\ldots,\pi_K,\eta_1,\ldots,\eta_K).
$$

observed log-likelihood：

$$
\ell_n(\theta)
=
\sum_{i=1}^n
\log
\left[
\sum_{k=1}^K
\pi_kf(X_i;\eta_k)
\right].
$$

log-of-sum使 component-specific sufficient statistics不可直接读出。

## 四、Latent Indicators

定义 one-hot latent indicators：

$$
Z_{ik}
=
\mathbf 1\{Z_i=k\}.
$$

complete likelihood：

$$
p_\theta(x,z)
=
\prod_{i=1}^n
\prod_{k=1}^K
\left[
\pi_kf(x_i;\eta_k)
\right]^{z_{ik}}.
$$

complete log-likelihood：

$$
\boxed{
\ell_c(\theta;x,z)
=
\sum_{i=1}^n\sum_{k=1}^K
z_{ik}
\left[
\log\pi_k+\log f(x_i;\eta_k)
\right].
}
$$

若 \(z_{ik}\) 已知，通常可按 components分开估计；EM用 conditional expectation \(E[Z_{ik}\mid X]\) 替代未知 indicator。

## 五、一般 ELBO / KL 恒等式

对单个 \(x\)，取任意 auxiliary distribution \(q(z)\)，且其support不超出 joint model support：

$$
\begin{aligned}
\log p_\theta(x)
&=
\log\sum_zq(z)
\frac{p_\theta(x,z)}{q(z)}\\
&\ge
\sum_zq(z)
\log\frac{p_\theta(x,z)}{q(z)}.
\end{aligned}
$$

定义

$$
\boxed{
\mathcal F(q,\theta)
=
E_q[\log p_\theta(x,Z)]
+
H(q).
}
$$

更精确地，

$$
\boxed{
\log p_\theta(x)
=
\mathcal F(q,\theta)
+
\mathrm{KL}
\left(
q(z)
\middle\|
p_\theta(z\mid x)
\right).
}
$$

证明：

$$
\begin{aligned}
\mathrm{KL}(q\|p_\theta(\cdot\mid x))
&=
E_q\left[
\log q(Z)
-
\log p_\theta(Z\mid x)
\right]\\
&=
E_q[\log q(Z)]
-
E_q[\log p_\theta(x,Z)]
+
\log p_\theta(x).
\end{aligned}
$$

移项即得。

由于 KL非负：

$$
\mathcal F(q,\theta)
\le
\log p_\theta(x).
$$

等号当且仅当

$$
q(z)=p_\theta(z\mid x)
$$

在适当 a.e. 意义下成立。

## 六、E-Step

给 current parameter \(\theta^{(t)}\)，exact E-step：

$$
\boxed{
q_i^{(t)}(z)
=
p_{\theta^{(t)}}(z\mid x_i).
}
$$

这使

$$
\mathrm{KL}
\left(
q_i^{(t)}
\|
p_{\theta^{(t)}}(\cdot\mid x_i)
\right)
=
0,
$$

所以 lower bound在 current parameter处tight：

$$
\mathcal F(q^{(t)},\theta^{(t)})
=
\ell_n(\theta^{(t)}).
$$

定义 EM auxiliary function：

$$
\boxed{
Q(\theta\mid\theta^{(t)})
=
E_{\theta^{(t)}}[
\ell_c(\theta;X,Z)
\mid X
].
}
$$

因为 \(H(q^{(t)})\) 在 M-step中不依 candidate \(\theta\)，最大化 \(\mathcal F\) 等价于最大化 \(Q\)。

## 七、M-Step 与 Monotonicity

exact M-step：

$$
\boxed{
\theta^{(t+1)}
\in
\arg\max_\theta
Q(\theta\mid\theta^{(t)}).
}
$$

取 \(q^{(t)}=p_{\theta^{(t)}}(z\mid x)\)。利用恒等式：

$$
\ell_n(\theta)
=
\mathcal F(q^{(t)},\theta)
+
\mathrm{KL}
\left(
q^{(t)}
\|
p_\theta(z\mid x)
\right).
$$

在 old parameter：

$$
\ell_n(\theta^{(t)})
=
\mathcal F(q^{(t)},\theta^{(t)}).
$$

因此

$$
\begin{aligned}
\ell_n(\theta^{(t+1)})
-
\ell_n(\theta^{(t)})
&=
\mathcal F(q^{(t)},\theta^{(t+1)})
-
\mathcal F(q^{(t)},\theta^{(t)})\\
&\quad+
\mathrm{KL}
\left(
q^{(t)}
\|
p_{\theta^{(t+1)}}(z\mid x)
\right)\\
&\ge
Q(\theta^{(t+1)}\mid\theta^{(t)})
-
Q(\theta^{(t)}\mid\theta^{(t)}).
\end{aligned}
$$

若 M-step不降低 \(Q\)，则

$$
\boxed{
\ell_n(\theta^{(t+1)})
\ge
\ell_n(\theta^{(t)}).
}
$$

这也覆盖 generalized EM：不必找到 \(Q\) global maximizer，只需保证足够改进。但 approximate/stochastic estimates若有 Monte Carlo noise，observed likelihood未必每步严格单调。

## 八、图：EM 的严谨对象链

先看图回答：为什么 E-step的 responsibility可等于 \(0.9\)，却仍不能断言 observation的“真实类型”以90%概率被发现？

![[00-知识库管理/_assets/figures/learning-theory/fig-latent-mixture-em-v2.svg|900]]

> [!figure] 图 20.6-11　潜变量 posterior、ELBO 恒等式与 EM 单调链
> 左栏把observed \(X\)、unobserved \(Z\) 与posterior responsibility分开；中栏用 \(\log p=\mathcal F+\mathrm{KL}\) 说明 exact E-step令bound tight、M-step改善bound并使observed likelihood不降；右栏列出local stationary、label switching、Gaussian variance collapse与missing-information slow convergence。来源：依据 Dempster–Laird–Rubin、Wu、Teicher、科学空间EM文章与ESL独立绘制；确定性 SVG，由 [[plot_classical_models_unsupervised_v2.py]] 生成。

**怎样读图**：中栏是同一 objective的坐标上升结构；右栏提醒 monotonicity只是一条 optimization invariant，不包含MLE existence、parameter uniqueness或model truth。

**图没有证明什么**：它没有证明 latent classes对应human concepts、causal mechanisms或真实群体，也没有证明任意 approximate E/M implementation保持 exact EM guarantee。

## 九、Gaussian Mixture Model

令

$$
X\mid Z=k
\sim
\mathcal N(\mu_k,\Sigma_k).
$$

marginal：

$$
p_\theta(x)
=
\sum_{k=1}^K
\pi_k
\mathcal N(x;\mu_k,\Sigma_k).
$$

### 9.1 E-Step Responsibilities

Bayes rule：

$$
\boxed{
r_{ik}
:=
P_{\theta^{(t)}}(Z_i=k\mid X_i=x_i)
=
\frac{
\pi_k^{(t)}
\mathcal N(x_i;\mu_k^{(t)},\Sigma_k^{(t)})
}{
\sum_{j=1}^K
\pi_j^{(t)}
\mathcal N(x_i;\mu_j^{(t)},\Sigma_j^{(t)})
}.
}
$$

满足

$$
r_{ik}\ge0,
\qquad
\sum_kr_{ik}=1.
$$

数值实现必须在 log domain：

$$
\log r_{ik}
=
a_{ik}
-
\operatorname{LSE}_j(a_{ij}),
$$

其中

$$
a_{ik}
=
\log\pi_k+\log\mathcal N(x_i;\mu_k,\Sigma_k).
$$

### 9.2 Effective Counts

$$
N_k
=
\sum_{i=1}^nr_{ik}.
$$

### 9.3 Mixing Weights

在 simplex constraint下：

$$
\boxed{
\pi_k^{(t+1)}
=
\frac{N_k}{n}.
}
$$

### 9.4 Means

$$
\boxed{
\mu_k^{(t+1)}
=
\frac1{N_k}
\sum_{i=1}^n
r_{ik}x_i.
}
$$

### 9.5 Covariances

$$
\boxed{
\Sigma_k^{(t+1)}
=
\frac1{N_k}
\sum_{i=1}^n
r_{ik}
(x_i-\mu_k^{(t+1)})
(x_i-\mu_k^{(t+1)})^T.
}
$$

若 covariance受 shared/diagonal/isotropic constraints，M-step公式随 parameterization改变。

## 十、一个 Responsibility 手算

两 components：

$$
\pi_1=\pi_2=\frac12,
\qquad
\mu_1=-1,
\qquad
\mu_2=1,
\qquad
\sigma_1^2=\sigma_2^2=1.
$$

对 \(x=0\)，两密度相等：

$$
r_1=r_2=\frac12.
$$

对 \(x=2\)，忽略共同 normalization：

$$
\phi(2;-1,1)\propto e^{-9/2},
\qquad
\phi(2;1,1)\propto e^{-1/2}.
$$

所以

$$
r_2
=
\frac{e^{-1/2}}
{e^{-9/2}+e^{-1/2}}
=
\frac1{1+e^{-4}}
\approx
0.9820.
$$

这是 declared two-Gaussian model与current parameters下的 conditional probability；若 model错设、\(K\)错或parameters由同数据不稳定估计，它不是无条件现实类别概率。

## 十一、Soft K-Means 接口

若 Gaussian mixture使用：

$$
\pi_k=1/K,
\qquad
\Sigma_k=\sigma^2I,
$$

则

$$
r_{ik}
\propto
\exp
\left(
-\frac{\|x_i-\mu_k\|^2}{2\sigma^2}
\right).
$$

当

$$
\sigma^2\downarrow0,
$$

responsibilities趋于 nearest-center hard assignments（无ties时）。但：

- K-Means objective不是一般 GMM observed likelihood；
- GMM还估 mixing weights/covariances；
- finite \(\sigma\) 有soft uncertainty；
- \(\sigma\to0\) 是singular limit；
- generative density fit与quantization risk语义不同。

## 十二、Label Switching

对任意 permutation \(\pi\)：

$$
\pi_k'
=
\pi_{\pi(k)},
\qquad
\eta_k'
=
\eta_{\pi(k)}.
$$

则

$$
p_{\theta'}(x)=p_\theta(x).
$$

所以 mixture parameter不在 ordinary ordered space上 identifiable。应：

- 比较 mixture density；
- optimal-match components；
- 加identifying convention用于reporting；
- Bayesian posterior中允许多个symmetric modes；
- 不把MCMC跨label modes误判成 parameter instability。

Teicher式 identifiability结论通常是 **up to permutation**，并依component family/number等条件。

## 十三、Gaussian Mixture Variance Collapse

对某 observation \(x_i\)，令一个 component：

$$
\mu_k=x_i,
\qquad
\Sigma_k=\varepsilon^2I.
$$

则

$$
\mathcal N(x_i;\mu_k,\Sigma_k)
\propto
\varepsilon^{-d}
\to\infty
\qquad
(\varepsilon\downarrow0).
$$

只要其 weight保持正且其他 components拟合其余points，observed likelihood可发散。因此 unrestricted Gaussian mixture MLE可能不存在。

常见干预：

- covariance floor；
- shared/isotropic covariance；
- inverse-Wishart/penalty；
- minimum component weight/effective count；
- constrained parameter space；
- Bayesian prior。

这些不是纯numerical jitter，而是改变 estimator/model。

## 十四、EM “收敛”分四层

### 14.1 Likelihood Monotonicity

$$
\ell(\theta^{(t+1)})
\ge
\ell(\theta^{(t)}).
$$

### 14.2 Likelihood Values Converge

若 likelihood sequence有上界，则 monotone sequence有limit。

### 14.3 Limit Points Stationary

需要 continuity、closed mapping、differentiability、interior等regularity。Wu给出相应条件化结果。

### 14.4 Parameters Converge to Unique MLE

需要更强的 uniqueness/unimodality/compactness等条件；mixtures通常不满足。

因此以下推理错误：

$$
\text{likelihood increments small}
\Rightarrow
\text{global MLE found}.
$$

increment small也可能来自flat ridge、weak separation、boundary或numerical tolerance。

## 十五、为什么 EM 可能很慢

E-step后仍有大量 latent uncertainty时，complete-data information与observed-data information差距大。直觉上：

- components重叠强；
- responsibilities接近 diffuse；
- parameters与latent assignments相互拖动；
- local EM map derivative接近1；
- linear convergence factor接近1。

Newton/quasi-Newton、ECM/ECME、parameter expansion或acceleration可改善，但改变algorithm与stability。不能只比较iterations，应比较 likelihood evaluations、linear solves、memory与final stationarity。

## 十六、Initialization 与 Multiple Starts

常见 initialization：

- random responsibilities；
- K-Means centers；
- hierarchical clustering；
- method of moments；
- warm-start from simpler model；
- domain-informed seeds。

多 starts后选最高 training likelihood是更大的 optimization search，但仍可能：

- 选择singular solution；
- 适配training noise；
- 漏掉broad basins；
- 在外部test上不优。

需报告 start distribution、budget、best/median、component collapse与held-out log score。

## 十七、Exact、Generalized、Variational 与 Monte Carlo EM

| 方法 | E-step | M-step | 单调性合同 |
|---|---|---|---|
| exact EM | exact posterior | exact \(Q\) max | observed likelihood不降 |
| generalized EM | exact posterior | 只改善 \(Q\) | 若确实改善则不降 |
| variational EM | restricted \(q\) family | 改善ELBO | ELBO不降，不必是likelihood |
| Monte Carlo EM | posterior expectation近似 | approximate | finite MC noise下需误差控制 |
| amortized inference | learned \(q_\phi(z\mid x)\) | joint gradient | optimization gap + amortization gap |

尤其在 VAE 中，encoder \(q_\phi\) 不是每个 datapoint的exact E-step；它共享parameters且通常受restricted family限制。

## 十八、Model Selection 与 Number of Components

training likelihood通常随 \(K\) 增大不降，且Gaussian mixture有singularity。选择 \(K\) 可使用：

- held-out log likelihood；
- cross-validation；
- regularized likelihood；
- BIC/AIC，在regularity适用性审计后；
- Bayesian marginal likelihood；
- task-specific utility；
- posterior predictive checks。

mixture models是典型 singular/nonidentifiable models，朴素

$$
d\log n
$$

penalty的regular Laplace推导可能失效。不要把software BIC数字当无条件 Bayes evidence。

## 十九、Misspecification

即使 EM找到 observed likelihood global optimum，若

$$
P_0\notin\{P_\theta:\theta\in\Theta\},
$$

它只找到 model family内的近似。常见错设：

- component tails错误；
- covariance shape错误；
- observations dependent；
- \(K\)不足/过多；
- missingness机制忽略；
- latent classes并非exchangeable；
- data经过selection/truncation；
- deployment distribution改变。

posterior responsibilities在错设下仍可数值sharp，却未必calibrated。

## 二十、AI 接口

### 20.1 Mixture of Experts

$$
p(y\mid x)
=
\sum_{k=1}^K
\pi_k(x)
p_k(y\mid x).
$$

这里 gate \(\pi_k(x)\) 与 expert likelihood均依 \(x\)。它不是ordinary i.i.d. mixture的直接复制。joint training会有：

- expert permutation symmetry；
- gate collapse；
- load imbalance；
- rich gate导致 nonidentifiability；
- routing feedback改变data distribution；
- top-\(k\) discrete approximation。

### 20.2 Latent Prompt / Topic Model

posterior topic weight高不等于文档具有唯一“真实主题”。topic语义来自 model/priors/vocabulary/selection；需 stability、held-out likelihood与human/task validation。

### 20.3 Weak Supervision

latent class可以整合 noisy labels，但若 annotator dependence与class prevalence错设，responsibility会过度自信。需要 gold subset、calibration与sensitivity。

### 20.4 Generative Models

discrete latent codes、VQ codebooks与diffusion mixture components都可能出现 unused components与symmetry。ELBO改善不自动说明 sample quality、coverage或semantic disentanglement。

## 二十一、完整验收 Protocol

1. 声明 observed/latent variables与joint factorization；
2. 写出 support与parameter constraints；
3. 检查 identifiability up to symmetry；
4. 检查 likelihood是否bounded/MLE是否存在；
5. 使用多 starts并记录所有 failure modes；
6. 同时报 observed likelihood、ELBO（若不同）、stationarity与parameter movement；
7. selection放入nested validation；
8. final test用 proper predictive score；
9. 对 responsibilities做 calibration/semantic/shift audit；
10. 保存component matching与version。

## 二十二、常见错误

### 错误 1：E-Step 是填入真实 Missing Values

它计算 current model下的conditional distribution/expectation，不是恢复ground truth。

### 错误 2：EM每轮增 Likelihood，所以是全局优化

nonconvex objective可有多个stationary points。

### 错误 3：Likelihood有上界，所以Parameters收敛

parameter sequence可在level set上移动；还需regularity/uniqueness。

### 错误 4：Mixture可辨识，所以有限样本容易估

identifiability不保证well-conditioned estimation；weak separation可使information近singular。

### 错误 5：Covariance Floor 只是数值修复

它约束model/estimator并防止singularity，具有统计含义。

## 二十三、审计清单

1. \(Z\) 是什么，是否真正observed？
2. joint/marginal likelihood是否写对？
3. E-step exact还是approximate？
4. M-step maximizes、improves还是stochastic？
5. 监控的是likelihood还是ELBO？
6. MLE是否存在，parameter space是否compact/constrained？
7. label symmetry如何处理？
8. initialization与multiple-start budget是什么？
9. \(K\) 怎样选择，是否regular criterion适用？
10. responsibility语义与deployment calibration如何验收？

## 二十四、本章掌握标准

### A. 识别

能区分 latent variable、parameter、posterior responsibility与complete-data statistic。

### B. 计算

能手算两component responsibility与Gaussian mixture M-step。

### C. 推导

能独立重建 ELBO/KL恒等式、E-step tightness与M-step monotonicity。

### D. 边界

能构造 label switching、variance collapse、local optimum与misspecified latent semantics。

### E. AI 迁移

能审计 mixture-of-experts/VAE/latent routing的symmetry、collapse、approximate inference与evaluation。

对应训练：[[习题 - 潜变量模型、混合模型与 EM]]  
独立详解：[[解答 - 潜变量模型、混合模型与 EM]]

## 二十五、最小记忆

1. observed likelihood对latent variable求和/积分；
2. complete log-likelihood通常更易优化；
3. \(\log p=\mathcal F+\mathrm{KL}\) 是EM主恒等式；
4. exact E-step使bound tight；
5. M-step改善 \(Q\) 使observed likelihood不降；
6. monotonicity不等于global optimality；
7. likelihood convergence不等于parameter convergence；
8. mixtures至少有label permutation symmetry；
9. unrestricted Gaussian mixture likelihood可因variance collapse无界；
10. exact EM、variational EM与amortized inference不是同一保证。
