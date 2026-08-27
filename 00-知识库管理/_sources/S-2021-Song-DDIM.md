---
type: source
status: verified
area: [sources, generative-models, diffusion, ddim]
source_type: paper
title: "Denoising Diffusion Implicit Models"
author: "Jiaming Song; Chenlin Meng; Stefano Ermon"
year: 2021
url: "https://arxiv.org/abs/2010.02502"
venue: "ICLR 2021"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[DDIM、非 Markov 前向族与确定性采样]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Song–Meng–Ermon：DDIM

> [!abstract] 来源定位
> DDIM 构造与 DDPM 拥有相同训练边缘/目标的一族非 Markov forward processes，并给出可确定性的 reverse sampler 与时间子序列加速。论文直接支持其构造和 2021 实验；不支持“任意大跳步无误差”或“确定性等于 exact inversion”。

课程必须同时报告 timestep subsequence、$\eta$、prediction parameterization、clipping 和 NFE；这些共同定义有限步 sampler。

