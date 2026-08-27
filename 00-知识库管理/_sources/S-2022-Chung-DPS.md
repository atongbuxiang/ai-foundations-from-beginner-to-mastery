---
type: source
status: verified
area: [sources, generative-models, diffusion, inverse-problems]
source_type: paper
title: "Diffusion Posterior Sampling for General Noisy Inverse Problems"
author: "Hyungjin Chung; Jeongsol Kim; Michael T. McCann; Marc L. Klasky; Jong Chul Ye"
year: 2022
url: "https://arxiv.org/abs/2209.14687"
venue: "ICLR 2023"
accessed: 2026-08-25
source_tier: A
scope_role: bridge
related: ["[[逆问题、约束采样与 Plug-and-Play 控制]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Chung et al.：Diffusion Posterior Sampling

> [!abstract] 来源定位
> 原论文把 diffusion prior 与 noisy nonlinear measurement likelihood 的近似 gradient 结合，用于 posterior sampling。课程用它说明 $y$ 观测 $x_0$ 时，$p(y\mid x_t)$ 通常不可直接计算，需要借 $\hat x_0(x_t)$ 等近似。

方法性结论必须附 forward operator、noise model、likelihood scale、gradient normalization、schedule 与 sampler。measurement consistency 不是 posterior calibration 的充分条件。
