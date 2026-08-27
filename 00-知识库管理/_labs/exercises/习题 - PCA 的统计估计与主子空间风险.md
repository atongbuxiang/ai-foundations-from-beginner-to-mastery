---
type: exercise
status: draft
area: [learning-theory/pca, spectral-estimation, representation-learning]
topic: "[[PCA 的统计估计与主子空间风险]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[PCA 的统计估计与主子空间风险]]"]
related: ["[[解答 - PCA 的统计估计与主子空间风险]]", "[[奇异值分解]]"]
solution: "[[解答 - PCA 的统计估计与主子空间风险]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - PCA 的统计估计与主子空间风险

> [!abstract] 训练目标
> 从 covariance、variational objective 与 centered SVD 三个入口得到同一个 PCA 对象；能计算 reconstruction risk，使用 eigengap解释 subspace stability，并把 preprocessing、rank selection 与 downstream evaluation写成无泄漏协议。

## A. 识别与复述

### LT-PCA-A01

区分 population covariance、sample covariance、top eigenvector、top-(r) eigenspace与任意一组 eigenbasis。为什么 repeated eigenvalue 时应报告 subspace而非单根 eigenvector？

### LT-PCA-A02

分别写出 PCA 的 maximum projected variance、minimum reconstruction error 与 centered-data SVD 三种定义，并注明center/scaling convention。

### LT-PCA-A03

区分 eigenvalue error、basis-vector error、projector error与 excess reconstruction risk；它们何时能、何时不能互相控制？

## B. 手算与数值判断

### LT-PCA-B01

对 covariance
$$
\Sigma=\begin{pmatrix}3&1\\1&3\end{pmatrix},
$$
求 eigenvalues、第一主方向以及 rank-1 population reconstruction risk。

### LT-PCA-B02

两条 one-dimensional subspaces夹角为 (30^\circ)。求对应 orthogonal projectors之差的 operator norm与 squared Frobenius norm。

### LT-PCA-B03

population covariance为 (\operatorname{diag}(4,1))，sample perturbation产生
$$
\widehat\Sigma=\begin{pmatrix}4&0.3\\0.3&1\end{pmatrix}.
$$
求 sample top eigenvector相对 (e_1) 的旋转角，给出degree近似，并说明 eigengap在答案中的作用。

## C. 推导与证明

### LT-PCA-C01

证明：对任意 rank-(r) orthogonal projector (P)，最小化
$$
E\|X-\mu-P(X-\mu)\|^2
$$
等价于最大化 (\operatorname{tr}(P\Sigma))，最优值由 top-(r) eigenspace取得。

### LT-PCA-C02

设 centered data matrix (X_c=U D V^\top)。证明 sample covariance (X_c^\top X_c/n) 的 eigenvectors是 (V)，eigenvalues是 (d_j^2/n)，并解释 scores 与 loadings。

### LT-PCA-C03

设 (P_\star) 与 (\widehat P) 分别为 (\Sigma) 与 (\widehat\Sigma) 的 top-(r) projector。证明
$$
0\le \operatorname{tr}(P_\star\Sigma)-\operatorname{tr}(\widehat P\Sigma)
\le 2r\|\widehat\Sigma-\Sigma\|_{\rm op}.
$$
为什么这个 excess-risk bound不需要显式 eigengap，而 subspace recovery通常需要？

## D. 边界、反例与纠错

### LT-PCA-D01

令 (\Sigma=I_2)。反驳“第一主方向可以被一致恢复”，同时说明 rank-1 reconstruction risk为何仍定义良好。

### LT-PCA-D02

构造一个低variance feature却高度预测 label 的例子，反驳“PCA保留高variance方向，所以一定保留监督任务信息”。

### LT-PCA-D03

解释在全数据上center/standardize/PCA后再做cross-validation为何泄漏。写出合法 fold-local pipeline。

## E. AI 迁移

### LT-PCA-E01

为 4096-dimensional embedding设计 PCA compression实验：选择rank、fit/transform边界、下游指标、reconstruction、whitening、seed与shift审计。

### LT-PCA-E02

比较 PCA compression、whitening与随机投影：分别保留什么几何量，什么时候会放大noise？

### LT-PCA-E03

设计一张 representation PCA report，至少包括 spectrum、eigengap、subspace stability、reconstruction、downstream utility、groups/time split与敏感性分析。
