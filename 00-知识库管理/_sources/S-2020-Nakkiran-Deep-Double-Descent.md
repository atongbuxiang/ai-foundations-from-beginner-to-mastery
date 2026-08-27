---
type: source
status: active
area: [sources, deep-double-descent, interpolation, empirical-generalization]
source_type: paper
title: "Deep Double Descent: Where Bigger Models and More Data Hurt"
author: [Preetum Nakkiran, Gal Kaplun, Yamini Bansal, Tristan Yang, Boaz Barak, Ilya Sutskever]
year: 2020
url: "https://openreview.net/forum?id=B1g5sA4twr"
accessed: 2026-08-23
source_tier: A
license: "OpenReview conference paper; retain citation"
venue: "ICLR 2020"
scope_role: primary
temporal_role: modern-empirical
related: ["[[插值、双下降与经典偏差方差边界]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Deep Double Descent
> [!abstract] 来源定位
> 在 CNN、ResNet、Transformer 等 setting 中研究 model-wise、sample-wise 与 epoch-wise double descent。本库调用多路径现象和 interpolation peak；结论保留 optimizer/regularization/early-stopping 条件。
## 本库调用
1. model-wise path；
2. sample-wise nonmonotonicity；
3. epoch-wise path；
4. label noise/regularization interaction；
5. empirical evidence boundary。
