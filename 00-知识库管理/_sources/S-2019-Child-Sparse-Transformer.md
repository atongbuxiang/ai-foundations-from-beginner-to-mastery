---
type: source
status: draft
area: [sources, ai/transformers, sparse-attention]
source_type: paper
title: "Generating Long Sequences with Sparse Transformers"
author: "Rewon Child et al."
year: 2019
url: "https://arxiv.org/abs/1904.10509"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: method-paper
related: ["[[局部、分块与稀疏 Attention]]", "[[Attention 的二次复杂度、内存与 IO 瓶颈]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Sparse Transformer：稀疏分解、kernel 与长序列

> [!abstract] 来源定位
> 该工作用结构化稀疏 attention pattern 把 dense $n^2$ pair 数降到约 $n\sqrt n$，同时配套重计算和专用 kernel。复杂度结论针对指定 pattern；质量和 wall-clock 是论文实现与任务下的经验结果。

## 调用边界

- `I`：给定 pattern 的 edge 数和 receptive-path 可直接计数；
- `E`：长图像、音频和文本结果依模型、kernel 与硬件；
- 稀疏 mask 在 dense tensor 上实现，不会自动获得稀疏复杂度。
