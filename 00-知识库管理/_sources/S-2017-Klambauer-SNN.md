---
type: source
status: active
area: [sources, neural-networks, selu, self-normalization]
source_type: paper
title: "Self-Normalizing Neural Networks"
author: [Günter Klambauer, Thomas Unterthiner, Andreas Mayr, Sepp Hochreiter]
year: 2017
url: "https://proceedings.neurips.cc/paper_files/paper/2017/hash/5d44ee6f2c3f71b73125876103c8f6c4-Abstract.html"
accessed: 2026-08-23
source_tier: A
venue: "NeurIPS 2017"
scope_role: theorem-and-mechanism
temporal_role: classic
related: ["[[ELU、SELU 与自归一化接口]]", "[[方差传播与宽层均值场近似]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Klambauer et al. 2017：Self-Normalizing Neural Networks

> [!abstract] 来源定位
> 原论文为 SELU 构造均值—方差映射、固定点与 contraction 条件，并配套 alpha dropout。本库用它推导 $(0,1)$ moment fixed point 与适用合同；结论不自动覆盖 residual、attention、normalization、强相关、有限宽或训练后任意权重分布。
