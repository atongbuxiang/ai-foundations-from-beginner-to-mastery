---
type: source
status: active
area: [sources, conformal-prediction, regression, coverage]
source_type: paper
title: "Distribution-Free Predictive Inference for Regression"
author: [Jing Lei, Max G'Sell, Alessandro Rinaldo, Ryan J. Tibshirani, Larry Wasserman]
year: 2018
url: "https://doi.org/10.1080/01621459.2017.1307116"
accessed: 2026-08-23
source_tier: A
license: "Scholarly source; retain citation and theorem conditions"
venue: "Journal of the American Statistical Association"
scope_role: primary
temporal_role: foundational
related: ["[[Conformal Prediction 与有限样本 Coverage]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Distribution-Free Predictive Inference for Regression

> [!abstract] 来源定位
> 系统发展 regression conformal prediction 的有限样本、distribution-free marginal coverage 与效率分析。本库调用 split/full conformal 的对象和条件；不把 exchangeability 下的 marginal coverage 写成任意 shift 下的 conditional coverage。

## 本库调用

1. conformity/nonconformity score 与 candidate label inversion；
2. exchangeable ranks 产生有限样本 coverage；
3. sample splitting 牺牲数据效率换取计算与证明清晰；
4. residual score 使点预测器外包为 prediction interval；
5. validity 与 interval length/efficiency 是两个目标。
