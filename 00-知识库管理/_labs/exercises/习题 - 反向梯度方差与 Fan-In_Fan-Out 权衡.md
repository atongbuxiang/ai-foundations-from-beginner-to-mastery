---
type: exercise
status: draft
area: [neural-networks/initialization, gradient-propagation]
topic: "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 反向梯度方差与 Fan-In_Fan-Out 权衡|解答 - 反向梯度方差与 Fan-In/Fan-Out 权衡]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - 反向梯度方差与 Fan-In/Fan-Out 权衡

## A

### NN-FAN-A01
写出 affine+activation 一层的 forward 与 reverse 公式，并标出两条求和长度。

### NN-FAN-A02
定义 $c(q)$、$d(q)$、$\chi_f$、$\chi_b$，说明各自统计对象。

### NN-FAN-A03
区分 gradient second moment、gradient norm、Jacobian Frobenius scale 与 singular spectrum。

## B

### NN-FAN-B01
对 $n_{\mathrm{in}}=64,n_{\mathrm{out}}=256$ 的 linear layer，计算 fan-in、fan-out、Xavier 三种 variance 下的 $\chi_f,\chi_b$。

### NN-FAN-B02
计算 $0.95^{100}$ 与 $1.05^{100}$，解释单层小偏差的深度效应。

### NN-FAN-B03
给定 ReLU bottleneck 宽度 $512\to128\to512$，逐层计算 fan-in He 初始化的 backward multiplier。

## C

### NN-FAN-C01
从 differential/VJP 推导反向二阶矩递推，并逐项说明交叉项为何消失。

### NN-FAN-C02
推导单一 scalar variance 同时保持前向/反向所需的可兼容条件。

### NN-FAN-C03
构造平均平方增益为 1、但 condition number 任意大的线性 Jacobian。

## D

### NN-FAN-D01
指出 gradient-independence approximation 在真实反向传播中为何不严格。

### NN-FAN-D02
反驳“梯度 norm 没变，所以没有方向性梯度消失”。

### NN-FAN-D03
解释 residual、normalization 与 mean/sum loss reduction 如何改写 plain-chain 结论。

## E

### NN-FAN-E01
设计 width-profile×mode×activation 的前向/反向传播实验矩阵。

### NN-FAN-E02
为 distributed mixed-precision 训练建立 gradient-scale 账本。

### NN-FAN-E03
给出从 scalar moment 诊断升级到 Jacobian spectrum 诊断的停止/升级规则。

## 解答入口

[[解答 - 反向梯度方差与 Fan-In_Fan-Out 权衡|解答 - 反向梯度方差与 Fan-In/Fan-Out 权衡]]

