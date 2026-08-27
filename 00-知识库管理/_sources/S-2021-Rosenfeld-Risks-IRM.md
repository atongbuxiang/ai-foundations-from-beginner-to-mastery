---
type: source
status: active
area: [sources, invariant-risk-minimization, causal-robustness]
source_type: paper
title: "The Risks of Invariant Risk Minimization"
author: [Elan Rosenfeld, Pradeep Ravikumar, Andrej Risteski]
year: 2021
url: "https://openreview.net/forum?id=BbNIbVPJ-42"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and model conditions"
venue: "ICLR 2021"
scope_role: primary
temporal_role: critical-boundary
related: ["[[OOD、鲁棒性与因果不变性的边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# The Risks of Invariant Risk Minimization

> [!abstract] 来源定位
> 分析有限训练环境和高维特征下 IRM/环境不变目标可能选择错误 predictors 的条件。本库用它限制“跨训练域最优 ⇒ 因果/任意新域稳定”的外推；不把特定反例写成所有 invariance 方法无效。

## 本库调用

1. finite environments 不足以识别所有 spurious directions；
2. dimensionality 与 environment diversity 的关系；
3. empirical IRM surrogate 与理想 constraint 分开；
4. training invariance 不能保证 unseen interventions；
5. failure cases 与 ERM/robust baselines 同时报告。
