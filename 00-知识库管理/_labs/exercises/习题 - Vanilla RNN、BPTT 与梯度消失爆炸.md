---
type: exercise
status: draft
area: [architecture, rnn, optimization]
topic: "[[Vanilla RNN、BPTT 与梯度消失爆炸]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Vanilla RNN、BPTT 与梯度消失爆炸]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Vanilla RNN、BPTT 与梯度消失爆炸

## A. 识别与复述

### ARCH-RNN-A01
写出 vanilla RNN 的前向方程、所有矩阵形状和时间共享的参数。

### ARCH-RNN-A02
解释 BPTT 与普通反向传播的关系，以及共享参数为何产生跨时间求和。

### ARCH-RNN-A03
区分状态爆炸、梯度爆炸、梯度消失和随机梯度噪声。

## B. 手算与建模

### ARCH-RNN-B01
标量线性 RNN $h_t=wh_{t-1}+x_t$，$w=1/2,h_0=0,x=(2,0)$，损失 $L=h_2^2/2$。计算 $h_1,h_2,dL/dh_1,dL/dw$。

### ARCH-RNN-B02
对 $h_t=\tanh(wh_{t-1})$，$w=2,h_0=0.1,T=2$，数值计算状态与 $dh_2/dh_0$（保留三位小数）。

### ARCH-RNN-B03
梯度 $g=(3,4)$，阈值 $\tau=2$。计算 global norm clipping 后的梯度；再比较 elementwise clip 到 $[-2,2]$。

## C. 推导与证明

### ARCH-RNN-C01
推导 $g_t=\partial\ell_t/\partial h_t+J_{t+1}^Tg_{t+1}$。

### ARCH-RNN-C02
推导 $dL/dW_{hh}=\sum_t\delta_t h_{t-1}^T$ 并写出 $\delta_t$。

### ARCH-RNN-C03
证明若所有 $\|J_k\|_2\le\rho<1$，则距离 $n$ 的状态梯度范数至多乘 $\rho^n$。

## D. 边界、反例与纠错

### ARCH-RNN-D01
给出 $\rho(W)=0$ 但 $\|W\|_2$ 很大的矩阵，说明谱半径不能描述有限步 transient amplification。

### ARCH-RNN-D02
反驳：“只要对梯度裁剪，RNN 就能学习任意长依赖。”

### ARCH-RNN-D03
解释为什么 $\prod_k\|J_k\|>1$ 不能证明实际向量梯度必爆炸，并给出方向抵消例子。

## E. AI 迁移

### ARCH-RNN-E01
设计 per-time gradient probe，区分任务不需要长程与梯度到不了早期。

### ARCH-RNN-E02
审计 truncated BPTT 长度 $K$：列出 forward state、反向图、目标偏差和显存四项。

### ARCH-RNN-E03
写出混合精度训练中 global norm clipping 的正确顺序与需要记录的监控量。

## 解答入口

[[解答 - Vanilla RNN、BPTT 与梯度消失爆炸]]

