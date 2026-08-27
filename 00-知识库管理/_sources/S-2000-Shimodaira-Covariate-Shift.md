---
type: source
status: active
area: [sources, covariate-shift, importance-weighting]
source_type: paper
title: "Improving Predictive Inference under Covariate Shift by Weighting the Log-Likelihood Function"
author: [Hidetoshi Shimodaira]
year: 2000
url: "https://doi.org/10.1016/S0378-3758(00)00115-4"
accessed: 2026-08-23
source_tier: A
license: "Scholarly source; retain citation and regularity conditions"
venue: "Journal of Statistical Planning and Inference"
scope_role: primary
temporal_role: foundational
related: ["[[重要性加权与 Covariate Shift 校正]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Improving Predictive Inference under Covariate Shift

> [!abstract] 来源定位
> 研究 train/test covariate distributions 不同而条件规律稳定时，用 density-ratio weights 修正 predictive inference。本库调用 target-risk change-of-measure 主线；支持重叠、ratio estimation 与方差另行审计。

## 本库调用

1. $P_s(Y\mid X)=P_t(Y\mid X)$ 假设；
2. $w(X)=p_t(X)/p_s(X)$ 加权；
3. model misspecification 下 weighting 改变 pseudo-true target；
4. 权重不是“让分布看起来相似”的装饰；
5. overlap 失败时 source data 不能识别 target risk。
