---
type: exercise
status: draft
area: [architecture, state-space-models, mamba]
topic: "[[选择性状态空间、Mamba 与证据边界]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 选择性状态空间、Mamba 与证据边界]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - 选择性状态空间、Mamba 与证据边界

## A. 识别与复述

### ARCH-MAMBA-A01
写出 selective SSM 的抽象方程，并指出哪些参数依赖 $x_t$。

### ARCH-MAMBA-A02
解释 $\Delta_t,B_t,C_t$ 分别如何提供选择性直觉。

### ARCH-MAMBA-A03
为什么 Mamba 没有固定 convolution kernel，却仍可 parallel scan？

## B. 手算与建模

### ARCH-MAMBA-B01
标量 $A=-1$，分别取 $\Delta=0.1,1,3$，计算 retention $e^{-\Delta}$。

### ARCH-MAMBA-B02
$h_t=a_th_{t-1}+b_t$，$h_0=0$，$(a_1,b_1)=(0.5,2)$、$(a_2,b_2)=(0.1,3)$，顺序计算并用 pair composition 复算。

### ARCH-MAMBA-B03
若 $L=4096,D=512,N=16$，写 selective scan core 的量级 $LDN$；与 $L^2D$ 的 dense attention score 量级比较，不必把 MAC 与 FLOP 混用。

## C. 推导与证明

### ARCH-MAMBA-C01
展开 time-varying selective recurrence，写出 $x_j$ 到 $y_t$ 的系数并证明它依赖沿途输入。

### ARCH-MAMBA-C02
证明 input-dependent affine state update 仍满足 pair scan 的结合律。

### ARCH-MAMBA-C03
对 $A=-\alpha<0$ 推导 retention half-life 与 $\Delta$ 的关系。

## D. 边界、反例与纠错

### ARCH-MAMBA-D01
反驳：“复杂度对 $L$ 线性，所以任意长度上下文都能精确记住。”

### ARCH-MAMBA-D02
构造一个 selective gate 把重要信息错误遗忘的例子，说明机制不等于保证。

### ARCH-MAMBA-D03
解释为何论文的训练吞吐优势不能直接推出 batch=1 单 token latency 优势。

## E. AI 迁移

### ARCH-MAMBA-E01
设计 selective scan 与 sequential recurrence 的正确性/精度测试。

### ARCH-MAMBA-E02
为 Mamba vs Transformer 写一张公平 benchmark protocol。

### ARCH-MAMBA-E03
把一句“Mamba 比 Attention 更快更强”拆成至少六条可核验断言并指定证据类型。

## 解答入口

[[解答 - 选择性状态空间、Mamba 与证据边界]]

