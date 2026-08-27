---
type: source
status: active
area: [sources, learning-theory, clustering, impossibility]
source_type: paper
title: "An Impossibility Theorem for Clustering"
author: [Jon M. Kleinberg]
year: 2002
url: "https://papers.nips.cc/paper_files/paper/2002/hash/43e4e6a6f341e00671e123714de019a8-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "NeurIPS proceedings article; retain citation and independent summary"
venue: "NeurIPS 15"
scope_role: primary
temporal_role: classical-foundation
related: ["[[K-Means、聚类风险与不可辨识性]]", "[[No-Free-Lunch 与归纳偏置]]"]
created: 2026-08-23
updated: 2026-08-23
---

# An Impossibility Theorem for Clustering

> [!abstract] 来源定位
> Kleinberg 通过 scale invariance、richness与 consistency三条公理的不相容，说明“唯一自然聚类”不存在于无偏置的抽象距离输入上。本库用它约束聚类语义主张，而不把该公理定理误写成 K-Means risk theorem。

## 本库调用

1. clustering必须声明 representation、metric、scale与 algorithmic bias；
2. 不可能同时满足某组直觉公理，选择方法意味着选择结构偏好；
3. 该 theorem不证明 K-Means在任何具体分布上失败；
4. internal objective、external labels与 downstream utility是不同评价合同。
