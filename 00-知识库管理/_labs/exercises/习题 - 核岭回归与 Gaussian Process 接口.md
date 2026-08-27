---
type: exercise
status: draft
area: [learning-theory/kernel-ridge, gaussian-processes]
topic: "[[核岭回归与 Gaussian Process 接口]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[正定核、RKHS 与表示定理]]", "[[多元高斯分布]]"]
related: ["[[解答 - 核岭回归与 Gaussian Process 接口]]", "[[支持向量机、最大间隔与核方法]]"]
solution: "[[解答 - 核岭回归与 Gaussian Process 接口]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 核岭回归与 Gaussian Process 接口

> [!abstract] 训练目标
> 能从 representer theorem推到 Gram solve、谱滤波、effective dimension与 LOOCV；能独立推导 GP conditioning及 KRR–GP尺度匹配，并审计 posterior coverage与近似计算。

## A. 识别与复述

### LT-KGP-A01

区分 KRR estimator、GP prior draw、GP posterior mean、latent posterior variance与 fresh-response predictive variance。

### LT-KGP-A02

解释 finite Gram effective degrees of freedom与 population effective dimension；它们为什么依 kernel、inputs与 \(\lambda\)，且通常不是整数？

### LT-KGP-A03

为什么同一 \(k_x^T(K+cI)^{-1}y\) 不能证明 KRR 与 GP具有相同 uncertainty、coverage与 hyperparameter interpretation？

## B. 手算与数值判断

### LT-KGP-B01

给定
$$
K=\operatorname{diag}(9,1),\quad y=(2,2)^T,\quad n\lambda=1.
$$
求 \(\widehat\alpha\)、training fitted values、两个 shrinkage factors及 \(\operatorname{df}(\lambda)\)。

### LT-KGP-B02

某 fixed linear smoother有 \(e_i=y_i-\widehat y_i=0.3\)、\(S_{ii}=0.75\)。求 LOOCV residual。若该 \(\lambda\) 是从同一 LOOCV curve中挑出的，为什么该 residual公式仍不提供无偏 final performance estimate？

### LT-KGP-B03

取 \(\tau^2=1,\sigma^2=1\)，\(K=\operatorname{diag}(9,1)\)，test point满足 \(k_x=(0.5,0.2)^T\)、\(k(x,x)=1\)。求 latent posterior variance与 fresh-response predictive variance。

## C. 推导与证明

### LT-KGP-C01

用 orthogonal decomposition证明 KRR representer theorem，并推导 \((K+n\lambda I)\alpha=y\) 的 canonical solution。

### LT-KGP-C02

从 joint Gaussian block covariance推导 GP posterior mean与 covariance；再说明 fresh observation为什么额外加 \(\sigma^2\)。

### LT-KGP-C03

精确推导 mean-loss KRR 与 GP posterior mean对应关系 \(n\lambda=\sigma^2/\tau^2\)，并给出 sum-loss convention下的对应。

## D. 边界、反例与纠错

### LT-KGP-D01

反驳“GP prior从 covariance RKHS中随机抽一个有限范数函数”。用 Mercer coordinates解释常见 infinite-dimensional GP sample path为何可能几乎必然不在 RKHS。

### LT-KGP-D02

区分 jitter、observation noise、ridge与 low-rank approximation。给出把它们混写会造成的两个 uncertainty错误。

### LT-KGP-D03

反驳“marginal likelihood自动防止 overfitting并给最优 kernel”。讨论 multimodality、empirical Bayes、misspecification与 adaptive comparison。

## E. AI 迁移

### LT-KGP-E01

审计“frozen embedding + GP head”的 uncertainty：哪些 randomness被 posterior覆盖，哪些来自 representation/pretraining/hyperparameter/shift而未被覆盖？

### LT-KGP-E02

为 \(n=10^6\) 的 kernel regression选择 Nyström、random features或 iterative solve，写出计算、谱 approximation、seed与 validation验收字段。

### LT-KGP-E03

Bayesian optimization用 posterior variance选下一个昂贵实验。设计一份安全审计，覆盖 kernel misspecification、coverage、hyperparameter refit、acquisition adaptivity与 constraint violation。
