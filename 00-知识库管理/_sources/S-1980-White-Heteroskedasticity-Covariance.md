---
type: source
status: active
area: [sources, learning-theory, linear-regression, heteroskedasticity]
source_type: paper
title: "A Heteroskedasticity-Consistent Covariance Matrix Estimator and a Direct Test for Heteroskedasticity"
author: [Halbert White]
year: 1980
url: "https://doi.org/10.2307/1912934"
accessed: 2026-08-23
source_tier: A
license: "Econometrica article; retain citation and independent derivations"
venue: "Econometrica 48(4), 817–838"
scope_role: primary
temporal_role: classical-foundation
related: ["[[线性回归的统计学习理论]]", "[[模型可辨识性、选择与 Misspecification]]"]
created: 2026-08-23
updated: 2026-08-23
---

# A Heteroskedasticity-Consistent Covariance Matrix Estimator

> [!abstract] 来源定位
> White 说明：conditional mean 正确时，heteroskedasticity 不必破坏 OLS point estimation 的一致性，却会使同方差 covariance formula 失效；sandwich estimator 在适当条件下提供稳健渐近协方差。

## 元数据与纳入

- DOI：[JSTOR](https://doi.org/10.2307/1912934)；
- 正式引用：White, H. (1980), *Econometrica* 48(4), 817–838；
- 证据角色：heteroskedastic covariance、sandwich structure 与 naive standard-error failure；
- 本库只在相应 moment、independence/weak-dependence 与 regularity 条件下调用 asymptotic consistency。

## 本库调用的断言

1. \(E[\varepsilon\mid X]=0\) 与 \(\operatorname{Var}(\varepsilon\mid X)=\sigma^2\) 是不同假设；
2. heteroskedasticity 下 conditional OLS covariance 是 sandwich form；
3. naive \(\widehat\sigma^2(X^\top X)^{-1}\) 可能给错误 inference；
4. HC estimator 是渐近工具，不自动修复 finite-sample leverage、dependence、misspecified mean 或 numerical ill-conditioning。

