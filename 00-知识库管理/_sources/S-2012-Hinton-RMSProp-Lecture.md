---
type: source
status: verified
area: [sources, optimization, rmsprop]
source_type: lecture
title: "Neural Networks for Machine Learning, Lecture 6e: RMSProp"
author: "Geoffrey Hinton; Nitish Srivastava; Kevin Swersky"
year: 2012
url: "https://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf"
venue: "University of Toronto / Coursera lecture"
accessed: 2026-08-26
source_tier: A
license: "正式课程讲义；本库仅保存独立摘要、必要公式与链接"
scope_role: historical-definition
temporal_role: historical-foundational
related: ["[[RMSProp、滑动二阶矩与非平稳尺度]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Hinton 等：RMSProp 课程讲义

> [!abstract] 来源定位
> RMSProp 的经典课程来源：用近期梯度平方的滑动平均代替 AdaGrad 的永久累计量，再用其平方根缩放当前梯度。它提供算法动机，不提供现代框架所有变体的统一合同。

## 课程采用

$$
v_t=\rho v_{t-1}+(1-\rho)g_t^2,
\qquad
\theta_{t+1}=\theta_t-\eta\frac{g_t}{\sqrt{v_t}+\epsilon}.
$$

- forgetting time scale 由 $\rho$ 控制；
- 对非平稳 gradient scale 的响应快慢存在 bias–variance tradeoff；
- centered RMSProp、momentum、epsilon placement 与初始化是后来的实现约定，必须另查官方文档。

## 边界

“除以近期 RMS”不等于 whiten gradient，也不恢复 off-diagonal curvature；它只在当前坐标系中保存逐坐标二阶原始矩的 EMA。
