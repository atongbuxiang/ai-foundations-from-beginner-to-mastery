---
type: exercise
status: draft
area: [learning-theory/latent-variable-models, mixture-models, em]
topic: "[[潜变量模型、混合模型与 EM]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[潜变量模型、混合模型与 EM]]"]
related: ["[[解答 - 潜变量模型、混合模型与 EM]]", "[[模型可辨识性、选择与 Misspecification]]"]
solution: "[[解答 - 潜变量模型、混合模型与 EM]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 潜变量模型、混合模型与 EM

> [!abstract] 训练目标
> 从 marginal likelihood推导 ELBO/KL恒等式与 EM monotonicity；能手算 Gaussian-mixture responsibilities/updates，并区分 bound改善、likelihood收敛、parameter收敛、global optimality和statistical correctness。

## A. 识别与复述

### LT-EM-A01

区分 observed variable (X)、latent variable (Z)、parameter (\theta)、posterior (p_\theta(z\mid x))、complete-data likelihood与observed-data likelihood。

### LT-EM-A02

比较 exact EM、generalized EM、variational EM、Monte Carlo EM与amortized inference：E-step与M-step各自精确优化什么？

### LT-EM-A03

区分 likelihood monotonicity、likelihood-value convergence、parameter-iterate convergence、stationary point、local/global maximum与statistical consistency。

## B. 手算与数值判断

### LT-EM-B01

two-component Gaussian mixture中，(\pi_1=\pi_2=1/2)，(\mu_1=0,mu_2=2)，共同variance为1。求 (x=0) 与 (x=2) 属于component 2的responsibility。

### LT-EM-B02

数据 (x=(-2,0,2))，对component 2的responsibilities为 ((0.1,0.5,0.9))。求该component的new mixing weight、mean与variance M-step updates。

### LT-EM-B03

计算 (a=1000,b=999) 时的 (log(e^a+e^b))，写成数值稳定的 log-sum-exp形式并给出近似值。

## C. 推导与证明

### LT-EM-C01

从任意 auxiliary distribution (q(z)) 推导
$$
\log p_\theta(x)=\mathcal F(q,\theta)+D_{\rm KL}(q\|p_\theta(\cdot\mid x)).
$$
说明E-step为何使bound tight。

### LT-EM-C02

证明 exact EM 与 generalized EM 都使 observed log-likelihood不下降，并明确 proof 中固定的 (q) 是什么。

### LT-EM-C03

推导 full-covariance Gaussian mixture的 (\pi_k,\mu_k,\Sigma_k) M-step updates，并解释每个式子的weighted sufficient-statistic含义。

## D. 边界、反例与纠错

### LT-EM-D01

证明 mixture likelihood在 component label permutation下不变。为什么component 1的参数均值可能毫无意义？

### LT-EM-D02

说明 unconstrained Gaussian mixture likelihood如何通过 variance collapse趋于无穷。它与普通local maximum是同一问题吗？

### LT-EM-D03

反驳“EM likelihood收敛，所以parameters一定收敛且得到MLE”。列出至少五个缺口。

## E. AI 迁移

### LT-EM-E01

把 mixture-of-experts 写成 latent routing model，说明 exact posterior routing、learned router与hard routing分别改变什么objective/approximation。

### LT-EM-E02

解释 VAE training与exact EM的联系和差别：latent posterior、ELBO、amortization gap、decoder M-step与stochastic gradients。

### LT-EM-E03

为弱监督latent-label模型设计审计：identifiability、anchor assumptions、initialization、local optima、calibration、label semantics与held-out validation。
