---
type: source
status: verified
area: [sources, generative-models/vae, directional-statistics]
source_type: paper
title: "Hyperspherical Variational Auto-Encoders"
author: [Tim R. Davidson, Luca Falorsi, Nicola De Cao, Thomas Kipf, Jakub M. Tomczak]
year: 2018
url: "https://arxiv.org/abs/1804.00891"
accessed: 2026-08-25
source_tier: A
scope_role: core
temporal_role: classical
related: ["[[层次 VAE、表达性先验与近似后验 Flow]]", "[[S-2021-Su-8404-vMF-VAE]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Davidson et al.：Hyperspherical VAE

> [!abstract] 来源定位
> 论文用 vMF approximate posterior 与超球面 latent 处理具有方向/球面结构的数据，并在指定低维实验中比较 Gaussian VAE。它承担方法定义和实验；“球面 latent 普遍优于 Gaussian”不成立。

课程检查样本空间、surface measure、normalization constant、rejection sampling/reparameterized gradient、固定或可学习浓度以及与均匀 spherical prior 的 KL。

