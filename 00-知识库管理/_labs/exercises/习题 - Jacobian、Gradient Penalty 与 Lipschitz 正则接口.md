---
type: exercise
status: draft
area: [neural-networks/regularization, jacobian, gradient-penalty, lipschitz]
topic: "[[Jacobian、Gradient Penalty 与 Lipschitz 正则接口]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Jacobian、Gradient Penalty 与 Lipschitz 正则接口]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Jacobian、Gradient Penalty 与 Lipschitz 正则接口

## A

### NN-JGP-A01
写出带 domain、input norm 与 output norm 的 Lipschitz contract。Scalar output 时 derivative operator norm为何等于 input norm 的 dual-gradient norm？

### NN-JGP-A02
区分 loss input-gradient、model Jacobian、operator-norm、WGAN-GP、parameter-gradient 与 spectral-weight control 六个对象。

### NN-JGP-A03
解释 local/empirical/expected sensitivity 与 global/certified Lipschitz 的量词差别。

## B

### NN-JGP-B01
取 $J=\operatorname{diag}(3,1)$。计算 spectral norm、Frobenius norm、$Je_1,Je_2$，并说明单方向 probe 的失败。

### NN-JGP-B02
一个三层串行网络的 spectral norms 为 $(2,0.8,1.5)$，activations 都是 1-Lipschitz。求 product bound。若第二层是 residual $x+0.2G(x)$ 且 $\operatorname{Lip}(G)\le0.8$，求该 block bound。

### NN-JGP-B03
令 $J=\begin{bmatrix}1&2\\0&-1\end{bmatrix}$，$v$ 在 $(1,1),(1,-1),(-1,1),(-1,-1)$ 上均匀。枚举 $\|J^\mathsf Tv\|^2$ 并验证期望等于 $\|J\|_F^2$。

## C

### NN-JGP-C01
在凸 domain 上用线积分证明 $\operatorname{Lip}(f)\le\sup_x\|J_f(x)\|$，并指出非凸 domain 的证明断点。

### NN-JGP-C02
推导 Hutchinson VJP estimator $\mathbb E\|J^\mathsf Tv\|^2=\|J\|_F^2$，并讨论 probe variance 与 operator norm 的差别。

### NN-JGP-C03
由 Taylor 与 dual norm 推导 first-order adversarial bridge $\max_{\|\delta\|\le\rho}\ell(x+\delta)\approx\ell(x)+\rho\|\nabla_x\ell\|_*$，列出余项失效条件。

## D

### NN-JGP-D01
反驳：“训练点上的 Jacobian Frobenius penalty 很小，所以模型已被证明 globally 1-Lipschitz 且 adversarially robust。”

### NN-JGP-D02
比较 WGAN-GP 的 two-sided target-1 penalty、zero-centered penalty 与 one-sided upper penalty；说明任务对象与最优梯度语义。

### NN-JGP-D03
审计 spectral normalization 的 matrix layout、power iteration、residual composition、normalization state 与 mixed precision。

## E

### NN-JGP-E01
设计 local sensitivity—certificate—robust risk 三层验收，规定 clean/shift/attack、norm/radius、probe 与 compute 账。

### NN-JGP-E02
设计 double-backward property tests：finite difference、JVP/VJP、checkpoint、ReLU kink、AMP 与 batch-coupled normalization。

### NN-JGP-E03
给同一模型设计 loss-gradient、logit-Jacobian、probability-Jacobian 与 parameter-gradient 四种 penalty 的 matched-compute 比较，并规定结论边界。

## 解答入口

[[解答 - Jacobian、Gradient Penalty 与 Lipschitz 正则接口]]
