---
type: source
status: active
area: [sources, learning-theory, kernel-ridge, regularization-rates]
source_type: paper
title: "Optimal Rates for the Regularized Least-Squares Algorithm"
author: [Andrea Caponnetto, Ernesto De Vito]
year: 2007
url: "https://doi.org/10.1007/s10208-006-0196-8"
accessed: 2026-08-23
source_tier: A
license: "Foundations of Computational Mathematics article; retain citation and correction caveat"
venue: "Foundations of Computational Mathematics 7, 331–368"
scope_role: primary
temporal_role: classical-foundation
related: ["[[核岭回归与 Gaussian Process 接口]]", "[[局部 Rademacher 复杂度与快收敛率]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Optimal Rates for the Regularized Least-Squares Algorithm

> [!abstract] 来源定位
> Caponnetto 与 De Vito 以 covariance/integral operator、source condition 与 effective dimension 分析 RKHS regularized least squares，并建立相应 minimax-rate 主线。它为本库从 finite Gram shrinkage 走向 population spectral bias–variance 提供正式接口。

## 元数据与纳入

- 正式 DOI：[Springer](https://doi.org/10.1007/s10208-006-0196-8)；
- 正式引用：Caponnetto, A. & De Vito, E. (2007), *FoCM* 7, 331–368；
- 后续修正入口：[Sutherland 2017 correction note](https://arxiv.org/abs/1702.02982)；
- 证据角色：effective dimension、source/capacity assumptions、regularization choice 与 rate architecture；
- 本库不搬运未逐条件核验的定理常数，且显式保留 correction caveat。

## 本库调用的断言

1. KRR prediction behavior 由 kernel covariance operator 的 spectrum 与 target alignment共同决定；
2. effective dimension 可写成 eigenvalue shrinkage 的 trace；
3. regularization bias 与 stochastic variance 需要 source/capacity/noise assumptions 才能转成具体 rates；
4. “KRR 一律达到某个 \(n\)-rate”不是无条件命题。
