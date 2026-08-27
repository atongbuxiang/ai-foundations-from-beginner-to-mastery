---
type: source
status: verified
area: [sources, generative-models, diffusion, variance]
source_type: paper
title: "Improved Denoising Diffusion Probabilistic Models"
author: "Alex Nichol; Prafulla Dhariwal"
year: 2021
url: "https://proceedings.mlr.press/v139/nichol21a.html"
venue: "ICML 2021"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[扩散简化损失、时间加权、Schedule 与 SNR]]", "[[反向均值、固定方差、学习方差与 Analytic-DPM]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Nichol–Dhariwal：Improved DDPM

> [!abstract] 来源定位
> 论文研究 learned reverse variance、hybrid/VLB objective、importance-sampled timesteps、cosine schedule 和更少 sampling steps。课程采用具体方法与指定实验，并把“order-of-magnitude fewer forward passes”保留为论文设置下的经验结论。

Learned variance、mean objective、schedule 和 evaluation 互相作用，不能把整篇结果归因给单一技巧。官方代码的 flags 是实现证据，不替代概率推导。

