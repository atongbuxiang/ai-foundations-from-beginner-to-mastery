---
type: exercise
status: verified
area: [training, optimization, adaptive-optimization]
topic: "[[Adam 的尺度不变性、Sign 近似与 Update RMS]]"
solution: "[[解答 - Adam 的尺度不变性、Sign 近似与 Update RMS]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Adam 的尺度不变性、Sign 近似与 Update RMS

> [!abstract] 训练目标
> 把 exact identity、regime approximation 与 mean-field statistical estimate 分层；能推导低 SNR 下的 Update RMS，并避免把它们误写成无条件定理。

## A. 识别与复述

### TRN14-A01
精确定义“完整历史正比例缩放下的 Adam 方向不变性”，列出 $c$、$\epsilon$ 与状态同步条件。

### TRN14-A02
在什么局部条件下 Adam 方向近似 $\operatorname{sign}(g_t)$？为什么有 momentum 时不能直接写成当前梯度的 sign？

### TRN14-A03
区分 direction RMS、parameter-delta RMS 与含 AdamW decay 的 full-update RMS。

## B. 手算与构造

### TRN14-B01
取 $m=(2,-3),v=(4,9),\epsilon=0$。计算方向；把历史整体乘 $c=7$ 后验证不变。

### TRN14-B02
若 $\beta_1=0.9$ 且低 SNR、二阶矩归一化近似常数，计算理论 Update RMS $\sqrt{(1-\beta_1)/(1+\beta_1)}$。

### TRN14-B03
比较 $\beta_1=0,0.9,0.99$ 的低 SNR Update RMS，解释 momentum 如何改变方向幅度。

## C. 推导与证明

### TRN14-C01
对零均值、独立、方差 $\sigma^2$ 的平稳梯度，推导 EMA $m_t=(1-\beta_1)\sum_{k\ge0}\beta_1^kg_{t-k}$ 的稳态方差。

### TRN14-C02
在 $v_t\approx\sigma^2$、ratio-of-expectations 近似下，推出低 SNR Update RMS 公式，并逐条列出近似条件。

### TRN14-C03
证明梯度整体正比例缩放不等于任意参数重参数化不变性；用 $\theta=a\phi$ 写出链式法则比较参数位移。

## D. 边界、反例与纠错

### TRN14-D01
给出一个 $\beta_1>0$、当前梯度为正但 $m_t<0$ 的历史，反驳“Adam 就是 signSGD”。

### TRN14-D02
为什么理论 Update RMS 近似中 $\beta_2$ 消失，不等于实际训练中 $\beta_2$ 不重要？

### TRN14-D03
反驳：“direction RMS 恒为约 0.23，因此参数每步 RMS 都是 0.23。”

## E. AI 迁移

### TRN14-E01
为大模型日志定义三个不会混淆单位的 update 指标，并说明聚合层级。

### TRN14-E02
设计 Monte Carlo 实验检验低 SNR Update RMS，至少改变 $\beta_1$、SNR、维度和样本相关性。

### TRN14-E03
看到博客或论文给出简洁缩放律时，怎样把它转成“可证身份—近似假设—可观测诊断”三层笔记？

## 作答与复盘

每个结论标 `exact / approximation / empirical`。独立完成后打开 [[解答 - Adam 的尺度不变性、Sign 近似与 Update RMS]]。
