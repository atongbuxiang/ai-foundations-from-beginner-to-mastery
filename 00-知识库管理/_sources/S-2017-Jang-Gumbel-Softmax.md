---
type: source
status: verified
source_type: paper
source_tier: A
title: "Categorical Reparameterization with Gumbel-Softmax"
author: "Eric Jang, Shixiang Gu, Ben Poole"
year: 2017
url: "https://arxiv.org/abs/1611.01144"
accessed: 2026-08-25
area: [sources, ai/generative-models, gradient-estimation]
related: ["[[Categorical Diffusion、转移矩阵与离散后验]]", "[[VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Jang et al.：Gumbel–Softmax

> [!abstract] 原始证据
> 论文用可微 Gumbel–Softmax 随机变量替代 non-differentiable categorical sample，并以温度退火逼近 categorical。课程用它承担 continuous relaxation 的原始定义。

## 边界

- finite temperature 的样本位于 simplex interior，优化的是松弛目标；
- $\tau\to0$ 的分布极限不保证稳定低方差梯度；
- hard straight-through 版本的反向规则仍是代理估计。
