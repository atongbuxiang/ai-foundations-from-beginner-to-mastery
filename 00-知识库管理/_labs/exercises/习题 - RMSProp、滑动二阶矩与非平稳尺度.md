---
type: exercise
status: verified
area: [training, optimization, adaptive-optimization]
topic: "[[RMSProp、滑动二阶矩与非平稳尺度]]"
solution: "[[解答 - RMSProp、滑动二阶矩与非平稳尺度]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - RMSProp、滑动二阶矩与非平稳尺度

> [!abstract] 训练目标
> 把 EMA 看成可计算的时间滤波器，理解 RMSProp 的适应速度、偏置、实现分歧与非平稳失败模式。

## A. 识别与复述

### TRN10-A01
写出 uncentered RMSProp 的递推与更新；解释它估计的是二阶矩而不是方差。

### TRN10-A02
给出 decay $\rho$ 的 e-fold 记忆尺度、半衰期与归一化权重有效样本量的公式。

### TRN10-A03
比较 AdaGrad 与 RMSProp 对遥远历史的权重；哪一个能忘记，代价是什么？

## B. 手算与构造

### TRN10-B01
$v_0=0,\rho=0.9$，梯度依次为 $2,2,2$。计算 $v_1,v_2,v_3$ 及未加 $\epsilon$ 的归一化方向。

### TRN10-B02
在 $t=0$ 前长期有 $g^2=a$，之后恒为 $g^2=b$。推导切换后第 $k$ 步的 $v_k$，并计算达到新旧差距一半所需 $k$。

### TRN10-B03
$\rho=0.99$ 时求 e-fold、近似半衰期和 $N_{\rm eff}$；说明三者为什么不是同一个量。

## C. 推导与证明

### TRN10-C01
展开证明 $v_t=(1-\rho)\sum_{j=1}^t\rho^{t-j}g_j^2+\rho^tv_0$。

### TRN10-C02
在 $g_t^2=q$ 恒定且 $v_0=0$ 时，证明 $v_t=q(1-\rho^t)$；若不做偏差修正，早期归一化方向怎样被放大？

### TRN10-C03
对无限归一化 EMA 权重 $w_k=(1-\rho)\rho^k$，证明 $N_{\rm eff}=1/\sum_kw_k^2=(1+\rho)/(1-\rho)$。

## D. 边界、反例与纠错

### TRN10-D01
反驳：“$\rho=0.99$ 就精确等于记住最近 100 步。”

### TRN10-D02
构造一个单次巨大梯度尖峰，说明 RMSProp 此后若干步可能把正常梯度压得过小。

### TRN10-D03
为什么 centered RMSProp 与 uncentered RMSProp 不是只差一个名字？给出均值非零时的数值例子。

## E. AI 迁移

### TRN10-E01
训练出现 loss spike 后更新 RMS 长时间降低。你会记录哪些量来区分“二阶矩记忆”与“梯度本身变小”？

### TRN10-E02
为非平稳 curriculum 设计 $\rho$ 的比较实验，说明如何避免把更短记忆的暂时响应误判成最终更优。

### TRN10-E03
审计某框架的 `RMSprop` 配置时，至少要确认哪些实现语义，才能与论文式公式对齐？

## 作答与复盘

每题先写对象、假设与单位，再计算。独立完成后打开 [[解答 - RMSProp、滑动二阶矩与非平稳尺度]]。
