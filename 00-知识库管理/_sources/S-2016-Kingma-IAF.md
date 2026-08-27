---
type: source
status: verified
area: [sources, generative-models, autoregressive-flows, variational-inference]
source_type: paper
title: "Improving Variational Inference with Inverse Autoregressive Flow"
author: "Diederik P. Kingma; Tim Salimans; Rafal Jozefowicz; Xi Chen; Ilya Sutskever; Max Welling"
year: 2016
url: "https://arxiv.org/abs/1606.04934"
venue: "NeurIPS 2016"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[Autoregressive Flow、MAF 与 IAF 的方向权衡]]", "[[层次 VAE、表达性先验与近似后验 Flow]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Kingma et al.：IAF

> [!abstract] 来源定位
> IAF 以 base noise 的 autoregressive functions 构造 $x_i=\mu_i(z_{<i})+\sigma_i(z_{<i})z_i$，因此给定全体 $z$ 可并行 sample/transform 并计算 triangular logdet；反求 $z$ 通常串行。原论文主要角色是高维 variational posterior，而非默认数据-space density estimator。

与 MAF 的关系必须写清变量方向、调用任务和缓存对象，不能仅说“互为逆”后忽略计算图 critical path。

