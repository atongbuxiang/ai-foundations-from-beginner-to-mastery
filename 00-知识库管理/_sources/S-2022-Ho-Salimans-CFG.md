---
type: source
status: verified
area: [sources, generative-models, diffusion, classifier-free-guidance]
source_type: paper
title: "Classifier-Free Diffusion Guidance"
author: "Jonathan Ho; Tim Salimans"
year: 2022
url: "https://arxiv.org/abs/2207.12598"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
related: ["[[Classifier-Free Guidance、尺度与质量多样性前沿]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Ho–Salimans：Classifier-Free Diffusion Guidance

> [!abstract] 来源定位
> 原论文联合训练 conditional/unconditional score estimates，并在采样时线性组合，以换取 quality–diversity trade-off。它承担 CFG 的一级定义。

本卷固定公式 $r_{cfg}=r_u+w(r_c-r_u)$：$w=0$ 是无条件，$w=1$ 是普通条件，$w>1$ 是外推。若库使用 shifted scale，必须显式换算；$r$ 还必须说明是 score、noise、velocity 还是 data prediction。
