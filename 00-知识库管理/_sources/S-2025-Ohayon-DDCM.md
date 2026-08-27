---
type: source
status: verified
source_type: paper
source_tier: A
title: "Compressed Image Generation with Denoising Diffusion Codebook Models"
author: "Guy Ohayon et al."
year: 2025
url: "https://arxiv.org/abs/2502.01189"
accessed: 2026-08-25
area: [sources, ai/generative-models, compression]
related: ["[[DDCM、离散生成路线比较与证据地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Ohayon et al.：DDCM

> [!abstract] 原始证据
> DDCM 把反向扩散每步的 Gaussian noise 采样替换为从预定义有限 iid Gaussian codebook 中选择，得到与样本共同产生的无损 bit-stream 表示；目标相关选择把同一构造用于有损压缩/条件生成。

## 边界

- “免额外训练”以已有预训练 diffusion 为前提，不表示编码无计算成本。
- noise code index 是采样随机性的离散化，不是图像 patch 的局部语义 code。
- 质量与压缩结论限于原论文模型、码率和感知指标。
