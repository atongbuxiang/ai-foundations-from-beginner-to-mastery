---
type: source
status: verified
source_type: paper
source_tier: A
title: "DiVeQ: Differentiable Vector Quantization Using the Reparameterization Trick"
author: "Mohammad Hassan Vali, Tom Bäckström, Arno Solin"
year: 2025
url: "https://arxiv.org/abs/2509.26469"
accessed: 2026-08-25
area: [sources, ai/generative-models, quantization]
related: ["[[Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Vali et al.：DiVeQ

> [!abstract] 原始证据
> DiVeQ 把 hard quantization 表示为加入模拟 quantization distortion 的 error vector，保持 hard forward 并让 codebook 获得梯度；论文还给出 space-filling 变体并报告无需 auxiliary loss/temperature schedule 的实验。

## 边界

- “differentiable”指所定义的 surrogate computation/gradient path，不意味着 nearest-neighbor argmin 本身处处可微。
- SF-DiVeQ 与基础 DiVeQ 是不同方法；利用率、重构和生成结论需分开报告。
