---
type: source
status: active
area: [sources, metric-learning, nearest-neighbor, margin]
source_type: paper
title: "Distance Metric Learning for Large Margin Nearest Neighbor Classification"
author: [Kilian Q. Weinberger, Lawrence K. Saul]
year: 2009
url: "https://www.jmlr.org/papers/v10/weinberger09a.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "JMLR 10, 207–244"
scope_role: primary
temporal_role: classical-foundation
related: ["[[度量学习、相似性与检索风险]]", "[[支持向量机、最大间隔与核方法]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Distance Metric Learning for Large Margin Nearest Neighbor Classification

> [!abstract] 来源定位
> LMNN 以 target neighbors 与 different-class impostors 定义 large-margin Mahalanobis learning，并给出 convex semidefinite formulation。本库用它连接 pair/triplet constraints、hinge surrogate 与 kNN task risk。

## 本库调用

1. pull target neighbors、push margin-violating impostors；
2. Mahalanobis matrix learning 可凸，deep encoder 整体通常非凸；
3. target-neighbor choice 属于 training contract；
4. metric loss 下降不等于 held-out retrieval risk 下降；
5. multi-class geometry 仍依赖 labels 与 sampling；
