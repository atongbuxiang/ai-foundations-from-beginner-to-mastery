---
type: source
status: verified
area: [sources, generative-models, invertible-networks]
source_type: paper
title: "Invertible Residual Networks"
author: "Jens Behrmann; Will Grathwohl; Ricky T. Q. Chen; David Duvenaud; Jörn-Henrik Jacobsen"
year: 2019
url: "https://proceedings.mlr.press/v97/behrmann19a.html"
venue: "ICML 2019"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[Residual Flow、可逆 ResNet 与 Logdet 估计]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Behrmann et al.：Invertible Residual Networks

> [!abstract] 来源定位
> 若 residual branch $g$ 的 Lipschitz constant 严格小于 1，则 $F=I+g$ 可逆，逆可由 fixed-point iteration 求解。Likelihood 需要 $\log\det(I+J_g)$ 的幂级数/trace 近似。课程将 sufficient invertibility certificate 与 estimator bias/variance 分离。

边界：谱归一化给的是实现上界/近似；接近 1 会令逆迭代变慢；有限截断 logdet 有 bias；数学可逆不等于浮点 round-trip 良好；后续 residual flow 改进不回写成原论文定理。

