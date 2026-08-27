---
type: exercise
status: draft
area: [architecture, attention, tensor-shapes]
topic: "[[Self-Attention、Cross-Attention 与张量形状]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Self-Attention、Cross-Attention 与张量形状]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Self-Attention、Cross-Attention 与张量形状

## A. 识别与复述

### ARCH-SC-A01
用 Q/K/V 来源解释 self-attention 与 cross-attention 的统一与差异。

### ARCH-SC-A02
写出 $T_q,T_k,d_k,d_v$ 下 Q/K/V/A/O shapes。

### ARCH-SC-A03
说明“self”为什么既不等于只看自己，也不等于 $W_Q=W_K=W_V$。

## B. 手算与建模

### ARCH-SC-B01
$B=8,T_q=32,T_k=128,d_k=64,d_v=80$。计算 Q/K/V/A/O 元素数（忽略 heads）。

### ARCH-SC-B02
文本 20 tokens 作为 queries，图像 196 patches 作为 memory，$d_k=64,d_v=128$。给出 score 与 output shapes，并说明谁决定输出 token 数。

### ARCH-SC-B03
给定 $X\in\mathbb R^{10\times512}$、$W_Q,W_K\in\mathbb R^{512\times64}$、$W_V\in\mathbb R^{512\times96}$，列出 self-attention 全链路 shapes。

## C. 推导与证明

### ARCH-SC-C01
证明无位置、无非对称 mask 的 self-attention 对同步 token 置换等变。

### ARCH-SC-C02
证明 cross-attention 对 K/V pair 同步重排不变。

### ARCH-SC-C03
证明 cross-attention 对 query 重排等变，并说明输出行数为何是 $T_q$。

## D. 边界、反例与纠错

### ARCH-SC-D01
构造 K/V 候选轴错位的例子，说明即使 shape 合法也会语义错误。

### ARCH-SC-D02
反驳：“无位置 self-attention 不能表示任何有用函数。”

### ARCH-SC-D03
反驳：“Transformer 有通用逼近定理，所以有限模型一定能学会任意长度算法。”

## E. AI 迁移

### ARCH-SC-E01
为 encoder–decoder 翻译 block 写 batch/head 之前的完整 shape ledger 与两类 padding mask。

### ARCH-SC-E02
为 text-to-image cross-attention 写 Q/K/V 来源、长度、position 与模态尺度审计。

### ARCH-SC-E03
设计置换测试，分别验证 self-attention 等变、memory pair 不变和 position 注入后对称性改变。

## 解答入口

[[解答 - Self-Attention、Cross-Attention 与张量形状]]
