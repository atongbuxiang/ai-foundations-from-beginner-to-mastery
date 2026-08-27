---
type: source
status: verified
area: [sources, optimization, adamw, weight-scale]
source_type: blog
title: "AdamW的Weight RMS的渐近估计（上）"
author: 苏剑林
year: 2025
url: "https://spaces.ac.cn/archives/11307"
accessed: 2026-08-26
source_tier: C
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
scope_role: chinese-derivation-entry
temporal_role: research-exposition
related: ["[[L2 正则、Coupled Decay 与 AdamW]]", "[[权重衰减、尺度不变性与 Weight RMS 动力学]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 苏剑林：AdamW Weight RMS 渐近估计

> [!abstract] 来源定位
> 文章把常 LR/decay 的 AdamW 参数递推写成 EMA，并在零均值、稳态与平均场条件下估计 Weight RMS。它提供很有用的尺度诊断，但不说明真实网络的所有层都会达到同一平衡。

## 核心重写

若 decoupled AdamW 写成

$$
\theta_t=(1-\eta\lambda)\theta_{t-1}-\eta u_t,
$$

记 $\beta_3=1-\eta\lambda$，则参数是初始化与 $-u_t/\lambda$ 历史的指数加权组合。对于零均值、低 SNR、epsilon 可忽略、近似平稳的 normalized update，文章得到

$$
\operatorname{RMS}(\theta_t)^2
\approx
\beta_3^{2t}\operatorname{RMS}(\theta_0)^2
+(1-\beta_3^{2t})\frac{\eta}{2\lambda},
$$

从而长期近似 $\operatorname{RMS}(\theta)\approx\sqrt{\eta/(2\lambda)}$。

## 不可省略的条件

- decoupled decay 且 $0<\eta\lambda\ll1$；
- LR/decay 常数或变化慢；
- update 与已有参数的相关项可忽略或用更完整平均场处理；
- 更新零均值、低 SNR、稳态、参数维数足够大；
- 参数组、归一化尺度对称与初始化残留另行审计。

课程会用最小随机实验复查 $\sqrt{\eta/\lambda}$ 标度，同时构造非零均值与 schedule 反例。
