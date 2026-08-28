---
type: solution
status: draft
area: [learning-theory/pca, spectral-estimation, representation-learning]
topic: "[[PCA 的统计估计与主子空间风险]]"
exercise: "[[习题 - PCA 的统计估计与主子空间风险]]"
prerequisites: ["[[PCA 的统计估计与主子空间风险]]"]
related: ["[[奇异值分解]]", "[[协方差、相关性与条件期望]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - PCA 的统计估计与主子空间风险

> [!warning] 解题原则
> PCA至少有三个对象层次：population covariance (\Sigma)、sample covariance (\widehat\Sigma)、数值算法输出。先声明center/scaling与target rank，再区分 eigenbasis、subspace projector和reconstruction risk；没有 eigengap时，低风险不等于方向可恢复。

## A. 识别与复述

### LT-PCA-A01

若 (X\in\mathbb R^d)，(\mu=E[X])，population covariance为

$$
\Sigma=E[(X-\mu)(X-\mu)^\top].
$$

样本均值 (\bar X) 下常用

$$
\widehat\Sigma_n
=\frac1n\sum_{i=1}^n(X_i-\bar X)(X_i-\bar X)^\top;
$$

若使用 (1/(n-1))，eigenvectors不变、eigenvalues整体缩放。

top eigenvector是满足 (\Sigma u_1=\lambda_1u_1) 的unit vector；若 (\lambda_1>\lambda_2)，它只在sign意义下唯一。top-(r) eigenspace为top-(r) eigenvectors张成的space，其 projector

$$
P_r=U_rU_r^\top
$$

不依赖basis内rotation。若 (\lambda_j=\lambda_{j+1})，对应 eigenspace内任意orthonormal rotation都是合法eigenbasis；单根 vector不是可识别对象。若 boundary gap (\lambda_r-\lambda_{r+1}>0)，top-(r) subspace仍唯一。

### LT-PCA-A02

令 (P=UU^\top)，(U^\top U=I_r)。population maximum variance：

$$
\max_{U^\top U=I_r}
E\|U^\top(X-\mu)\|^2
=
\max_U\operatorname{tr}(U^\top\Sigma U).
$$

minimum reconstruction：

$$
\min_{P=P^\top=P^2,\operatorname{rank}P=r}
E\|(I-P)(X-\mu)\|^2.
$$

对centered data matrix (X_c\in\mathbb R^{n\times d})，SVD

$$
X_c=UDV^\top
$$

中 (V_r) 是 sample principal directions，(X_cV_r=U_rD_r) 是scores。若先逐feature standardize，做的是 correlation-scale PCA；这与raw covariance PCA是不同问题，必须声明。

### LT-PCA-A03

- eigenvalue error：如 (|\widehat\lambda_j-\lambda_j|)；Weyl给出上界 (\|\widehat\Sigma-\Sigma\|_{\rm op})。
- basis-vector error：如 (\min_{s=\pm1}\|\widehat u-su\|)；只在simple eigenvalue下有意义。
- projector/subspace error：(\|\widehat P-P\|_{\rm op}) 或 Frobenius norm；尊重basis rotation。
- excess reconstruction risk：
  $$
  \operatorname{tr}(P\Sigma)-\operatorname{tr}(\widehat P\Sigma).
  $$

covariance error可直接控制 eigenvalues与excess risk；要把它转为subspace error，一般要除以 eigengap。反向不总成立：在 isotropic covariance中任何方向都有最优risk，projectors可相距很远而excess risk为零。

## B. 手算与数值判断

### LT-PCA-B01

特征多项式：

$$
\det(\Sigma-\lambda I)
=(3-\lambda)^2-1
=(\lambda-4)(\lambda-2).
$$

所以 (\lambda_1=4,\lambda_2=2)。对应 unit eigenvectors可取

$$
u_1=\frac1{\sqrt2}(1,1)^\top,
\qquad
u_2=\frac1{\sqrt2}(1,-1)^\top.
$$

rank-1 reconstruction丢掉第二方向，population risk为 discarded eigenvalue之和：

$$
\boxed{R(P_1)=\lambda_2=2.}
$$

### LT-PCA-B02

one-dimensional subspaces的principal angle为 (\theta) 时，projector差满足

$$
\|P-\widehat P\|_{\rm op}=\sin\theta,
$$

$$
\|P-\widehat P\|_F^2=2\sin^2\theta.
$$

代入 (\theta=30^\circ)：

$$
\boxed{\|P-\widehat P\|_{\rm op}=1/2},
$$

$$
\boxed{\|P-\widehat P\|_F^2=2(1/2)^2=1/2}.
$$

### LT-PCA-B03

对 symmetric (2\times2) matrix

$$
\begin{pmatrix}a&b\\b&d\end{pmatrix},
$$

principal axis相对第一坐标轴的角度满足

$$
\tan(2\theta)=\frac{2b}{a-d}.
$$

这里

$$
\tan(2\theta)=\frac{0.6}{3}=0.2,
$$

所以

$$
\theta=\frac12\arctan(0.2)
\approx0.09870\text{ rad}
\approx\boxed{5.65^\circ}.
$$

off-diagonal perturbation为0.3，population gap为3，small-angle近似 (\theta\approx0.3/3=0.1) rad。相同perturbation若gap更小，会产生更大rotation。

## C. 推导与证明

### LT-PCA-C01

令 (Y=X-\mu)。因 (P=P^\top=P^2)，(I-P)也是orthogonal projector：

$$
\begin{aligned}
E\|Y-PY\|^2
&=E[Y^\top(I-P)Y]\\
&=\operatorname{tr}((I-P)E[YY^\top])\\
&=\operatorname{tr}(\Sigma)-\operatorname{tr}(P\Sigma).
\end{aligned}
$$

第一项固定，故min reconstruction等价于max captured variance。

写 $\Sigma=\sum_{j=1}^d\lambda_ju_ju_j^\top$，$\lambda_1\ge\cdots\ge\lambda_d$。则

$$
\operatorname{tr}(P\Sigma)
=\sum_{j=1}^d\lambda_j u_j^\top Pu_j.
$$

令 (a_j=u_j^\top Pu_j=\|Pu_j\|^2)，有 (0\le a_j\le1) 且

$$
\sum_ja_j=\operatorname{tr}P=r.
$$

为了最大化加权和，应把全部weight放在最大的 (r) 个eigenvalues上，因此

$$
\max_P\operatorname{tr}(P\Sigma)=\sum_{j=1}^r\lambda_j,
$$

由top-(r) eigenspace projector取得；最小reconstruction risk为

$$
\boxed{\sum_{j=r+1}^d\lambda_j}.
$$

### LT-PCA-C02

由 (X_c=UDV^\top)：

$$
\widehat\Sigma
=\frac1nX_c^\top X_c
=\frac1nVDU^\top UDV^\top
=V\frac{D^2}{n}V^\top.
$$

故右 singular vectors (v_j) 是 sample covariance eigenvectors，eigenvalues为

$$
\widehat\lambda_j=d_j^2/n.
$$

loadings/directions (V_r) 给出原 feature space中的axes；projected coordinates（scores）为

$$
X_cV_r=U_rD_r.
$$

若 covariance使用 (1/(n-1))，只把 eigenvalues改为 (d_j^2/(n-1))。

### LT-PCA-C03

记 (E=\widehat\Sigma-\Sigma)。因 (P_\star) maximizes (\operatorname{tr}(P\Sigma))，左侧非负。又因 (\widehat P) maximizes sample captured variance，

$$
\operatorname{tr}(\widehat P\widehat\Sigma)
\ge
\operatorname{tr}(P_\star\widehat\Sigma).
$$

于是

$$
\begin{aligned}
&\operatorname{tr}(P_\star\Sigma)-\operatorname{tr}(\widehat P\Sigma)\\
&=\operatorname{tr}((P_\star-\widehat P)\widehat\Sigma)
-\operatorname{tr}((P_\star-\widehat P)E)\\
&\le
\operatorname{tr}((\widehat P-P_\star)E).
\end{aligned}
$$

用 trace duality：

$$
|\operatorname{tr}((\widehat P-P_\star)E)|
\le
\|\widehat P-P_\star\|_*\|E\|_{\rm op}.
$$

两个rank-(r) projectors之差的nuclear norm至多 (2r)，故

$$
\boxed{
0\le R(\widehat P)-R(P_\star)
\le2r\|\widehat\Sigma-\Sigma\|_{\rm op}.
}
$$

这个结论只问 sample-chosen subspace丢失了多少population variance；gap为零时很多远离的subspaces也可能同样最优。要恢复特定subspace orientation，Davis–Kahan型bound通常含

$$
\frac{\|E\|_{\rm op}}{\lambda_r-\lambda_{r+1}},
$$

所以需要positive boundary eigengap。

## D. 边界、反例与纠错

### LT-PCA-D01

若 (\Sigma=I_2)，每个unit vector (u) 都满足 (u^\top\Sigma u=1)。没有population-defined“第一方向”；sample covariance的微小随机扰动可以把top vector指向任意方向，因此不能对某个固定vector一致恢复。

但任意rank-1 projector的reconstruction risk都为

$$
\operatorname{tr}(\Sigma)-\operatorname{tr}(P\Sigma)=2-1=1.
$$

所以 optimal risk明确，argmin不唯一。这正是risk consistency不推出parameter/subspace consistency的例子。

### LT-PCA-D02

令 (Y\in\{-1,+1\}) 等概率，

$$
X_1=100Z,
\qquad Z\sim N(0,1),
$$

$$
X_2=0.1Y.
$$

则 (\operatorname{Var}(X_1)=10^4)，(\operatorname{Var}(X_2)=0.01)。rank-1 PCA几乎只保留 (X_1)，但 (X_1\perp Y)，而 (Y=\operatorname{sign}(X_2)) 可由低variance feature完美预测。PCA优化unsupervised reconstruction，不知道label utility。

### LT-PCA-D03

若先在全数据上估计mean、scale、principal directions，validation rows已经影响 representation；fold score不再对应“未见这些rows的pipeline”。合法做法对每个 training fold (T_k)：

1. 只在 (T_k) 拟合imputer/mean/scale；
2. 只在 transformed (T_k) 拟合PCA/rank rule；
3. 用这些fitted transformations变换 (T_k,V_k)；
4. 只在 transformed (T_k) 拟合downstream model；
5. 在 (V_k) score；
6. rank selection在inner loop完成，outer fold只评价。

## E. AI 迁移

### LT-PCA-E01

一个合格实验协议：

- unit：按user/document/time group切分，避免near-duplicate泄漏；
- preprocessing：fold-local centering；是否scale要基于embedding语义声明；
- candidates：(r\in\{32,64,128,256,512\})，在inner validation选择；
- fit：只在inner training embeddings求PCA；固定randomized-SVD seed/tolerance；
- metrics：variance retained、reconstruction MSE、subspace stability，以及retrieval/classification/calibration等真实downstream metrics；
- whitening：单独作为candidate，设置eigenvalue floor，报告是否放大小eigenvalue noise；
- final：锁定rank/pipeline后在outer groups/time split评价，再用全部development data refit；
- shift：新domain/time下重测spectrum、reconstruction与task utility。

不能只用explained-variance threshold宣布compression成功。

### LT-PCA-E02

- PCA compression优先保留sample variance最大的subspace；通常不保pairwise distances的uniform guarantee，也不知晓labels。
- whitening在PCA coordinates中乘 (\widehat\lambda_j^{-1/2})，令sample covariance近似identity；它改变距离并会放大小 eigenvalue directions的estimation noise，需regularized floor。
- 随机投影在适当dimension下可用Johnson–Lindenstrauss机制近似保有限点集pairwise distances；不利用data covariance，也不最小化同rank reconstruction error。

若目的为Euclidean retrieval，随机投影的distance contract可能更直接；若目的为reconstruction/compression，PCA更自然；若downstream需要equalized scales，regularized whitening可能有用但风险最大。

### LT-PCA-E03

最小report应包括：

1. data unit、center/scale与fit split；
2. eigenvalue scree、cumulative variance与candidate ranks；
3. boundary eigengaps与bootstrap/subsample projector stability；
4. train/held-out reconstruction及group分解；
5. downstream task proper metrics、calibration与latency；
6. whitening/eigenvalue-floor设置；
7. randomized solver seed、iterations与residual；
8. time/domain shift下 spectrum与utility漂移；
9. low-variance task signal敏感性；
10. rank选择是否与final test严格隔离。
