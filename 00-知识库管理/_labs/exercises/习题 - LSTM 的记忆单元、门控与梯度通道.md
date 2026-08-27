---
type: exercise
status: draft
area: [architecture, rnn, lstm]
topic: "[[LSTM 的记忆单元、门控与梯度通道]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - LSTM 的记忆单元、门控与梯度通道]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - LSTM 的记忆单元、门控与梯度通道

## A. 识别与复述

### ARCH-LSTM-A01
写出现代标准 LSTM 的四个门/候选方程、cell update 和 hidden readout。

### ARCH-LSTM-A02
分别说明 forget、input、output gate 的作用；为什么它们不是概率分布？

### ARCH-LSTM-A03
解释 cell state 与 hidden state 的语义和流式保存差别。

## B. 手算与建模

### ARCH-LSTM-B01
$c_0=2$，$(f,i,\tilde c,o)=(0.5,0.25,-0.4,0.8)$，计算 $c_1,h_1$。

### ARCH-LSTM-B02
无写入且恒定 $f=0.98$，计算 50 步保留比例和 half-life。

### ARCH-LSTM-B03
$d_x=20,d_h=32$，计算标准合并 affine LSTM 的 recurrent cell 参数数与每样本流式状态标量数。

## C. 推导与证明

### ARCH-LSTM-C01
在固定门/候选的局部视角下推导 $\partial c_T/\partial c_t$ 的直接项。

### ARCH-LSTM-C02
由 $f^{\tau}=1/2$ 推导 half-life，并给出 $f\to1^-$ 时的一阶近似。

### ARCH-LSTM-C03
说明完整 $dc_t/dc_{t-1}$ 为何不仅是 $f_t$；画出至少一条经 $h_{t-1}$ 回到 gates 的路径。

## D. 边界、反例与纠错

### ARCH-LSTM-D01
用数值反驳：“forget gate 只要 0.99 就可永久保留。”

### ARCH-LSTM-D02
构造 $f=i=1$ 时 cell magnitude 线性增长的例子，说明门值不构成凸组合。

### ARCH-LSTM-D03
解释为何较大 forget bias 不能保证任务上的长期记忆更好。

## E. AI 迁移

### ARCH-LSTM-E01
写一套跨框架 LSTM 权重迁移核对清单。

### ARCH-LSTM-E02
设计最小单元测试分别触发保持、清空、写入和关闭输出四种行为。

### ARCH-LSTM-E03
为流式 LSTM 服务计算 state memory，并说明 bidirectional LSTM 为什么不满足同样在线合同。

## 解答入口

[[解答 - LSTM 的记忆单元、门控与梯度通道]]

