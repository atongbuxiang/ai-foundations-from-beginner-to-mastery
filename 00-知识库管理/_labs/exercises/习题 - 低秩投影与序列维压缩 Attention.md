---
type: exercise
status: draft
area: [architecture, efficient-attention, low-rank, compression]
topic: "[[低秩投影与序列维压缩 Attention]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 低秩投影与序列维压缩 Attention]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - 低秩投影与序列维压缩 Attention

## A. 识别与复述

### ARCH-LOWRANK-A01
区分 feature/head 维低秩、sequence 维压缩、logit matrix 低秩与 normalized attention matrix 低秩。

### ARCH-LOWRANK-A02
写出 Linformer 型 $E,F\in\mathbb R^{k\times n}$ 对 K/V 的投影、结果 shape 与 attention output。

### ARCH-LOWRANK-A03
为什么低秩序列投影是模型近似，而不是像结合律重排那样的恒等计算？

## B. 手算与建模

### ARCH-LOWRANK-B01
令 $n=1024,k=64,d_h=128$。比较单头 dense $QK^\top$ 与压缩后 $QK'^\top$ 的主乘加数及 score 标量数。

### ARCH-LOWRANK-B02
给定奇异值 $(8,4,2,1,0.5)$，计算最佳 rank-2 近似的谱范数误差与 Frobenius 误差。

### ARCH-LOWRANK-B03
令 $K\in\mathbb R^{4\times2}$、$E\in\mathbb R^{2\times4}$。逐项写出 $K'=EK$，并指出 $E$ 的列对应 token 还是 feature。

## C. 推导与证明

### ARCH-LOWRANK-C01
证明 $\|Q(K-\hat K)^\top\|_F\le \|Q\|_2\|K-\hat K\|_F$，并解释它只控制 logits 的哪一层误差。

### ARCH-LOWRANK-C02
用 Eckart–Young 结论写出最佳 rank-$k$ 近似的谱尾误差；说明 learned shared projection 为什么不必达到逐样本 SVD 最优值。

### ARCH-LOWRANK-C03
证明若压缩矩阵某一行同时使用当前时刻之后的 K/V，则 causal output 可能泄漏未来；给出最小 $n=2$ 代数例子。

## D. 边界、反例与纠错

### ARCH-LOWRANK-D01
构造两个 logit 矩阵 Frobenius 距离很小、但某一行 softmax 输出变化很明显的情形，并解释 margin 的作用。

### ARCH-LOWRANK-D02
反驳：“训练集上平均有效秩低，所以每个样本、每层、每个长度都可安全使用同一个 $k$。”

### ARCH-LOWRANK-D03
解释固定 $E\in\mathbb R^{k\times n_{train}}$ 在 $n_{test}>n_{train}$ 时为何没有天然定义，并列出三种可声明的扩展合同。

## E. AI 迁移

### ARCH-LOWRANK-E01
设计低秩 attention 的谱诊断：采哪些层/头/样本，测哪些矩阵与哪些误差分位数？

### ARCH-LOWRANK-E02
写一个 causal leakage 单元测试，使错误 projection 即使 shape 正确也必然失败。

### ARCH-LOWRANK-E03
设计公平实验，比较 dense、最佳离线 SVD、learned projection 与随机 projection，避免把“可压缩性”与“可学习性”混为一谈。

## 解答入口

[[解答 - 低秩投影与序列维压缩 Attention]]
