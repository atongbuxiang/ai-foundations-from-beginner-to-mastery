---
type: source
status: active
area: [sources, learning-theory, em, convergence]
source_type: paper
title: "On the Convergence Properties of the EM Algorithm"
author: [C. F. Jeff Wu]
year: 1983
url: "https://doi.org/10.1214/aos/1176346060"
accessed: 2026-08-23
source_tier: A
license: "Annals of Statistics article; retain citation and independent summary"
venue: "Annals of Statistics 11(1), 95–103"
scope_role: primary
temporal_role: classical-foundation
related: ["[[潜变量模型、混合模型与 EM]]", "[[一阶最优性条件与梯度下降]]"]
created: 2026-08-23
updated: 2026-08-23
---

# On the Convergence Properties of the EM Algorithm

> [!abstract] 来源定位
> Wu 区分 likelihood monotonicity、limit-point stationarity与parameter-sequence convergence，并给出使这些结论成立的条件。本库据此禁止把“EM loss每轮改善”直接写成“EM收敛到MLE”。

## 本库调用

1. EM limit point是否 stationary需要 continuity、closedness与regularity条件；
2. parameter iterates收敛比 likelihood values收敛更强；
3. unimodality/uniqueness等额外条件才可能推出唯一 MLE；
4. boundary、singularity、noncompact parameter space与approximate E/M steps需单独处理。
