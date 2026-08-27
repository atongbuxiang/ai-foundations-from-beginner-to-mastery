---
type: source
status: active
area: [sources, importance-weighting, generalization-bounds]
source_type: paper
title: "Learning Bounds for Importance Weighting"
author: [Corinna Cortes, Yishay Mansour, Mehryar Mohri]
year: 2010
url: "https://papers.nips.cc/paper_files/paper/2010/hash/59c33016884a62116be975a9bb8257e3-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and moment conditions"
venue: "NeurIPS 2010"
scope_role: primary
temporal_role: theory
related: ["[[重要性加权与 Covariate Shift 校正]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Learning Bounds for Importance Weighting

> [!abstract] 来源定位
> 给出 importance-weighted learning 的泛化控制，揭示权重矩、Rényi-type divergence 与有效样本量的作用。本库调用其“无偏不等于低误差”边界；不把 bounded-weight 特例外推到任意 support mismatch。

## 本库调用

1. weighted empirical process 的复杂度；
2. weight tail/second moment 决定 concentration；
3. target/source divergence 进入 sample requirement；
4. 大权重使少数 source points 主导；
5. clipping 与 self-normalization 需单独计算偏差。
