---
type: source
status: verified
area: [sources, benchmarking, variance, reproducibility]
source_type: paper
title: "Accounting for Variance in Machine Learning Benchmarks"
author: "Bouthillier et al."
year: 2021
url: "https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf"
accessed: 2026-08-26
source_tier: A
venue: MLSys
scope_role: statistical-benchmarking
related: ["[[随机种子、配对比较、置信区间与序贯决策]]", "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Bouthillier 等：机器学习基准中的方差分账

> [!abstract] 来源定位
> 论文把 data sampling、initialization 和 hyperparameter optimization 等随机性纳入 benchmark 比较，并研究有限预算下的比较方法。

## 本卷调用

- 先定义比较的随机变量与算法分布，再选择估计器；
- 对共享数据/seed 的方法使用 paired difference；
- 将 tuning randomness 和 final-evaluation randomness 分账；
- 报 mean/quantiles/interval 与失败率，不只报单一标准差。

## 边界

benchmark variance 不是一个可跨实验搬运的常数；配对只有在同一随机因素确实同时作用于两方法时才降低方差。
