---
type: source
status: verified
source_type: paper
source_tier: A
title: "MaskGIT: Masked Generative Image Transformer"
author: "Huiwen Chang et al."
year: 2022
url: "https://arxiv.org/abs/2202.04200"
accessed: 2026-08-25
area: [sources, ai/generative-models, multimodal]
related: ["[[Absorbing-state、Mask Diffusion 与并行迭代生成]]", "[[图像 Token、掩码生成与多模态条件分布]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Chang et al.：MaskGIT

> [!abstract] 原始证据
> MaskGIT 在随机遮掩 token 上训练双向预测，采样从全 mask 开始并多轮并行预测、按置信度重新遮掩。课程采用其 iterative refinement 程序，并与严格 Markov absorbing diffusion 分开。

## 边界

- 并行预测使用条件独立因子化近似，不等于一次从完整 joint 精确采样。
- 置信度 schedule、温度与重复遮掩定义 sampler；只给轮数不能复现。
- 论文的加速倍数绑定 token 数、baseline 与硬件协议。
