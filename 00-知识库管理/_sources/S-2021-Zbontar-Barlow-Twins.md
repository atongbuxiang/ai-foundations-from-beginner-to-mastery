---
type: source
status: active
area: [sources, self-supervised-learning, redundancy-reduction, collapse]
source_type: paper
title: "Barlow Twins: Self-Supervised Learning via Redundancy Reduction"
author: [Jure Zbontar, Li Jing, Ishan Misra, Yann LeCun, Stéphane Deny]
year: 2021
url: "https://proceedings.mlr.press/v139/zbontar21a.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and method conditions"
venue: "ICML 2021"
scope_role: primary
temporal_role: modern-method
related: ["[[表示坍缩、非坍缩与可辨识边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Barlow Twins

> [!abstract] 来源定位
> 用两视图表示的 cross-correlation 接近 identity 同时鼓励对角对齐与非对角去冗余。本库调用其 batch statistic、标准化与 loss geometry；有限 batch 成功不等于获得独立语义因素。

## 本库调用

1. diagonal term 处理 cross-view invariance；
2. off-diagonal term 抑制 feature redundancy；
3. correlation 依赖 batch centering/scaling；
4. identity target 排除完全常数解但不保证 task sufficiency；
5. decorrelation 不等于 statistical independence 或 disentanglement。
