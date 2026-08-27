---
type: source
status: active
area: [sources, learning-theory, pca, dimension-reduction]
source_type: review
title: "Principal Component Analysis: A Review and Recent Developments"
author: [Ian T. Jolliffe, Jorge Cadima]
year: 2016
url: "https://doi.org/10.1098/rsta.2015.0202"
accessed: 2026-08-23
source_tier: A
license: "Royal Society open article; retain citation and independent derivations"
venue: "Philosophical Transactions of the Royal Society A 374:20150202"
scope_role: primary-review
temporal_role: classical-foundation
related: ["[[PCA 的统计估计与主子空间风险]]", "[[奇异值分解]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Principal Component Analysis: A Review and Recent Developments

> [!abstract] 来源定位
> Jolliffe 与 Cadima 从最大方差、正交主成分、dimension reduction 和数据自适应性梳理 PCA，并明确讨论 PCA 能与不能解释什么。本库用它校准 PCA 的 statistical object、centering/scaling 与变体边界。

## 本库调用

1. PCA directions来自 sample covariance eigensystem，不是预先给定的语义轴；
2. sequential variance maximization与正交约束给 principal components；
3. centering、standardization与变量尺度会改变目标；
4. explained variance不是 label relevance、causality或 downstream utility；
5. robust/sparse/kernel等变体改变 estimator，不应与 ordinary PCA 混称。
