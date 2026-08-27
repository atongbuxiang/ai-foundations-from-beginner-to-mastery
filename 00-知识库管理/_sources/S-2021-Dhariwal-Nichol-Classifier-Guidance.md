---
type: source
status: verified
area: [sources, generative-models, diffusion, guidance]
source_type: paper
title: "Diffusion Models Beat GANs on Image Synthesis"
author: "Prafulla Dhariwal; Alex Nichol"
year: 2021
url: "https://arxiv.org/abs/2105.05233"
venue: "NeurIPS 2021"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
related: ["[[条件生成、Bayes 分解与 Classifier Guidance]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Dhariwal–Nichol：Classifier Guidance

> [!abstract] 来源定位
> 原论文给出 noisy classifier gradient 引导 diffusion sampling，并实证展示 guidance scale 在 fidelity 与 diversity 间的权衡。课程用其作为 classifier guidance 的一级定义和实验来源。

调用边界：分类器必须在相应噪声层训练/校准；梯度要按 sampler 参数化转换；论文 ImageNet 结果不构成任意条件、任意模型上的保证。
