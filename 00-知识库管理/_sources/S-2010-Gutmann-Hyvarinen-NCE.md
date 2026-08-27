---
type: source
status: active
area: [sources, noise-contrastive-estimation, unnormalized-models]
source_type: paper
title: "Noise-contrastive estimation: A new estimation principle for unnormalized statistical models"
author: [Michael Gutmann, Aapo Hyvärinen]
year: 2010
url: "https://proceedings.mlr.press/v9/gutmann10a.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "AISTATS 2010"
scope_role: primary
temporal_role: method-origin
related: ["[[对比学习、InfoNCE 与密度比]]", "[[S-2018-Su-5617-噪声对比估计与配分函数]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Noise-contrastive estimation: A new estimation principle for unnormalized statistical models

> [!abstract] 来源定位
> 原始 NCE 把 data 与 known noise 做 binary logistic discrimination，以估计 unnormalized density 及 normalizing constant。本库用它严格区分 NCE parameter estimation 与后来 InfoNCE 的 multi-candidate MI-bound 语境。

## 本库调用

1. NCE 目标是 unnormalized statistical model estimation；
2. class-posterior logit 含 model/noise density ratio 与 sample ratio；
3. consistency 需要 model、noise 与 support 条件；
4. 增加 noise samples 有 statistical/computational trade-off；
5. 名称相近不代表 NCE 与 InfoNCE 有相同 estimand；
