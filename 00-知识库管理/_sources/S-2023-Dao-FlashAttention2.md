---
type: source
status: draft
area: [sources, ai/transformers, flashattention, gpu]
source_type: paper
title: "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning"
author: "Tri Dao"
year: 2023
url: "https://arxiv.org/abs/2307.08691"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: algorithm-paper
related: ["[[FlashAttention、精确计算与 IO Awareness]]"]
created: 2026-08-24
updated: 2026-08-24
---

# FlashAttention-2：并行划分与非 Matmul 工作

> [!abstract] 来源定位
> FA2 在相同 exact-attention 路线上重分 thread blocks/warps，并减少非矩阵乘工作，以提高 occupancy 与有效吞吐。

## 调用边界

- 算法族版本不能混写；不同 GPU、head dimension、causal mode 和 sequence length 的收益不同；
- kernel TFLOPs、attention-layer speedup 与 end-to-end model throughput 是三种指标。
