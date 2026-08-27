---
type: source
status: verified
area: [sources, generative-models, diffusion]
source_type: paper
title: "Deep Unsupervised Learning using Nonequilibrium Thermodynamics"
author: "Jascha Sohl-Dickstein; Eric Weiss; Niru Maheswaranathan; Surya Ganguli"
year: 2015
url: "https://arxiv.org/abs/1503.03585"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[DDPM 前向 Markov 加噪与闭式边缘]]", "[[DDPM 反向后验、ELBO 与逐步 KL]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Sohl-Dickstein et al.：Nonequilibrium Diffusion

> [!abstract] 来源定位
> 论文系统提出逐步破坏数据结构并学习反向 diffusion 的生成建模路线，是 DDPM 的历史基础。课程从中采用 forward/reverse chain 与 variational probability bound 的历史骨架；现代 Gaussian parameterization、简化噪声目标与图像结果由后续 DDPM 论文承担。

原论文直接支持其方法和当时实验，不支持“任意缓慢 corruption 都容易反演”或有限 network/step 下的普遍收敛。

