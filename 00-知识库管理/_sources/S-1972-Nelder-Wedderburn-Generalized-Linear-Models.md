---
type: source
status: active
area: [sources, learning-theory, generalized-linear-models, logistic-regression]
source_type: paper
title: "Generalized Linear Models"
author: [John A. Nelder, Robert W. M. Wedderburn]
year: 1972
url: "https://doi.org/10.2307/2344614"
accessed: 2026-08-23
source_tier: A
license: "JRSS Series A article; retain citation and independent derivations"
venue: "Journal of the Royal Statistical Society Series A 135(3), 370–384"
scope_role: primary
temporal_role: classical-foundation
related: ["[[逻辑回归、复合损失与概率分类]]", "[[常用连续分布与指数族]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Generalized Linear Models

> [!abstract] 来源定位
> Nelder 与 Wedderburn 以 exponential-family response、linear predictor 与 link function 统一 normal、binomial、Poisson 和 gamma models，并把 maximum likelihood computation 表成 iterative weighted linear regression。它是 logistic regression 的 GLM 历史与算法接口。

## 元数据与纳入

- 正式 DOI：[Wiley/RSS](https://doi.org/10.2307/2344614)；
- 正式引用：Nelder, J. A. & Wedderburn, R. W. M. (1972), *JRSS A* 135, 370–384；
- 证据角色：GLM 三元结构、binomial-logit model 与 IRLS；
- 边界：proper scoring、classification calibration、separation 与 modern regularization 分别由后续原论文补齐。

## 本库调用的断言

1. response distribution、linear predictor 与 link 是三个不同建模选择；
2. logistic regression 使用 binomial conditional law 与 logit link；
3. score/Hessian 导出 iterative reweighted least squares；
4. likelihood model 与 prediction decision threshold 不应混为一层。

