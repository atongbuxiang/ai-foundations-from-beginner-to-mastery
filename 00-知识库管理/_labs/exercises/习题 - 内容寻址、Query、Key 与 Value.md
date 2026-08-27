---
type: exercise
status: draft
area: [architecture, attention, content-addressing]
topic: "[[内容寻址、Query、Key 与 Value]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 内容寻址、Query、Key 与 Value]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - 内容寻址、Query、Key 与 Value

## A. 识别与复述

### ARCH-QKV-A01
分别用一句话说明 query、key、value 的角色，并指出哪两个对象必须共享比较维度。

### ARCH-QKV-A02
给定 $Q\in\mathbb R^{T_q\times d_k},K\in\mathbb R^{T_k\times d_k},V\in\mathbb R^{T_k\times d_v}$，写出 score、weight 与 output 的 shape。

### ARCH-QKV-A03
解释“self-attention 中 Q/K/V 同源”为什么不等于 $Q=K=V$。

## B. 手算与建模

### ARCH-QKV-B01
权重为 $(0.6,0.3,0.1)$，values 为 $(1,0),(0,2),(-1,1)$。计算输出。

### ARCH-QKV-B02
设 $Q=\begin{bmatrix}1&0\\0&1\end{bmatrix}$，$K=I_2$，$V=\begin{bmatrix}2&0\\0&4\end{bmatrix}$。忽略缩放，逐行 softmax 后计算输出。

### ARCH-QKV-B03
一个 cross-attention 有 5 个 queries、12 个 memory items，$d_k=8,d_v=16$。列出 Q/K/V/A/O shapes。

## C. 推导与证明

### ARCH-QKV-C01
证明当每行权重非负且和为 1 时，attention 输出位于可见 values 的凸包。

### ARCH-QKV-C02
证明同步置换 key/value pairs 不改变单 query 的 normalized attention 输出。

### ARCH-QKV-C03
比较 hard argmax retrieval 与 softmax retrieval 的可微性，指出唯一最大值区域内与分界处分别发生什么。

## D. 边界、反例与纠错

### ARCH-QKV-D01
反驳：“key 越相似，返回的 value 也越相似。”

### ARCH-QKV-D02
构造两个完全不同的 attention weight vectors，却因 values 退化而给出相同输出。

### ARCH-QKV-D03
反驳：“每个 query 能看全部 tokens，所以模型一定能复制任意一个 token。”

## E. AI 迁移

### ARCH-QKV-E01
为图像 caption decoder 读取 image patches 写一份 Q/K/V 与 mask 合同。

### ARCH-QKV-E02
设计一个最小单元测试，分别验证改变 key 与改变 value 对权重/输出的不同影响。

### ARCH-QKV-E03
把 retrieval-augmented generation 中“问题 tokens 读取 retrieved chunks”写成 shape、候选身份和泄漏审计。

## 解答入口

[[解答 - 内容寻址、Query、Key 与 Value]]
