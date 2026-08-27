---
type: source
status: active
area: [sources, metric-learning, clustering, side-information]
source_type: paper
title: "Distance Metric Learning with Application to Clustering with Side-Information"
author: [Eric P. Xing, Andrew Y. Ng, Michael I. Jordan, Stuart Russell]
year: 2002
url: "https://papers.nips.cc/paper_files/paper/2002/hash/c3e4035af2a1cde9f21e1ae1951ac80b-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "NeurIPS 2002"
scope_role: primary
temporal_role: classical-foundation
related: ["[[度量学习、相似性与检索风险]]", "[[K-Means、聚类风险与不可辨识性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Distance Metric Learning with Application to Clustering with Side-Information

> [!abstract] 来源定位
> 从 similar/dissimilar pair side-information 学习 Mahalanobis geometry，使 clustering 不再依赖手工 distance。本库调用其 PSD metric、linear-transform equivalence 与 pair-sampling 语义。

## 本库调用

1. PSD Mahalanobis distance 等价于先线性变换再用 Euclidean distance；
2. pair constraints 定义 supervision 与 similarity；
3. learned geometry 不保证对未声明 task 有效；
4. constraint sampling 与 evaluation split 必须分开；
5. singular PSD matrix 给 pseudo-metric 而未必是真 metric；
