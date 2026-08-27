---
type: exercise
status: verified
area: [training, optimization, matrix-preconditioning]
topic: "[[Shampoo、逆矩阵根与 Kronecker 预条件]]"
solution: "[[解答 - Shampoo、逆矩阵根与 Kronecker 预条件]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Shampoo、逆矩阵根与 Kronecker 预条件

> [!abstract] 训练目标
> 从 tensor mode Gram 推出 $-1/(2k)$ 次根；能手算左右预条件、建立 inverse-root residual，并把 block、refresh、grafting 与分布式成本写进同一合同。

## A. 识别与复述

### TRN23-A01
比较 full-matrix AdaGrad 与 Shampoo 的 state shape。对 order-$k$ tensor，为什么是每个 mode 一个 $d_i\times d_i$ Gram？

### TRN23-A02
写出经典 Shampoo 的 mode-wise update，并解释矩阵参数为何左右各是 inverse fourth root，而不是 inverse square root。

### TRN23-A03
区分 statistics clock、root-refresh clock 与 apply clock；写出 amortized cost 公式并解释 refresh staleness。

## B. 手算与构造

### TRN23-B01
取 $L=\operatorname{diag}(16,1)$、$R=\operatorname{diag}(1,81)$、$G=\begin{bmatrix}1&1\\1&1\end{bmatrix}$。计算 $L^{-1/4}GR^{-1/4}$。

### TRN23-B02
一个 $2\times3\times4$ gradient tensor 的三个 mode matricization 各是什么 shape？三个 Gram 的 shape、总 state 元素数与 flatten 后 full matrix 元素数分别是多少？

### TRN23-B03
对 $A=\operatorname{diag}(16,1)$、$X=\operatorname{diag}(1/2,1)$、$p=4$，计算 $X^pA-I$ 与 $XA-AX$；若误用 $X=\operatorname{diag}(1/4,1)$ 会发生什么？

## C. 推导与证明

### TRN23-C01
说明多个 mode 的 $-1/(2k)$ 次根为何在 separable/Kronecker 结构中合成整体 half-power；并核对 $k=1$、$k=2$ 两个特例。

### TRN23-C02
对 SPD $A=Q\Lambda Q^T$ 证明 principal inverse $p$-th root 的对称性、正定性和与 $A$ 的交换性；说明 repeated eigenvalue 不破坏 matrix function 的唯一性。

### TRN23-C03
推导 $C_{avg}=C_{stats}+C_{apply}+C_{root}/K+C_{comm}$，并说明为什么它仍不足以描述 refresh step 的 tail latency 与 peak memory。

## D. 边界、反例与纠错

### TRN23-D01
反驳：“inverse-root iteration 只用 GEMM，所以自动比 eigendecomposition 稳定且快。”列出收敛域、scaling、dtype、迭代数与 kernel/通信因素。

### TRN23-D02
构造 eigenvalue 接近零的 Gram，说明无 damping 时 inverse root 如何放大噪声；比较 eigenvalue floor 与 $A+\epsilon I$ 两种修复的语义。

### TRN23-D03
说明 block splitting、grafting 与 fallback 分别删除、替换或保留了什么。为什么使用这些工程机制后不能只报告“Shampoo”一个名字？

## E. AI 迁移

### TRN23-E01
设计 inverse-root 质量日志，至少含 symmetry、finite、$r_{inv}$、$r_{comm}$、eigenvalue floor、dtype、repair 与 update norm。

### TRN23-E02
为大矩阵参数估算 Shampoo 的 persistent state 与 refresh workspace；指出哪些 buffer 会导致峰值显著高于简单的 $\sum_i d_i^2$。

### TRN23-E03
设计 Shampoo 与 AdamW 的 time-to-quality 实验，要求同时改变 refresh period 和 block size，并说明如何避免把更大的调参预算赠送给某一方法。

## 作答与复盘

每题记录 `independent / hinted / copied / blocked / careless`。所有 root 都必须注明 exponent、damping 与 residual，完成后打开 [[解答 - Shampoo、逆矩阵根与 Kronecker 预条件]]。
