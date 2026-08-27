---
type: exercise
status: draft
area: [architecture, moe, capacity, dispatch]
topic: "[[Expert Capacity、Dispatch 与 Token Dropping]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Expert Capacity、Dispatch 与 Token Dropping]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Expert Capacity、Dispatch 与 Token Dropping

## A. 识别与复述

### ARCH-DISPATCH-A01
定义 assignment matrix、专家负载与总 assignment 数。

### ARCH-DISPATCH-A02
区分 drop、pad 与 dropless 的精确定义。

### ARCH-DISPATCH-A03
说明 token-choice 与 expert-choice 分别固定 assignment matrix 的哪一方向。

## B. 手算与建模

### ARCH-DISPATCH-B01
$T=8,E=3,k=1,\alpha=1$ 时计算 $C$；对负载 $[4,2,2]$ 算 drop 数、空槽数与利用率。

### ARCH-DISPATCH-B02
$T=12,E=4,k=2,\alpha=1.25$，计算容量与总槽位，并给出无 drop 所需的最大负载条件。

### ARCH-DISPATCH-B03
给定 $A=\begin{bmatrix}1&1&0\\0&1&1\\1&0&1\end{bmatrix}$，计算每 token 激活数、每专家负载和总 assignment。

## C. 推导与证明

### ARCH-DISPATCH-C01
证明 token-choice Top-k 下 $\sum_jn_j=Tk$。

### ARCH-DISPATCH-C02
推导 fixed-capacity padded execution 的槽位利用率公式。

### ARCH-DISPATCH-C03
用行/列约束证明 Expert Choice 不保证每 token 恰好激活 $k$ 个专家。

## D. 边界、反例与纠错

### ARCH-DISPATCH-D01
反驳：“dropless 等于完全没有 padding 与负载问题。”

### ARCH-DISPATCH-D02
构造先到先得 drop 对 token 位置产生系统性偏差的例子。

### ARCH-DISPATCH-D03
说明 capacity policy 为什么可能改变模型函数，而不只是运行时。

## E. AI 迁移

### ARCH-DISPATCH-E01
设计一个 permutation/inverse-permutation 正确性测试。

### ARCH-DISPATCH-E02
设计 capacity factor sweep，要求同时报告质量与系统指标。

### ARCH-DISPATCH-E03
比较 token-choice 与 expert-choice 时应控制哪些变量？

## 解答入口

[[解答 - Expert Capacity、Dispatch 与 Token Dropping]]

