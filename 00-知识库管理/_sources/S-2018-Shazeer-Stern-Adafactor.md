---
type: source
status: verified
area: [sources, optimization, adafactor, memory]
source_type: paper
title: "Adafactor: Adaptive Learning Rates with Sublinear Memory Cost"
author: "Noam Shazeer; Mitchell Stern"
year: 2018
url: "https://arxiv.org/abs/1804.04235"
venue: "ICML 2018"
accessed: 2026-08-26
source_tier: A
license: "arXiv/ICML 论文；本库仅保存独立摘要、必要公式与链接"
scope_role: memory-efficient-adaptation
temporal_role: modern-foundational
related: ["[[Lion、Adafactor 与自适应优化器证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Shazeer、Stern：Adafactor

> [!abstract] 来源定位
> Adafactor 针对矩阵参数把逐元素二阶矩近似为 row/column factors，使辅助状态由 $O(nm)$ 降为 $O(n+m)$；论文还引入 update clipping、变化的二阶衰减与 parameter-scale-aware step。

## 课程采用与边界

- factored statistic 匹配 row/column marginals，不等于原二阶矩矩阵的低秩最佳逼近；
- 对向量参数仍需未分解状态或特定 fallback；
- 省掉 momentum 时状态内存可明显下降，但 update rule、relative step 与 clipping 同时变化，不能把结果只归因于“factorization”；
- 不同框架对 LR、$\epsilon_1$ 与 decoupled decay 有公开分歧，需与当前官方文档逐式核对。
