---
type: source
status: active
area: [sources, learning-theory, random-forests, ensembles]
source_type: paper
title: "Random Forests"
author: [Leo Breiman]
year: 2001
url: "https://doi.org/10.1023/A:1010933404324"
accessed: 2026-08-23
source_tier: A
license: "Machine Learning journal article; author-hosted PDF available, retain citation"
venue: "Machine Learning 45, 5–32"
scope_role: primary
temporal_role: classical-foundation
related: ["[[Bagging、Random Forest 与 Boosting]]", "[[偏差—方差—噪声分解]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Random Forests

> [!abstract] 来源定位
> Breiman 将 randomized tree predictors 的 ensemble formalize，并用 bootstrap/random-feature mechanisms、individual strength、correlation 与 large-forest limit 分析 random forests。它是本库“增加树数消除的是 Monte Carlo error，而非所有统计误差”的正式起点。

## 元数据与纳入

- 正式 DOI：[Springer](https://doi.org/10.1023/A:1010933404324)；
- 作者论文页：[Berkeley](https://www.stat.berkeley.edu/~breiman/papers.html)；
- 正式引用：Breiman, L. (2001), *Machine Learning* 45, 5–32；
- 证据角色：randomized-tree ensemble、feature subsampling、strength/correlation 与 infinite-forest limit；
- 边界：feature importance、probability calibration、modern consistency 与 dependent data 需要另行审计。

## 本库调用的断言

1. forest tree 依赖随机向量，ensemble对其随机性投票/平均；
2. 增加树数时 conditional ensemble趋于 infinite-forest limit；
3. decorrelation 与 base-tree quality 必须共同考虑；
4. random feature subsampling不是无条件 variance-only intervention；
5. OOB predictions 可用于内部估计，但 adaptive reuse 不自动保持独立测试语义。
