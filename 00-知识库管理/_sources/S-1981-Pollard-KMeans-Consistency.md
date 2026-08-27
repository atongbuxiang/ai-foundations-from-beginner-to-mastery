---
type: source
status: active
area: [sources, learning-theory, k-means, clustering-consistency]
source_type: paper
title: "Strong Consistency of K-Means Clustering"
author: [David Pollard]
year: 1981
url: "https://doi.org/10.1214/aos/1176345339"
accessed: 2026-08-23
source_tier: A
license: "Annals of Statistics article; author-hosted PDF available"
venue: "Annals of Statistics 9(1), 135–140"
scope_role: primary
temporal_role: classical-foundation
related: ["[[K-Means、聚类风险与不可辨识性]]", "[[可实现、不可知、相合性与可学习性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Strong Consistency of K-Means Clustering

> [!abstract] 来源定位
> Pollard 把 K-Means写成对 nearest-center squared-distance risk 的 empirical minimization，并在矩条件、唯一性等假设下研究 empirical optimal center sets 的强相合。本库用它区分 global empirical minimizer、Lloyd output与 population optimum。

## 本库调用

1. population/empirical K-Means risk是对 unordered center set定义的 quantization objective；
2. 固定 assignment时最优 center是 cluster mean；
3. consistency需要矩、紧性/分离与 population optimum条件；
4. global ERM相合不能自动转移给局部 Lloyd iterate；
5. center-set收敛不等于外部语义标签恢复。
