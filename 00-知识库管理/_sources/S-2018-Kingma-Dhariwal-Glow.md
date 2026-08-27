---
type: source
status: verified
area: [sources, generative-models, normalizing-flows]
source_type: paper
title: "Glow: Generative Flow with Invertible 1x1 Convolutions"
author: "Diederik P. Kingma; Prafulla Dhariwal"
year: 2018
url: "https://proceedings.neurips.cc/paper/2018/hash/d139db6a236200b21cc7f752979132d0-Abstract.html"
venue: "NeurIPS 2018"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Kingma–Dhariwal：Glow

> [!abstract] 来源定位
> Glow 用 ActNorm、可逆 $1\times1$ convolution 与 affine coupling 组成 flow step。$W\in\mathbb R^{C\times C}$ 作用于每个 spatial location，因此总 logdet 为 $HW\log|\det W|$。课程同时审计 LU 参数化、初始 batch、最小奇异值与多尺度 split。

论文直接支持架构与其 benchmark；不支持“exact likelihood 自动带来 OOD detection”“linear latent direction 必然语义可控”或任意分辨率的训练成本结论。

