---
type: source
status: active
area: [sources, conformal-prediction, quantile-regression, coverage]
source_type: paper
title: "Conformalized Quantile Regression"
author: [Yaniv Romano, Evan Patterson, Emmanuel J. Candès]
year: 2019
url: "https://proceedings.neurips.cc/paper_files/paper/2019/hash/5103c3584b063c431bd1268e9b5e76fb-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "NeurIPS 2019"
scope_role: primary
temporal_role: modern-method
related: ["[[Conformal Prediction 与有限样本 Coverage]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Conformalized Quantile Regression

> [!abstract] 来源定位
> 用 learned conditional quantiles 构造自适应初始区间，再用 held-out conformity scores 做有限样本校正。本库调用其 CQR score 和 heteroscedastic efficiency 直觉；coverage 仍来自 exchangeability 与 calibration rank，而不是 quantile model 本身正确。

## 本库调用

1. lower/upper quantile regression 提供输入依赖的初始带宽；
2. score 为标签超出初始区间两端的最大量；
3. calibration quantile 同时外扩上下端点；
4. base model 可错设，marginal validity 仍由 rank argument 控制；
5. calibration reuse、distribution shift 与 subgroup conditional coverage 仍是边界。
