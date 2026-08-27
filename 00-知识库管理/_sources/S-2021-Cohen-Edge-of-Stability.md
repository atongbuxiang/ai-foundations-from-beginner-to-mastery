---
type: source
status: verified
area: [sources, optimization, stability, deep-learning]
source_type: paper
title: "Gradient Descent on Neural Networks Typically Occurs at the Edge of Stability"
author: [Jeremy M. Cohen, Simran Kaur, Yuanzhi Li, J. Zico Kolter, Ameet Talwalkar]
year: 2021
url: "https://arxiv.org/abs/2103.00065"
accessed: 2026-08-26
source_tier: A
venue: "ICLR 2021"
scope_role: primary
related: ["[[二次模型的学习率—动量稳定域与阻尼]]", "[[Critical Batch、隐式偏置与 SGD 证据地图]]", "[[Update-to-Weight Ratio、谱与尺度诊断]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Cohen 等 2021：Edge of Stability

> [!abstract] 来源定位
> 论文实证显示 full-batch gradient descent 训练若干神经网络时，最大 Hessian eigenvalue 常在 $2/\eta$ 附近或略高，短时 loss 非单调而长时下降。课程把它标为深网训练轨迹的强实证现象，不把固定二次函数的 $2/L$ 定理直接用于时变非线性损失。

## 课程调用

- 固定二次稳定阈值与训练中 local sharpness 的对照；
- “单步下降 lemma 失效”不等于训练必然发散；
- 曲率由参数轨迹共同改变，静态 Hessian 分析是局部探针；
- 诊断时同时记录 loss、top eigenvalue、update 和时间窗口。
