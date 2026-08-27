---
type: source
status: verified
area: [sources, generative-models, diffusion, likelihood]
source_type: paper
title: "Variational Diffusion Models"
author: "Diederik P. Kingma; Tim Salimans; Ben Poole; Jonathan Ho"
year: 2021
url: "https://arxiv.org/abs/2107.00630"
accessed: 2026-08-25
source_tier: A
scope_role: bridge
temporal_role: foundational
related: ["[[扩散简化损失、时间加权、Schedule 与 SNR]]", "[[DDPM 反向后验、ELBO 与逐步 KL]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Kingma et al.：Variational Diffusion Models

> [!abstract] 来源定位
> VDM 以 signal-to-noise ratio 组织连续/离散 diffusion likelihood，并研究可学习 schedule。GEN-44 用它建立 log-SNR 与 loss-weight 的语言；DDPM 的离散公式仍以原论文为主。

“同一端点下 schedule 的 VLB 性质”依赖连续时间/parameterization/weighting 假设，不能无条件迁移到有限步 sampler 质量。

