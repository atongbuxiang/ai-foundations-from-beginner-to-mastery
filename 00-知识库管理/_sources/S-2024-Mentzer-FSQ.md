---
type: source
status: verified
source_type: paper
source_tier: A
title: "Finite Scalar Quantization: VQ-VAE Made Simple"
author: "Fabian Mentzer et al."
year: 2024
url: "https://arxiv.org/abs/2309.15505"
accessed: 2026-08-25
area: [sources, ai/generative-models, quantization]
related: ["[[Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Mentzer et al.：FSQ

> [!abstract] 原始证据
> FSQ 把 latent 投影到少量维度，并对每维量化到固定有限集合，隐式 codebook 是笛卡尔积。原论文报告在 MaskGIT/UViM 等任务上的竞争性表现，并强调无需 learned codebook、commitment loss 和 code reseeding。

## 边界

- “不发生传统 learned-codebook collapse”不等于组合 token 频率均匀。
- 相同名义 $K=\prod_jL_j$ 不保证相同几何、熵率或 rate–distortion。
- 竞争性结论限于论文任务和配置。
