---
type: source
status: verified
area: [sources, statistics, sequential-analysis, confidence-sequences]
source_type: paper
title: "Time-uniform, nonparametric, nonasymptotic confidence sequences"
author: "Howard et al."
year: 2021
url: "https://doi.org/10.1214/20-AOS1991"
accessed: 2026-08-26
source_tier: A
venue: "Annals of Statistics"
scope_role: formal-methods
related: ["[[随机种子、配对比较、置信区间与序贯决策]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Howard 等：Time-uniform Confidence Sequences

> [!abstract] 来源定位
> confidence sequence 是对所有观测时刻同时有效的随机区间，因此可在预设条件下容许持续查看和数据依赖停止。

## 本卷调用

- 区分 fixed-$n$ confidence interval 与 time-uniform confidence sequence；
- 若每增加一对 seed 都查看结果，必须使用预注册 alpha-spending、sequential test 或 CS；
- 记录 stopping time、边界公式与每次 peek，而非只保存最终区间；
- precision stopping 与 efficacy/futility stopping 的目标分开。

## 边界

CS 的有效性仍依赖其 martingale/尾界条件与 experimental unit；普通每步 95% CI 不能因“看起来保守”而当作 time-uniform。
