---
type: source
status: verified
area: [sources, optimization, adamw, schedule, weight-scale]
source_type: blog
title: "AdamW的Weight RMS的渐近估计（下）"
author: 苏剑林
year: 2025
url: "https://spaces.ac.cn/archives/11404"
accessed: 2026-08-26
source_tier: C
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
scope_role: chinese-derivation-entry
related: ["[[Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]", "[[权重衰减、尺度不变性与 Weight RMS 动力学]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 苏剑林：动态 Learning Rate 下的 AdamW Weight RMS

> [!abstract] 来源定位
> 文章把常 LR 的 Weight RMS 平衡推广到随时间变化的学习率/衰减，强调参数尺度响应具有记忆核而非瞬时跟随。课程采用递推与时标视角，不把平均场估计当逐层恒等式。

## 课程采用

从

$$
\theta_t=(1-\eta_t\lambda_t)\theta_{t-1}-\eta_tu_t
$$

展开初始化与历史更新的乘积权重，比较 schedule 变化速度和 $1/(\eta_t\lambda_t)$ 量级的遗忘时标。零均值、低 SNR、弱相关、epsilon 可忽略和参数维数足够大等条件必须保留。

## 边界

真实网络的 normalization symmetry、非平稳 update、分组 LR/decay 与训练末段 cooldown 都会造成偏离；偏离本身是诊断信息。
