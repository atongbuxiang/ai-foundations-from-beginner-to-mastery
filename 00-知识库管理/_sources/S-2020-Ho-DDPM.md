---
type: source
status: verified
area: [sources, generative-models, diffusion, ddpm]
source_type: paper
title: "Denoising Diffusion Probabilistic Models"
author: "Jonathan Ho; Ajay Jain; Pieter Abbeel"
year: 2020
url: "https://arxiv.org/abs/2006.11239"
venue: "NeurIPS 2020"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[DDPM 前向 Markov 加噪与闭式边缘]]", "[[DDPM 反向后验、ELBO 与逐步 KL]]", "[[数据、噪声、速度与 Score 参数化]]", "[[最小 DDPM 的张量合同、复现门与证据地图]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Ho–Jain–Abbeel：DDPM

> [!abstract] 来源定位
> DDPM 固定线性 Gaussian forward chain，闭式得到任意 $q(x_t\mid x_0)$ 和 posterior $q(x_{t-1}\mid x_t,x_0)$，以 learned Gaussian reverse chain 最大化 variational bound，并提出与 denoising score matching 相连的 noise-prediction 训练。GEN-41—44、48 以此为一级主来源。

## 课程边界

- 原论文常用 $\beta_t$ 为 variance、$\alpha_t=1-\beta_t$、$\bar\alpha_t=\prod_{s\le t}\alpha_s$；
- `L_simple` 删除/重排 ELBO 的 timestep 权重，不能在有限网络中与 exact ELBO 当同一目标；
- forward closed form 与 reverse network accuracy 是不同命题；
- 论文 benchmark 是 2020 设置，不作为当前家族胜负。

