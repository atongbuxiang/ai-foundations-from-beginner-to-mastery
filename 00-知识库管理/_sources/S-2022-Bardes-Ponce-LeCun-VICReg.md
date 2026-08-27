---
type: source
status: active
area: [sources, self-supervised-learning, variance, covariance, collapse]
source_type: paper
title: "VICReg: Variance-Invariance-Covariance Regularization for Self-Supervised Learning"
author: [Adrien Bardes, Jean Ponce, Yann LeCun]
year: 2022
url: "https://openreview.net/forum?id=xm6YD62D1Ub"
accessed: 2026-08-23
source_tier: A
license: "ICLR OpenReview; retain citation and method conditions"
venue: "ICLR 2022"
scope_role: primary
temporal_role: modern-method
related: ["[[表示坍缩、非坍缩与可辨识边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# VICReg

> [!abstract] 来源定位
> 把 invariance、per-coordinate variance floor 与 within-view covariance penalty 显式分开。本库用它构造可手算的非坍缩证书，并强调这些是 batch-level surrogate 而非下游充分性的定理。

## 本库调用

1. invariance-only objective 容许 constant solution；
2. variance hinge 排除每一坐标零方差；
3. covariance penalty 抑制维度冗余；
4. variance floor 依赖 batch estimator、epsilon 与 threshold；
5. non-collapse、full rank、isotropy、identifiability 与 usefulness 必须分层。
