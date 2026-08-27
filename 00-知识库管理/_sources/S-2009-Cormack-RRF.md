---
type: source
status: verified
area: [sources, information-retrieval, rank-fusion]
source_type: paper
title: "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods"
author: "Gordon V. Cormack; Charles L. A. Clarke; Stefan Buettcher"
year: 2009
url: "https://research.google/pubs/reciprocal-rank-fusion-outperforms-condorcet-and-individual-rank-learning-methods/"
accessed: 2026-08-26
source_tier: P1
license: "SIGIR paper; independent summary"
scope_role: rank-fusion
related: ["[[BM25、Dense Retrieval、Hybrid 与 Score Fusion]]"]
created: 2026-08-26
updated: 2026-08-26
---

# RRF：不依赖原始分数量纲的排序融合

> [!abstract] 来源定位
> RRF 用多个排序中的倒数名次求和融合结果。课程采用其无需对 BM25 与 dense 原始分数做同尺度假设的优点，并保留常数与截断深度。

RRF 不是概率校准，也不保证任何两路系统组合都优于最好单路；必须在目标查询分布上比较。
