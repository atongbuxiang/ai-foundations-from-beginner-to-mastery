---
type: source
status: active
area: [sources, generalization-measures, sharpness, empirical-audit]
source_type: paper
title: "Fantastic Generalization Measures and Where to Find Them"
author: [Yiding Jiang, Behnam Neyshabur, Hossein Mobahi, Dilip Krishnan, Samy Bengio]
year: 2020
url: "https://openreview.net/forum?id=SJgIPJBFvH"
accessed: 2026-08-23
source_tier: A
license: "OpenReview conference paper; retain citation"
venue: "ICLR 2020"
scope_role: primary
temporal_role: modern-empirical
related: ["[[范数、平坦性、Sharpness 与参数化不变性]]", "[[深度泛化证据地图与开放问题]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Fantastic Generalization Measures
> [!abstract] 来源定位
> 大规模比较多类深网 generalization measures，并用跨超参数 rank correlation 审计稳健性。本库调用 measure-selection、confounding 与 correlation boundary；不把排名当因果证明。
## 本库调用
1. generalization-measure benchmark；
2. controlled hyperparameter sweeps；
3. rank correlation；
4. measure failures/promising signals；
5. correlation vs causation。
