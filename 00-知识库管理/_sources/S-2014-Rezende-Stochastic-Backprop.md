---
type: source
status: verified
area: [sources, generative-models/vae, gradient-estimation]
source_type: paper
title: "Stochastic Backpropagation and Approximate Inference in Deep Generative Models"
author: [Danilo Jimenez Rezende, Shakir Mohamed, Daan Wierstra]
year: 2014
url: "https://arxiv.org/abs/1401.4082"
accessed: 2026-08-25
source_tier: A
scope_role: core
temporal_role: classical
related: ["[[VAE 的 ELBO、变分后验与重参数化梯度]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Rezende、Mohamed 与 Wierstra：Stochastic Backpropagation

> [!abstract] 来源定位
> 论文与 AEVB 同期发展了连续 latent-variable model 的 stochastic backpropagation/pathwise gradient，并讨论深层生成模型中的 approximate inference。课程用它交叉验证重参数化并避免把方法史归于单一来源。

## 边界

Pathwise estimator 要求分布样本可表示为参数无关噪声的可微变换，并满足导数进入期望的正则条件；它通常降低但不保证最小方差，也不直接适用于离散 latent。

