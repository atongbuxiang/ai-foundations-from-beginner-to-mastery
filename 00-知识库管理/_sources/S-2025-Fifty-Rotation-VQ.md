---
type: source
status: verified
source_type: paper
source_tier: A
title: "Restructuring Vector Quantization with the Rotation Trick"
author: "Christopher Fifty et al."
year: 2025
url: "https://arxiv.org/abs/2410.06424"
accessed: 2026-08-25
area: [sources, ai/generative-models, optimization]
related: ["[[Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Fifty et al.：VQ Rotation Trick

> [!abstract] 原始证据
> 论文用旋转与缩放把 encoder output 变到所选 code，反向把该线性变换当作常量，从而让量化角度与尺度进入代理梯度。论文在多种 VQ-VAE 训练配置中报告重构、利用率和量化误差改善。

## 边界

- 这是 surrogate Jacobian 设计，不是 hard argmin 的真实导数。
- 原论文平均改善与某个新配置的失败可同时成立；课程保留初始化、范数比和 loss scale 审计。
