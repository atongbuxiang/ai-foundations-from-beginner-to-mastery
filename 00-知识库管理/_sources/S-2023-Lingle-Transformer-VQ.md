---
type: source
status: draft
area: [sources, ai/transformers, vector-quantization, efficient-attention]
source_type: paper
title: "Transformer-VQ: Linear-Time Transformers via Vector Quantization"
author: "Lucas D. Lingle"
year: 2023
url: "https://arxiv.org/abs/2309.16354"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: method-paper
related: ["[[局部、分块与稀疏 Attention]]", "[[核特征、线性 Attention 与结合律重排]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Transformer-VQ：量化 Key 与聚合 Cache

> [!abstract] 来源定位
> Transformer-VQ 把 keys 映射到有限 codebook，从而可按 code 聚合 causal softmax 的分子和分母，以线性时间处理序列；误差入口是 key quantization 与训练机制。

## 调用边界

- 线性复杂度以 codebook size 不随长度同阶增长为前提；
- 仍保留 softmax 形式不代表与原 dense keys 完全相同；
- 论文速度/质量依专用实现、序列长度与模型配置。
