---
type: source
status: active
area: [sources, learning-theory, model-selection, aic]
source_type: paper
title: "A New Look at the Statistical Model Identification"
author: [Hirotugu Akaike]
year: 1974
url: "https://doi.org/10.1109/TAC.1974.1100705"
accessed: 2026-08-23
source_tier: A
license: "IEEE article; retain citation and independent derivations"
venue: "IEEE Transactions on Automatic Control 19(6), 716–723"
scope_role: primary
temporal_role: classical-foundation
related: ["[[模型可辨识性、选择与 Misspecification]]", "[[正则化、交叉验证与模型选择]]"]
created: 2026-08-23
updated: 2026-08-23
---

# A New Look at the Statistical Model Identification

> [!abstract] 来源定位
> Akaike把 model identification与 expected predictive information loss连接，形成 likelihood fit加参数复杂度修正的 AIC 主线。本库用它区分 predictive model selection、true-model recovery与 post-selection inference。

## 本库调用

1. training likelihood对复杂模型有系统 optimism；
2. regular parametric条件下 AIC用 \(2d\) 修正 expected out-of-sample deviance；
3. effective dimension、singular model与adaptive search会破坏朴素 parameter count；
4. AIC不是“真实模型存在时必选真模型”的无条件保证；
5. selection后的同数据 inference需要额外修正。
