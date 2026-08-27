---
type: exercise
status: draft
area: [neural-networks/initialization, orthogonal-initialization, dynamical-isometry]
topic: "[[正交初始化与 Dynamical Isometry]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 正交初始化与 Dynamical Isometry]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - 正交初始化与 Dynamical Isometry

## A

### NN-DISO-A01
分别定义 square orthogonal、column-semi-orthogonal 与 row-semi-orthogonal，并说明各自保哪个空间的 norm。

### NN-DISO-A02
区分 mean squared singular value 稳定、condition number 可控与 dynamical isometry。

### NN-DISO-A03
写出 nonlinear feedforward network 的输入—输出 Jacobian product，并指出正交权重之外的 factors。

## B

### NN-DISO-B01
给定 $W\in\mathbb R^{5\times3}$ 且 $W^TW=I_3$，求其 rank、三个 nonzero singular values，并证明它对任意 $x\in\mathbb R^3$ 保长。

### NN-DISO-B02
给定 $W\in\mathbb R^{3\times5}$ 且 $WW^T=I_3$，说明为什么存在二维 kernel，并计算 $W^TW$ 的 eigenvalue multiset。

### NN-DISO-B03
令每层 $W_\ell=gQ_\ell$，其中 $Q_\ell$ 为方阵 orthogonal。求 $L$ 层 linear product 的全部 singular values；当 $g=1.01,L=100$ 时给出数值量级。

## C

### NN-DISO-C01
证明方阵 orthogonal matrices 的乘积仍正交，并据此证明 deep linear Jacobian 的 dynamical isometry。

### NN-DISO-C02
对 $J=D_2W_2D_1W_1$，构造一个 $W_1,W_2$ 正交但 $J$ rank deficient 的 ReLU 例子。

### NN-DISO-C03
证明 $J_\varepsilon=\operatorname{diag}(\sqrt{2-\varepsilon^2},\varepsilon)$ 的 mean squared singular value 为 1，但 condition number 发散。

## D

### NN-DISO-D01
反驳：“矩形 orthogonal initialization 对所有输入方向保长。”

### NN-DISO-D02
反驳：“把 convolution kernel reshape 后做 orthogonal initialization，就证明了 convolution operator isometric。”

### NN-DISO-D03
反驳：“初始化时 $W^TW=I$，普通 SGD 训练后也会保持正交。”

## E

### NN-DISO-E01
设计 small-network 显式 Jacobian SVD 与 large-network matrix-free 谱估计的交叉验证。

### NN-DISO-E02
为含 bottleneck 的 encoder–decoder 定义 restricted dynamical-isometry 审计，明确 relevant subspace。

### NN-DISO-E03
设计 Gaussian、Xavier、Kaiming、orthogonal-gain 四种初始化的 matched comparison，规定必须报告的谱量。

## 解答入口

[[解答 - 正交初始化与 Dynamical Isometry]]
