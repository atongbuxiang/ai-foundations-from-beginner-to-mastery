---
type: source
status: active
area: [sources, mutual-information, contrastive-learning, variational-bounds]
source_type: paper
title: "On Variational Bounds of Mutual Information"
author: [Ben Poole, Sherjil Ozair, Aaron van den Oord, Alexander A. Alemi, George Tucker]
year: 2019
url: "https://proceedings.mlr.press/v97/poole19a.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "ICML 2019"
scope_role: primary
temporal_role: modern-theory
related: ["[[对比学习、InfoNCE 与密度比]]", "[[互信息与依赖性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# On Variational Bounds of Mutual Information

> [!abstract] 来源定位
> 统一多类 neural MI bounds 并比较 bias–variance 与 gradient trade-off。本库用它明确 InfoNCE 是特定 variational lower bound，不是无偏 MI estimator。

## 本库调用

1. variational critic family 产生 approximation gap；
2. finite-sample estimate 与 population bound 分开；
3. high MI 时可能 high bias 或 high variance；
4. optimization usefulness 不等于 MI estimation accuracy；
5. critic overfit 与 gradient bias 需要独立审计；
