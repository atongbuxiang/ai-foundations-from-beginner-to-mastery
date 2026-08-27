---
type: exercise
status: draft
area: [architecture, attention, matrix-rank]
topic: "[[Attention 矩阵的秩、瓶颈与有效秩]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Attention 矩阵的秩、瓶颈与有效秩]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Attention 矩阵的秩、瓶颈与有效秩

## A. 识别与复述

### ARCH-RANK-A01
分别写出 logit、weight、output 的 rank 上界或不能直接给出的界。

### ARCH-RANK-A02
定义 stable rank 与谱熵 effective rank，并说明二者不可混报的原因。

### ARCH-RANK-A03
说明 strict rank、numerical rank、conditioning 和 effective rank 的区别。

## B. 手算与建模

### ARCH-RANK-B01
对 $L=\begin{bmatrix}0&0\\0&1\end{bmatrix}$ 计算 rank，并证明 row-softmax 后满秩。

### ARCH-RANK-B02
对奇异值 $(4,2,0)$ 计算 strict rank、stable rank 和谱熵 effective rank。

### ARCH-RANK-B03
$A$ 满秩 $4\times4$，$V\in\mathbb R^{4\times2}$ 的两列共线。给出 $AV$ 的最大可能 rank。

## C. 推导与证明

### ARCH-RANK-C01
证明 factorized normalized linear attention $A=D^{-1}\Phi_Q\Phi_K^T$ 在 D 可逆时 rank 不超过 feature width r。

### ARCH-RANK-C02
证明 finite-logit inclusive causal softmax attention 满秩，并给出它仍可病态的构造思路。

### ARCH-RANK-C03
推导多头拼接输出 rank 的上界 $\min(T_q,\sum_r\operatorname{rank}O_r)$。

## D. 边界、反例与纠错

### ARCH-RANK-D01
反驳：“$d_k<T$，所以 softmax attention matrix 必低秩。”

### ARCH-RANK-D02
构造严格满秩但 stable rank 接近 1 的对角矩阵族。

### ARCH-RANK-D03
解释 pure-attention rank-collapse theorem 为何不能直接用于含 residual/MLP 的完整 Transformer。

## E. AI 迁移

### ARCH-RANK-E01
设计 per-layer/per-head logit/weight/output/hidden spectral audit。

### ARCH-RANK-E02
为 exact softmax 与 feature-rank r 的 linear attention 设计表达—质量—成本扫描。

### ARCH-RANK-E03
评审声明“causal attention 满秩，所以 Decoder-only 更强”，按 I/T/E/H/O 拆分。

## 解答入口

[[解答 - Attention 矩阵的秩、瓶颈与有效秩]]
