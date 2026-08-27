---
type: exercise
status: draft
area: [architecture, rnn, gru]
topic: "[[GRU、门控递推与 RNN 结构比较]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - GRU、门控递推与 RNN 结构比较]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - GRU、门控递推与 RNN 结构比较

## A. 识别与复述

### ARCH-GRU-A01
按本节约定写出 reset、update、候选与 hidden update 方程。

### ARCH-GRU-A02
解释 update gate 的逐维插值含义和 reset gate 的候选控制含义。

### ARCH-GRU-A03
列出 GRU 与 LSTM 在 recurrent state、门和流式内存上的主要差异。

## B. 手算与建模

### ARCH-GRU-B01
$h_{old}=(2,-1)$，$\tilde h=(0,3)$，$z=(0.25,0.8)$，按本节约定计算 $h_{new}$。

### ARCH-GRU-B02
标量 GRU 候选恒为 4，$z=0.2,h_0=0$，计算 $h_1,h_2$ 并求极限。

### ARCH-GRU-B03
$d_x=20,d_h=32$，计算标准三 affine GRU 参数数和单层单样本流式状态标量数。

## C. 推导与证明

### ARCH-GRU-C01
固定 gate 和候选时，推导 $\partial h_t/\partial h_{t-1}$ 的直接项及跨 $n$ 步保留因子。

### ARCH-GRU-C02
证明一般 $U(r\odot h)\ne r\odot(Uh)$，并写出两者相等的一个充分条件。

### ARCH-GRU-C03
将恒定 $z$ 的标量更新写成指数加权平均并求 half-life。

## D. 边界、反例与纠错

### ARCH-GRU-D01
解释两个都叫 GRU 的库为何可能给出不同输出；至少列四项原因。

### ARCH-GRU-D02
反驳：“GRU 参数少于 LSTM，所以任何设备都一定更快且更准。”

### ARCH-GRU-D03
给出 update convention 相反但表示同一插值的两组方程。

## E. AI 迁移

### ARCH-GRU-E01
设计跨框架权重迁移的单步中间值对齐实验。

### ARCH-GRU-E02
为移动端流式分类比较 vanilla RNN、GRU、LSTM，给出至少五个实测指标。

### ARCH-GRU-E03
解释 GRU 与 selective SSM 的相似直觉和不可混同之处。

## 解答入口

[[解答 - GRU、门控递推与 RNN 结构比较]]

