---
type: source
status: verified
area: [sources, generative-models, diffusion, parameterization]
source_type: paper
title: "Progressive Distillation for Fast Sampling of Diffusion Models"
author: "Tim Salimans; Jonathan Ho"
year: 2022
url: "https://arxiv.org/abs/2202.00512"
venue: "ICLR 2022"
accessed: 2026-08-25
source_tier: A
scope_role: bridge
temporal_role: foundational
related: ["[[数据、噪声、速度与 Score 参数化]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Salimans–Ho：Progressive Distillation

> [!abstract] 来源定位
> 论文在少步 diffusion/distillation 中使用角度/velocity parameterization，并逐次把 $N$ 步 DDIM teacher 蒸馏为 $N/2$ 步 student。GEN-43 采用 $v=a_t\epsilon-s_tx_0$ 的旋转换算和数值尺度动机；蒸馏算法本身留到 50.9。

$x_0/\epsilon/v$ 可代数互换，不等于在给定网络、loss weighting 和低 SNR 下优化动态相同。

