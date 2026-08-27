---
type: source
status: verified
area: [sources, generative-models, autoregressive-flows]
source_type: paper
title: "Masked Autoregressive Flow for Density Estimation"
author: "George Papamakarios; Theo Pavlakou; Iain Murray"
year: 2017
url: "https://arxiv.org/abs/1705.07057"
venue: "NeurIPS 2017"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[Autoregressive Flow、MAF 与 IAF 的方向权衡]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Papamakarios et al.：MAF

> [!abstract] 来源定位
> MAF 让 $z_i=(x_i-\mu_i(x_{<i}))/\sigma_i(x_{<i})$：给定完整 $x$，masked network 可并行算全部 density 参数；从 $z$ 生成 $x$ 却需按维度递归。论文将 MAF、IAF、RealNVP 置于同一 triangular-flow 视角。

课程用它建立“同一双射，选哪个方向作为模型 forward 会交换 density evaluation 与 sampling 成本”的严格账；MAF 的“适合 density estimation”不是说 sample 无法生成，只是串行 critical path 长。

