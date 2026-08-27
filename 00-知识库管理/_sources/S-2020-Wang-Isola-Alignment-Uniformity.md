---
type: source
status: active
area: [sources, contrastive-learning, alignment, uniformity]
source_type: paper
title: "Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere"
author: [Tongzhou Wang, Phillip Isola]
year: 2020
url: "https://proceedings.mlr.press/v119/wang20k.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "ICML 2020"
scope_role: primary
temporal_role: modern-theory
related: ["[[对比学习、InfoNCE 与密度比]]", "[[表示坍缩、非坍缩与可辨识边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere

> [!abstract] 来源定位
> 在 unit hypersphere 与 asymptotic setting 下把 contrastive objective 连接到 positive alignment 与 feature-distribution uniformity。本库用它提供 MI 解释之外的 geometry ledger，并保留其条件。

## 本库调用

1. alignment 使 positive representations 接近；
2. uniformity 避免所有 points 集中到同一区域；
3. normalization 与 negative distribution 定义结论；
4. alignment 与 uniformity 良好不自动等于 task sufficiency；
5. finite batch、false negatives 与 augmentation validity 仍需另审；
