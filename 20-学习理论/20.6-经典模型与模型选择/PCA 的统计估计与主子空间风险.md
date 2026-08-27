---
type: theorem
status: draft
area: [learning-theory/pca, covariance-estimation, subspace-risk, dimension-reduction]
aliases: [Statistical PCA Theory, Principal Subspace Estimation, PCA Risk]
node_id: LT-49
prerequisites: ["[[协方差、相关性与条件期望]]", "[[定理 - 有限维谱定理]]", "[[奇异值分解]]", "[[定理 - Eckart–Young–Mirsky]]", "[[特征向量与子空间扰动定理]]"]
related: ["[[核岭回归与 Gaussian Process 接口]]", "[[K-Means、聚类风险与不可辨识性]]", "[[表示学习的任务、表示与下游风险]]", "[[Covariate、Label 与 Concept Shift]]"]
sources: ["[[S-2016-Jolliffe-Cadima-PCA-Review]]", "[[S-2015-Yu-Wang-Samworth-Davis-Kahan]]", "[[S-2009-Hastie-Tibshirani-Friedman-ESL]]"]
exercises: ["[[习题 - PCA 的统计估计与主子空间风险]]"]
solutions: ["[[解答 - PCA 的统计估计与主子空间风险]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-pca-subspace-risk-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# PCA 的统计估计与主子空间风险

> [!abstract] 本章主问题
> PCA 常被介绍成“对数据做一次 SVD”。这只说了计算层，没有说清统计对象：
>
> - population PCA 的目标是总体 covariance \(\Sigma\) 的 top eigenspace；
> - sample PCA 使用 data-dependent \(\widehat\Sigma\) 估计它；
> - 最大投影方差、最小正交重构误差与 centered data matrix 的 top singular subspace在同一 normalization 下等价；
> - eigenvalue估得准不等于 eigenvector估得准，主子空间误差还要除以 eigengap；
> - repeated eigenvalue下单根 eigenvector不具有可辨识意义，应比较 projector或 invariant subspace；
> - explained variance高不等于对 label、因果机制或 deployment utility有用。
>
> 因此本章把 **经验优化、总体目标、子空间损失、谱扰动、维数选择和 AI 使用协议** 分开。

> [!question] 初学者读完必须能回答
> 1. 为什么 PCA 必须先声明 centering 与 scaling？
> 2. 最大方差与最小 reconstruction error 怎样严格等价？
> 3. sample covariance 与 centered data SVD如何对应？
> 4. 为什么 eigengap小会使方向剧烈旋转？
> 5. repeated eigenvalues时应估计 eigenvector还是 subspace？
> 6. 为什么在全数据上先做 PCA 再 cross-validation 会泄漏？

## 一、学习目标

1. 写出 population/sample PCA 的不同随机对象；
2. 用 Rayleigh–Ritz 推导第一主方向；
3. 用 Ky Fan 原理推导 top-\(r\) principal subspace；
4. 证明 projected variance与 reconstruction error等价；
5. 从 centered data SVD推导 covariance eigendecomposition；
6. 定义 projector、principal-angle与 excess-reconstruction losses；
7. 用 Weyl 与 Davis–Kahan建立 covariance error到 subspace error的桥；
8. 区分 eigenvalue、basis、subspace与 downstream prediction；
9. 审计 rank selection、whitening、standardization、robustness与 high-dimensional regime；
10. 为 embedding compression建立无泄漏 evaluation protocol。

## 二、对象合同

令

$$
X\in\mathbb R^d,
\qquad
\mu=E[X],
\qquad
\Sigma=E[(X-\mu)(X-\mu)^T].
$$

假设 \(E\|X\|^2<\infty\)，则 \(\Sigma\succeq0\)。谱分解：

$$
\Sigma
=
U\Lambda U^T,
\qquad
\lambda_1\ge\lambda_2\ge\cdots\ge\lambda_d\ge0.
$$

population rank-\(r\) principal subspace：

$$
\mathcal U_r
=
\operatorname{span}(u_1,\ldots,u_r),
\qquad
P_r=U_rU_r^T.
$$

样本 \(X_1,\ldots,X_n\overset{\mathrm{iid}}{\sim}P\)。sample mean 与 mean-normalized covariance：

$$
\bar X
=
\frac1n\sum_{i=1}^nX_i,
$$

$$
\widehat\Sigma
=
\frac1n\sum_{i=1}^n
(X_i-\bar X)(X_i-\bar X)^T.
$$

> [!warning] \(1/n\) 与 \(1/(n-1)\)
> \(1/(n-1)\) 使 sample covariance在 i.i.d. finite-second-moment 条件下无偏；\(1/n\) 与 mean empirical reconstruction objective直接对齐。二者只差 scalar，不改变 eigenvectors，却改变 eigenvalues与 explained-variance scale。实现与定理必须声明 convention。

sample top-\(r\) subspace：

$$
\widehat{\mathcal U}_r
=
\operatorname{range}(\widehat U_r),
\qquad
\widehat P_r=\widehat U_r\widehat U_r^T.
$$

随机性层次：

| 对象 | 是否随机 | 依赖 |
|---|---:|---|
| \(\Sigma,P_r\) | 在 fixed data law 下固定 | population distribution |
| \(\widehat\Sigma,\widehat P_r\) | 随 sample随机 | observations与preprocessing |
| randomized SVD output | 给 sample 后仍随机 | sketch/seed |
| downstream score | 还依 label/task split | representation与evaluation protocol |

## 三、第一主方向：最大投影方差

考虑 unit direction \(w\in\mathbb R^d\)：

$$
\|w\|_2=1.
$$

centered scalar projection为

$$
Z=w^T(X-\mu).
$$

其 variance：

$$
\operatorname{Var}(Z)
=
E[w^T(X-\mu)(X-\mu)^Tw]
=
w^T\Sigma w.
$$

因此第一主方向满足

$$
\boxed{
u_1
\in
\arg\max_{\|w\|=1}
w^T\Sigma w.
}
$$

令 \(w=\sum_j a_ju_j\)，且 \(\sum_j a_j^2=1\)，则

$$
w^T\Sigma w
=
\sum_{j=1}^d\lambda_ja_j^2
\le
\lambda_1.
$$

等号要求 \(w\) 落在 top-eigenvalue eigenspace。若 \(\lambda_1>\lambda_2\)，方向只差 sign：

$$
w=\pm u_1.
$$

若 \(\lambda_1=\lambda_2\)，top eigenspace中的任意 unit vector都最优；此时“真实第一 eigenvector”不是 distribution-identifiable object。

## 四、Top-\(r\) 子空间：总投影方差

令 \(V\in\mathbb R^{d\times r}\) 满足

$$
V^TV=I_r.
$$

projected coordinates为 \(V^T(X-\mu)\)，总 variance：

$$
E\|V^T(X-\mu)\|^2
=
\operatorname{tr}(V^T\Sigma V).
$$

Ky Fan variational principle给

$$
\boxed{
\max_{V^TV=I_r}
\operatorname{tr}(V^T\Sigma V)
=
\sum_{j=1}^r\lambda_j.
}
$$

在 gap

$$
\Delta_r
=
\lambda_r-\lambda_{r+1}
>0
$$

时，最优 subspace唯一，但 basis不唯一：

$$
V=U_rQ,
\qquad
Q^TQ=I_r.
$$

所以 top-\(r\) PCA 的不变量是

$$
P_r=U_rU_r^T,
$$

不是 \(U_r\) 的具体 columns。

## 五、为什么等价于最小重构误差

对 rank-\(r\) orthogonal projector \(P=VV^T\)，定义 population reconstruction risk：

$$
\mathcal R(P)
=
E\|(I-P)(X-\mu)\|^2.
$$

因 \(P=P^T=P^2\)：

$$
\begin{aligned}
\mathcal R(P)
&=
E[(X-\mu)^T(I-P)(X-\mu)]\\
&=
\operatorname{tr}[(I-P)\Sigma]\\
&=
\operatorname{tr}(\Sigma)-\operatorname{tr}(P\Sigma).
\end{aligned}
$$

\(\operatorname{tr}(\Sigma)\) 不依 \(P\)，故

$$
\boxed{
\arg\min_{\operatorname{rank}(P)=r}\mathcal R(P)
=
\arg\max_{\operatorname{rank}(P)=r}\operatorname{tr}(P\Sigma).
}
$$

最小风险：

$$
\boxed{
\mathcal R(P_r)
=
\sum_{j=r+1}^d\lambda_j.
}
$$

这就是“discarded eigenvalue mass”。它是 squared Euclidean reconstruction loss 下的结论；换成 \(\ell_1\)、weighted、missing-data或 manifold distance后，普通 PCA不再自动最优。

## 六、Sample PCA 与 SVD

构造 centered data matrix，令 rows 为 samples：

$$
X_c
=
\begin{bmatrix}
(X_1-\bar X)^T\\
\vdots\\
(X_n-\bar X)^T
\end{bmatrix}
\in\mathbb R^{n\times d}.
$$

则

$$
\widehat\Sigma
=
\frac1nX_c^TX_c.
$$

thin SVD：

$$
X_c
=
LDR^T.
$$

于是

$$
\widehat\Sigma
=
R\frac{D^2}{n}R^T.
$$

因此：

- sample principal directions是 \(R\) 的 columns；
- sample eigenvalues为 \(d_j^2/n\)；
- score matrix为 \(X_cR_r=L_rD_r\)；
- rank-\(r\) reconstruction为 \(L_rD_rR_r^T\)。

这也说明 PCA、truncated SVD与 Eckart–Young–Mirsky 的联系。但要注意：

- EYM是 realized matrix approximation theorem；
- statistical PCA问 \(\widehat P_r\) 是否接近 population \(P_r\)；
- 二者不是同一个概率结论。

## 七、图：经验优化如何进入总体子空间风险

先看图回答：为什么“sample covariance的 leading eigenvalue很稳定”仍不足以说明 leading direction稳定？

![[00-知识库管理/_assets/figures/learning-theory/fig-pca-subspace-risk-v2.svg|900]]

> [!figure] 图 20.6-09　PCA 的经验目标、总体对象与 gap-sensitive 误差
> 左栏显示同一总体 elongation上，sample axis可因 covariance perturbation旋转；中栏对齐最大经验方差、最小重构误差与 centered-data SVD；右栏把 subspace error写成 covariance operator error除以 population eigengap，并提醒 rank selection属于 evaluation protocol。来源：依据 Jolliffe–Cadima、Yu–Wang–Samworth与本库谱扰动节点独立绘制；确定性 SVG，由 [[plot_classical_models_unsupervised_v2.py]] 生成。

**怎样读图**：中栏三种表述在 squared Euclidean、orthogonal projection和相同 centering下等价。右栏不是说 error永远等于一个 quotient，而是给典型 perturbation architecture：numerator由 sample/tail/dependence控制，denominator由 population geometry控制。

**图没有证明什么**：它没有证明任意高维数据都存在稳定低维语义，也没有证明 explained variance高就改善 classification、generation或causal inference；这些需要 task-specific evaluation。

## 八、三种不同的误差对象

### 8.1 Eigenvalue error

Weyl inequality：

$$
|\widehat\lambda_j-\lambda_j|
\le
\|\widehat\Sigma-\Sigma\|_{\mathrm{op}}.
$$

它不除 eigengap。

### 8.2 Eigenvector / subspace error

rank-one sign-invariant loss：

$$
\sin\angle(\widehat u_1,u_1)
=
\sqrt{1-(\widehat u_1^Tu_1)^2}.
$$

rank-\(r\) projector loss：

$$
\|\widehat P_r-P_r\|_{\mathrm{op}}
=
\|\sin\Theta(\widehat U_r,U_r)\|_{\mathrm{op}},
$$

$$
\|\widehat P_r-P_r\|_F^2
=
2\|\sin\Theta(\widehat U_r,U_r)\|_F^2.
$$

典型 Davis–Kahan form：

$$
\boxed{
\|\sin\Theta(\widehat U_r,U_r)\|_{\mathrm{op}}
\lesssim
\frac{\|\widehat\Sigma-\Sigma\|_{\mathrm{op}}}{\Delta_r}.
}
$$

常数与精确 gap definition依 theorem version。重点是：同样 covariance error在 small gap下会造成更大方向误差。

### 8.3 Excess reconstruction risk

定义

$$
\mathcal E_r
=
\mathcal R(\widehat P_r)-\mathcal R(P_r)
=
\operatorname{tr}[\Sigma(P_r-\widehat P_r)].
$$

因为 \(\widehat P_r\) 最大化 sample projected variance：

$$
\operatorname{tr}(\widehat\Sigma\widehat P_r)
\ge
\operatorname{tr}(\widehat\Sigma P_r).
$$

所以

$$
\begin{aligned}
\mathcal E_r
&=
\operatorname{tr}[(\Sigma-\widehat\Sigma)(P_r-\widehat P_r)]
+\operatorname{tr}[\widehat\Sigma(P_r-\widehat P_r)]\\
&\le
\operatorname{tr}[(\Sigma-\widehat\Sigma)(P_r-\widehat P_r)]\\
&\le
\|\Sigma-\widehat\Sigma\|_{\mathrm{op}}
\|P_r-\widehat P_r\|_*\\
&\le
2r\|\Sigma-\widehat\Sigma\|_{\mathrm{op}}.
\end{aligned}
$$

因此

$$
\boxed{
\mathcal E_r
\le
2r\|\widehat\Sigma-\Sigma\|_{\mathrm{op}}.
}
$$

这个 bound不除 gap。原因是：若两条 eigen-directions的 eigenvalues几乎相同，basis可以大幅旋转但 reconstruction cost只改变很小。

> [!important] 方向恢复与风险恢复不同
> Small eigengap时，\(\widehat U_r\) 可能不稳定，而 excess reconstruction risk仍小。若目标是可解释 loading，gap很关键；若目标只是压缩，可能无需恢复唯一方向。

## 九、Covariance Estimation 才是概率输入

Davis–Kahan不直接告诉我们

$$
\|\widehat\Sigma-\Sigma\|_{\mathrm{op}}
$$

有多大。还要声明 distribution class。

在 sub-Gaussian、i.i.d. 等条件下，典型 high-probability architecture是

$$
\|\widehat\Sigma-\Sigma\|_{\mathrm{op}}
\lesssim
\|\Sigma\|_{\mathrm{op}}
\left[
\sqrt{\frac{r_{\mathrm{eff}}+t}{n}}
+
\frac{r_{\mathrm{eff}}+t}{n}
\right],
$$

其中 effective rank

$$
r_{\mathrm{eff}}
=
\frac{\operatorname{tr}(\Sigma)}
{\|\Sigma\|_{\mathrm{op}}}.
$$

具体常数与 tail assumption不可省略。若数据 heavy-tailed、dependent、按用户重复或经过 adaptive filtering，ordinary sample covariance concentration可能失效，需要 robust covariance、block arguments或新的 sampling unit。

## 十、一个二维可复算例子

令

$$
\Sigma
=
\begin{bmatrix}
4&0\\
0&1
\end{bmatrix},
\qquad
\Delta_1=3.
$$

population first direction为 \(e_1\)。设 sample perturbation

$$
\widehat\Sigma
=
\begin{bmatrix}
4&0.3\\
0.3&1
\end{bmatrix}.
$$

对 symmetric \(2\times2\) matrix，leading-axis angle满足

$$
\tan(2\theta)
=
\frac{2(0.3)}{4-1}
=
0.2.
$$

故

$$
\theta
=
\frac12\arctan(0.2)
\approx
0.0987\text{ rad}
\approx
5.65^\circ.
$$

若 gap从 \(3\) 缩小到 \(0.3\)，同样 off-diagonal perturbation会给

$$
\tan(2\theta)=2,
$$

方向旋转明显增大。

rank-one population reconstruction risk：

$$
\mathcal R(P_1)=\lambda_2=1.
$$

若误用 \(45^\circ\) direction \(v=(1,1)^T/\sqrt2\)，保留 variance：

$$
v^T\Sigma v
=
\frac{4+1}{2}
=
2.5.
$$

总 variance为 \(5\)，所以 risk为 \(2.5\)，excess risk为 \(1.5\)。

## 十一、Centering、Scaling 与 Preprocessing

### 11.1 不 Centering

对 raw second moment

$$
E[XX^T]
=
\Sigma+\mu\mu^T,
$$

做 eigendecomposition会把 mean direction当作 high-variance direction。是否需要保留 mean取决于目标，但必须明确这不再是 ordinary covariance PCA。

### 11.2 Standardization

若 variables单位不同，covariance PCA可能由大尺度单位支配。对每列除 sample standard deviation等价于对 sample correlation matrix做 PCA。

这不是“更正确”，而是改变 geometry：

- covariance PCA保留 physical amplitude；
- correlation PCA把各变量 variance归一；
- whitening进一步把 retained directions variance变为 1。

### 11.3 数据泄漏

在 supervised downstream CV 中，以下对象都必须在每个 training fold内拟合：

- mean；
- scale；
- PCA directions；
- rank \(r\)；
- whitening regularizer。

先在全数据上做 PCA再 CV，会让 validation inputs影响 representation，即使没有使用 labels也仍是 transductive leakage。

## 十二、Rank 怎样选择

explained variance ratio：

$$
\operatorname{EVR}(r)
=
\frac{\sum_{j=1}^r\widehat\lambda_j}
{\sum_{j=1}^d\widehat\lambda_j}.
$$

它只回答 sample variance accounting，不回答：

- reconstruction在新数据上的误差；
- label prediction最优 rank；
- rare subgroup是否被删除；
- downstream latency/utility；
- shift后的稳定性。

可用的选择协议：

1. unsupervised reconstruction目标：held-out reconstruction loss；
2. supervised pipeline：nested CV中的 downstream proper loss；
3. compression：quality–memory–latency Pareto；
4. scientific interpretation：bootstrap subspace stability与 loading uncertainty；
5. safety：低频但关键方向的 stress tests。

若从多个 \(r\) 中选择最优 validation score，仍有 selection optimism；最终 test必须封存。

## 十三、重复谱、Sign 与 Rotation

单个 eigenvector有 sign symmetry：

$$
u\quad\text{与}\quad -u
$$

表示同一一维 subspace。

若 block eigenvalue重复，任意 orthogonal \(Q\) 给

$$
U_rQ
$$

同一 projector。错误比较方式：

$$
\|\widehat U_r-U_r\|_F.
$$

它会把合法 rotation误记为误差。应使用：

$$
\min_{Q^TQ=I}\|\widehat U_r-U_rQ\|_F,
$$

principal angles或 projector distance。

## 十四、High-Dimensional Regime

固定 \(d\)、\(n\to\infty\) 的 classical consistency不自动描述

$$
d/n\to c>0
$$

的 regime。高维时：

- sample eigenvalues有系统 spread；
- noise directions不再逐个消失；
- weak spikes可能无法产生一致 sample eigenvectors；
- rank selection与shrinkage需要 random-matrix或structural assumptions；
- sparse/low-rank covariance结构可能提供额外信息。

所以“样本很多”必须相对 dimension、effective rank、tail与 signal gap解释。

## 十五、Computation 与 Numerical Layer

### 15.1 不显式形成 Covariance

当 \(d\) 大时，形成 \(X_c^TX_c\) 需要 \(O(d^2)\) memory且可能平方 condition number。直接对 \(X_c\) 做 SVD或 matrix-free Lanczos/randomized SVD通常更合理。

### 15.2 \(n\ll d\) 的 Dual Route

先处理

$$
X_cX_c^T\in\mathbb R^{n\times n},
$$

再恢复 right singular vectors。但极小 singular values处恢复会放大 numerical error。

### 15.3 Randomized SVD

random sketch引入新的 algorithmic randomness与 approximation error。报告：

- target rank与oversampling；
- power iterations；
- seed；
- residual
  $$
  \|X_c-X_c\widehat P_r\|;
  $$
- orthogonality；
- 相对 exact/reference solver的偏差。

统计 sample error与randomized solver error必须分账。

## 十六、Robust PCA 不是一个唯一算法

“Robust PCA”可能指：

1. robust covariance/eigenspace estimation；
2. low-rank + sparse decomposition；
3. projection pursuit；
4. preprocessing中对 outliers winsorize/trim。

这些对象、loss与 contamination assumptions不同。ordinary PCA的 squared loss对 high-leverage points敏感；删 outlier也不能只凭主图目测，必须声明 contamination model与 selection protocol。

## 十七、AI 接口

### 17.1 Embedding Compression

对 frozen embeddings \(h(x)\in\mathbb R^d\)，PCA可得到

$$
z=P_r(h(x)-\widehat\mu).
$$

必须说明：

- \(\widehat\mu,\widehat P_r\) 用哪些 corpus拟合；
- token、document、user何者是 sampling unit；
- representation checkpoint是否固定；
- downstream task是否参与 \(r\) 选择；
- rare languages/subgroups是否被 low-variance filtering伤害；
- deployment embedding distribution是否 shift。

### 17.2 Whitening 与 Anisotropy

whitened coordinates：

$$
z
=
\widehat\Lambda_r^{-1/2}
\widehat U_r^T(x-\widehat\mu).
$$

小 eigenvalues会放大 noise，因此常用

$$
(\widehat\lambda_j+\varepsilon)^{-1/2}.
$$

\(\varepsilon\) 是 estimator/numerical design，不是无意义 jitter。whitening改善 cosine geometry也可能删除 useful frequency structure；需 downstream验证。

### 17.3 Activation / Feature Analysis

在 layer activations上看到少数主成分解释大量 variance，只说明 second-moment anisotropy。它不自动证明：

- 存在对应 human concept；
- model只使用这些 directions；
- ablation不会触发 nonlinear compensation；
- direction在 prompts/checkpoints间稳定；
- direction具有 causal控制作用。

需要 intervention、probe control、held-out stability与 mechanistic evidence。

## 十八、常见错误

### 错误 1：Explained Variance = Information

variance依 units与second moments；task information依 target。低 variance direction可以完美编码 rare label。

### 错误 2：Eigenvector Sign 变化 = 不稳定

sign flip是同一 subspace。先做 sign/Procrustes alignment或直接比较 projectors。

### 错误 3：Training Reconstruction 好 = Population PCA 好

需要 sample-to-population argument与 independent evaluation。

### 错误 4：SVD Solver 收敛 = Statistical Consistency

solver只逼近 realized matrix的 spectral object。

### 错误 5：PCA 是无监督所以不会泄漏

validation inputs仍会影响 mean、scale与subspace，破坏 inductive evaluation。

## 十九、审计清单

1. population target是 covariance eigenspace还是 realized matrix compression？
2. centering/scaling在哪里拟合？
3. covariance normalization是什么？
4. rank \(r\) 是否 data-dependent？
5. gap \(\lambda_r-\lambda_{r+1}\) 多大？
6. loss比较 basis、projector还是 reconstruction？
7. repeated spectrum如何处理 rotation？
8. tail/dependence assumptions是什么？
9. randomized solver error是否分开？
10. downstream task与shift如何验收？

## 二十、本章掌握标准

### A. 识别

能区分 sample SVD、population covariance、principal direction与principal subspace。

### B. 计算

能对 \(2\times2\) covariance手算 eigenvalues、angle、projected variance与reconstruction risk。

### C. 推导

能重建 maximum variance、minimum reconstruction、SVD equivalence与 excess-risk基本不等式。

### D. 边界

能构造 repeated eigenvalue、low-variance label、leakage与 high-dimensional failure。

### E. AI 迁移

能设计 embedding PCA/whitening pipeline，分开 representation fitting、rank selection、solver approximation、downstream test与shift。

对应训练：[[习题 - PCA 的统计估计与主子空间风险]]  
独立详解：[[解答 - PCA 的统计估计与主子空间风险]]

## 二十一、最小记忆

1. PCA估计的是 covariance principal subspace，不是天然语义；
2. projected variance最大化等价于 orthogonal squared reconstruction最小化；
3. sample PCA由 centered data SVD得到；
4. eigenvalue error看 covariance perturbation；
5. eigenvector/subspace error还除以 eigengap；
6. repeated eigenvalue时比较 projector，不比较任意 basis；
7. excess reconstruction risk可小于方向恢复难度所暗示的程度；
8. rank、centering、scaling与whitening都属于 estimator；
9. PCA preprocessing必须放进 fold；
10. solver convergence、sample consistency与 downstream utility是三种证据。
