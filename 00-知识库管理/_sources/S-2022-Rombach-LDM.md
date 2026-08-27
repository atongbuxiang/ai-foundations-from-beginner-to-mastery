---
type: source
status: verified
source_type: paper
source_tier: A
title: "High-Resolution Image Synthesis with Latent Diffusion Models"
author: "Robin Rombach et al."
year: 2022
url: "https://arxiv.org/abs/2112.10752"
accessed: 2026-08-25
area: [sources, ai/generative-models, diffusion]
related: ["[[Latent Diffusion、压缩瓶颈与两阶段误差]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Rombach et al.：Latent Diffusion Models

> [!abstract] 原始证据
> LDM 先训练感知 autoencoder，再在其连续 latent 上训练 diffusion；cross-attention 提供文本、框等条件。课程以它承担 latent diffusion 的两阶段定义和 computation–fidelity 折衷。

## 边界

- LDM 的 latent 通常是连续张量，不等于 VQ token；是否离散由 first-stage encoder 决定。
- autoencoder 的有损压缩限定可重构细节，diffusion 无法恢复被表示彻底丢弃的信息。
- 计算收益依赖空间下采样、channel、网络与硬件，不能只写“latent 更快”。
