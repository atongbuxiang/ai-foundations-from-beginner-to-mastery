---
type: solution
status: verified
area: [training, optimization, momentum]
topic: "[[Momentum、EMA、偏差修正与框架约定]]"
exercise: "[[习题 - Momentum、EMA、偏差修正与框架约定]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Momentum、EMA、偏差修正与框架约定

## A. 识别与复述

### TRN04-A01
Buffer：$b_t=\mu b_{t-1}+g_t,\Delta\theta=-\eta b_t$，state 单位是 gradient。Velocity：$v_t=\mu v_{t-1}-\eta g_t,\Delta\theta=v_t$，state 单位是 parameter。EMA：$m_t=\mu m_{t-1}+(1-\mu)g_t,\Delta\theta=-\alpha m_t$，state 单位是 gradient。

### TRN04-A02
常 $\eta$、同初始状态：$v_t=-\eta b_t$，$m_t=(1-\mu)b_t$，匹配 update 需 $\alpha=\eta/(1-\mu)$。

### TRN04-A03
当前 PyTorch 文档规定首个 buffer 直接设为第一 gradient，不从零统一应用 dampening；dampening 从第二步开始。故有 dampening 时首步是例外。

## B. 手算与构造

### TRN04-B01
$b_0=2,\Delta\theta_0=-0.2$；$b_1=.9(2)-1=.8,\Delta\theta_1=-.08$。Velocity $v_0=-.2$，$v_1=.9(-.2)-.1(-1)=-.08$，与 $-\eta b_t$ 一致。

### TRN04-B02
$m_0=.1(2)=.2$；$m_1=.9(.2)+.1(-1)=.08$。因 $m=.1b$，匹配 $-\eta b$ 需 $\alpha=.1/.1=1$。

### TRN04-B03
$b_0=3$，$b_1=.8(3)+3=5.4$，$b_2=.8(5.4)+3=7.32$，极限 $3/(1-.8)=15$。EMA 为 $.6,1.08,1.464$；分别除以 $.2,.36,.488$ 后都是 3。

## C. 推导与证明

### TRN04-C01
基步 $b_0=g_0$。若 $b_{t-1}=\sum_{k=0}^{t-1}\mu^{t-1-k}g_k$，则 $b_t=\mu b_{t-1}+g_t=\sum_{k=0}^{t-1}\mu^{t-k}g_k+g_t=\sum_{k=0}^t\mu^{t-k}g_k$。

### TRN04-C02
常 LR：若 $v_{t-1}=-\eta b_{t-1}$，则 $v_t=\mu(-\eta b_{t-1})-\eta g_t=-\eta b_t$。变化 LR 令 $v_t=-\eta_tb_t$：代入 $b_{t-1}=-v_{t-1}/\eta_{t-1}$ 得 $v_t=\mu(\eta_t/\eta_{t-1})v_{t-1}-\eta_tg_t$。

### TRN04-C03
展开 $m_t=(1-\mu)\sum_{k=0}^t\mu^{t-k}g_k$，权重和 $(1-\mu)\sum_{j=0}^t\mu^j=1-\mu^{t+1}$。零初始化少掉此前无限历史，因此除以该和把恒定 gradient 的估计恢复为自身。

## D. 边界、反例与纠错

### TRN04-D01
取 $g_0=g_1=1,\mu=.9,\eta_0=.1,\eta_1=.01$。Buffer：$b_0=1$，第二步 $b_1=1.9$，update $-.019$。朴素 velocity：$v_0=-.1$，$v_1=.9(-.1)-.01=-.1$。二者不相同。

### TRN04-D02
EMA 对高频序列可降 variance，却引入 lag；gradient mean 快速旋转时，旧方向会有系统偏差。即使 update noise 降低，也不能跳过 optimization path、model/data 与 validation 因果链推出泛化改善。

### TRN04-D03
若 tensor 是 $b$，对应 velocity 应为 $v=-\eta b$；直接复制会把 state 单位放大/缩小。转换还要求当前/历史 LR placement、constant LR、同初始化、无额外 dampening/bias correction；否则应从算法状态重新初始化或逐步翻译。

## E. AI 迁移

### TRN04-E01
用 gradients $g_1,g_2,g_3$：$b_1=g_1$；$b_2=.9b_1+(1-.1)g_2=.9b_1+.9g_2$；$b_3=.9b_2+.9g_3$。参数每步减 LR 乘 buffer。第一步没有 $.9g_1$ 的 dampening。

### TRN04-E02
冻结模型，手工注入确定梯度序列；每步抓取框架 state dict 的 buffer、实际 update direction、parameter；与按所用版本文档写的 reference recurrence 逐元素比较，并覆盖首步、dampening、Nesterov、变化 LR、resume。

### TRN04-E03
表中每组写 parameter names/shapes、LR、momentum、dampening、Nesterov、weight decay 与插入方式、state dtype/device、buffer init、step counter、scheduler。Norm/bias 常不 decay，但这必须是显式合同而非默认猜测。

## 无提示重做

- [ ] 在变化 LR 下重新推导两种 convention 的关系。
- [ ] 从 PyTorch state dict 手算恢复下一步。
