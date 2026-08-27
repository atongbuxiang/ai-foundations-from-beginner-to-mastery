---
type: exercise
status: verified
area: [training, optimization, momentum]
topic: "[[Momentum、EMA、偏差修正与框架约定]]"
solution: "[[解答 - Momentum、EMA、偏差修正与框架约定]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Momentum、EMA、偏差修正与框架约定

## A. 识别与复述

### TRN04-A01
写出 gradient-buffer、parameter-velocity 和 gradient-EMA 三种更新，并注明 state 单位。

### TRN04-A02
常 LR 下三者的尺度字典是什么？

### TRN04-A03
PyTorch SGD 的首个 momentum buffer 与 dampening 有何特殊语义？

## B. 手算与构造

### TRN04-B01
$g_0=2,g_1=-1,\mu=0.9,\eta=0.1$。从零状态算两步 buffer、velocity 与 parameter updates。

### TRN04-B02
同一梯度序列计算 EMA $m_t=0.9m_{t-1}+0.1g_t$；求匹配 buffer update 的 $\alpha$。

### TRN04-B03
恒定 $g=3,\mu=0.8$，写出 $b_0,b_1,b_2$ 和极限；再算 bias-corrected EMA。

## C. 推导与证明

### TRN04-C01
归纳证明 $b_t=\sum_{k=0}^t\mu^{t-k}g_k$。

### TRN04-C02
常 LR 下证明 $v_t=-\eta b_t$；变化 LR 下推导 $v_t=\mu(\eta_t/\eta_{t-1})v_{t-1}-\eta_tg_t$。

### TRN04-C03
证明零初始化 EMA 的权重和是 $1-\mu^{t+1}$，并说明 bias correction 的含义。

## D. 边界、反例与纠错

### TRN04-D01
给出 LR 在相邻两步变化时 buffer 与朴素 velocity 不再相同的数值反例。

### TRN04-D02
反驳：“EMA 一定降低训练噪声，因此一定改善泛化。”指出 filtering、lag 与因果外推问题。

### TRN04-D03
两个 checkpoint 的 momentum tensor 数值相同，但一个存 buffer、一个存 velocity。说明为什么直接迁移错误，并给转换条件。

## E. AI 迁移

### TRN04-E01
为 PyTorch `SGD(momentum=.9,dampening=.1)` 写前三步 buffer 方程，体现第一步例外。

### TRN04-E02
设计 framework convention parity test：给定手工 gradients，逐步比 buffer、direction、parameter。

### TRN04-E03
模型有 weight/bias/norm 三个 parameter groups。写复现表，说明每组 LR、momentum、decay 与 state dtype。

## 作答与复盘

完成独立尝试后打开 [[解答 - Momentum、EMA、偏差修正与框架约定]]。
