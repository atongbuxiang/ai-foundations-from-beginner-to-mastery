---
type: source
status: active
area: [sources, learning-theory, logistic-regression, separation]
source_type: paper
title: "On the existence of maximum likelihood estimates in logistic regression models"
author: [Adelin Albert, J. A. Anderson]
year: 1984
url: "https://doi.org/10.1093/biomet/71.1.1"
accessed: 2026-08-23
source_tier: A
license: "Biometrika article; retain citation and independent explanation"
venue: "Biometrika 71(1), 1–10"
scope_role: primary
temporal_role: classical-foundation
related: ["[[逻辑回归、复合损失与概率分类]]", "[[模型可辨识性、选择与 Misspecification]]"]
created: 2026-08-23
updated: 2026-08-23
---

# On the existence of maximum likelihood estimates in logistic regression models

> [!abstract] 来源定位
> Albert 与 Anderson 分类 complete separation、quasi-complete separation 与 overlap，并刻画 logistic-regression MLE 的存在边界。它解释“训练数据完全可分时优化器权重继续变大”不是单纯数值 bug，而可能是无正则 likelihood 没有有限 minimizer。

## 元数据与纳入

- DOI：[Biometrika](https://doi.org/10.1093/biomet/71.1.1)；
- 正式引用：Albert, A. & Anderson, J. A. (1984), *Biometrika* 71(1), 1–10；
- 证据角色：separation geometry 与 finite MLE existence；
- 边界：regularization、Bayesian prior、high-dimensional phase transition 与 numerical stopping 是后续层。

## 本库调用的断言

1. complete separation 下 unregularized logistic likelihood 的 supremum/infimum 可沿无穷参数射线逼近；
2. finite MLE existence 取决于 design-label geometry，不只取决于 feature matrix rank；
3. large coefficients、vanishing curvature 与 misleading standard errors 是结构症状；
4. coercive regularization 可恢复 finite optimization target，但改变 estimand。

