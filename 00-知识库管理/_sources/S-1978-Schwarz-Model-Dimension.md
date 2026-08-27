---
type: source
status: active
area: [sources, learning-theory, model-selection, bic]
source_type: paper
title: "Estimating the Dimension of a Model"
author: [Gideon Schwarz]
year: 1978
url: "https://doi.org/10.1214/aos/1176344136"
accessed: 2026-08-23
source_tier: A
license: "Annals of Statistics article; retain citation and independent derivations"
venue: "Annals of Statistics 6(2), 461–464"
scope_role: primary
temporal_role: classical-foundation
related: ["[[模型可辨识性、选择与 Misspecification]]", "[[正则化、交叉验证与模型选择]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Estimating the Dimension of a Model

> [!abstract] 来源定位
> Schwarz 从 Bayes model comparison 的 large-sample expansion得到 log-likelihood与dimension penalty的准则。本库用它解释 BIC 的 evidence/true-model-selection语义及其 regular-model边界。

## 本库调用

1. regular fixed-dimensional models下，negative twice log likelihood配 \(d\log n\) penalty；
2. BIC与AIC优化的 asymptotic target不同；
3. true model不在 candidates中时，“选择真模型”语义失效；
4. mixtures、neural networks等 singular/nonidentifiable models不能机械套 regular Laplace dimension；
5. candidate generation与数据复用仍需 selection audit。
