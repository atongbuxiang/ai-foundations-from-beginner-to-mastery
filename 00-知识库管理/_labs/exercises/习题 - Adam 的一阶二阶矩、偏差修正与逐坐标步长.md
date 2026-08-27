---
type: exercise
status: verified
area: [training, optimization, adaptive-optimization]
topic: "[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]"
solution: "[[解答 - Adam 的一阶二阶矩、偏差修正与逐坐标步长]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Adam 的一阶二阶矩、偏差修正与逐坐标步长

> [!abstract] 训练目标
> 能从零状态推导偏差修正、逐步手算 Adam，并严格区分“矩估计无偏”与“更新比值无偏”。

## A. 识别与复述

### TRN11-A01
写出经典 Adam 的 $m_t,v_t,\hat m_t,\hat v_t$ 与参数更新，说明每个状态的维度。

### TRN11-A02
为什么 $m_0=v_0=0$ 会产生启动偏差？偏差修正分别除以什么？

### TRN11-A03
区分 global learning rate、coordinate multiplier、normalized direction 与 parameter delta。

## B. 手算与构造

### TRN11-B01
一维 $g_1=2,g_2=4$，$\beta_1=0.5,\beta_2=0.75,\epsilon=0,\eta=0.1$。计算两步全部状态与位移。

### TRN11-B02
若梯度恒为 $g>0$，从零状态出发，证明每一步偏差修正后的方向为 1（$\epsilon=0$）。

### TRN11-B03
二维当前 $\hat m=(1,1),\hat v=(1,100)$，$\eta=0.01,\epsilon=0$。计算更新并解释方向旋转。

## C. 推导与证明

### TRN11-C01
若 $g_t$ 同分布且 $\mathbb E g_t=\mu$，推导 $\mathbb E m_t=(1-\beta_1^t)\mu$。

### TRN11-C02
若 $\mathbb E g_t^2=\nu$，推导 $\mathbb E v_t=(1-\beta_2^t)\nu$，并列出所需平稳性假设。

### TRN11-C03
证明即使 $\hat m_t$ 与 $\hat v_t$ 分别无偏，一般也不能推出 $\mathbb E[\hat m_t/\sqrt{\hat v_t}]=\mu/\sqrt\nu$。

## D. 边界、反例与纠错

### TRN11-D01
给出一个随机变量例子，直接展示“期望之比不等于比值的期望”。

### TRN11-D02
反驳：“Adam 每个坐标的实际步长就是 $\eta$。”

### TRN11-D03
为什么从 checkpoint 恢复权重但不恢复 step counter 会立刻改变 Adam 更新？

## E. AI 迁移

### TRN11-E01
日志只写 `lr=1e-4` 为什么不足以判断某层是否在快速更新？给出最小诊断量集合。

### TRN11-E02
设计一个单元测试验证框架 Adam 的偏差修正与状态推进顺序。

### TRN11-E03
在 gradient accumulation 中，应该每个 micro-batch 更新 $m,v$，还是每次 optimizer step 更新？说明这不是纯记号问题。

## 作答与复盘

完成独立推导后打开 [[解答 - Adam 的一阶二阶矩、偏差修正与逐坐标步长]]；计算题必须保留中间状态。
