---
type: source
status: verified
source_type: paper
source_tier: A
title: "Neural Discrete Representation Learning"
author: "Aaron van den Oord, Oriol Vinyals, Koray Kavukcuoglu"
year: 2017
url: "https://arxiv.org/abs/1711.00937"
accessed: 2026-08-25
area: [sources, ai/generative-models, representation-learning]
related: ["[[VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]", "[[图像 Token、掩码生成与多模态条件分布]]"]
created: 2026-08-25
updated: 2026-08-25
---

# van den Oord et al.：VQ-VAE

> [!abstract] 原始证据
> 论文提出用 nearest-neighbor vector quantization 学离散 latent，以 straight-through estimator 训练 encoder，并另学 autoregressive prior。课程以它承担 VQ-VAE 的结构、损失与两阶段生成定义。

## 边界

- 离散 posterior 与 learned prior 是生成模型组成；只训练重构 autoencoder 不能从 prior 生成。
- “缓解 posterior collapse”是相对特定连续 VAE/强 decoder 的机制与实验，不是所有设置的定理。
- STE、codebook update 与 commitment loss 的具体权重/优化器必须记录。
