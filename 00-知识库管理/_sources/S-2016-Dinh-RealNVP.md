---
type: source
status: verified
area: [sources, generative-models, normalizing-flows]
source_type: paper
title: "Density Estimation using Real NVP"
author: "Laurent Dinh; Jascha Sohl-Dickstein; Samy Bengio"
year: 2016
url: "https://arxiv.org/abs/1605.08803"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[Coupling Layer、NICE 与 RealNVP]]", "[[Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Dinh et al.：Real NVP

> [!abstract] 来源定位
> Real NVP 以 affine coupling、mask/permutation 与 multiscale architecture 获得 exact change-of-variables、sampling 和 latent inference。课程采用其结构公式，并把“数学 exact”限制为给定浮点实现/预处理下的模型密度，不等于真实数据 likelihood 无偏或样本语义好。

Affine coupling $y_A=x_A$、$y_B=x_B\odot e^{s(x_A)}+t(x_A)$ 的 logdet 为 $\sum_js_j(x_A)$，逆为 $x_B=(y_B-t(y_A))\odot e^{-s(y_A)}$。Scale clipping、round-trip residual、multiscale factor-out 和 dequantization 属于复现合同。

