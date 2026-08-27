---
type: source
status: verified
area: [sources, ai/scaling-laws, generative-modeling]
source_type: paper
title: "Scaling Laws for Autoregressive Generative Modeling"
author: "Tom Henighan et al."
year: 2020
url: "https://arxiv.org/abs/2010.14701"
accessed: 2026-08-26
source_tier: A
license: "arXiv paper; independent summary only"
scope_role: empirical-extension
temporal_role: foundational
related: ["[[经验 Scaling Law、幂律拟合与不可约项]]", "[[S-2020-Kaplan-语言模型尺度定律]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Scaling Laws for Autoregressive Generative Modeling

> [!abstract] 来源定位
> 论文在图像、视频、多模态与数学等自回归生成任务上研究 power-law-plus-constant，提供“不可约项与 reducible loss 分账”的跨域经验入口。

## 可调用证据

- 多个自回归生成域在所测范围内随模型/compute 平滑改善；
- 经验形式包含常数地板，因此 raw loss 的 log–log 图不必永远保持同一斜率；
- cross-entropy 可写成真实分布熵与 KL gap，给不可约项一个信息论解释入口；
- 不同域的常数、指数和有效窗口仍由数据与任务决定。

## 边界

- 真分布熵不可由有限拟合无误差识别；
- power-law-plus-constant 是经验函数族，不是所有下游离散指标的定理；
- 论文中的跨域相似性不能证明新架构或新模态共享精确指数。
