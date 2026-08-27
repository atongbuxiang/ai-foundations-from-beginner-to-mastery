---
type: source
status: verified
area: [sources, distributed-training, pipeline-parallelism]
source_type: paper
title: "GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism"
author: "Yanping Huang et al."
year: 2019
url: "https://arxiv.org/abs/1811.06965"
accessed: 2026-08-26
source_tier: A
license: "arXiv / NeurIPS paper；知识库仅保存独立摘要与链接"
scope_role: pipeline-parallelism
temporal_role: foundational
related: ["[[Tensor、Pipeline、Sequence 与 Expert Parallel]]", "[[ZeRO、FSDP、激活重计算与 Offload]]"]
created: 2026-08-26
updated: 2026-08-26
---

# GPipe

> [!abstract] 来源定位
> GPipe 把层序列分到多个 stage，再把 mini-batch 切成 micro-batches 填充流水线；它是推导 pipeline bubble、跨 stage activation 通信与同步 batch 语义的主要来源。

## 可调用证据

- 流水线并行切的是层/计算图深度，而非 batch 或单层矩阵；
- micro-batch 数越多，fill/drain bubble 的相对比例通常越小；
- stage 边界要传 activation，反向还要传 activation gradient；
- activation checkpointing 可降低 stage 内存但增加重算。

## 边界

- GPipe 的同步 schedule 不是所有 1F1B/interleaved/PipeDream schedule；
- stage 平衡取决于真实 kernel 时间和通信，不只按层数平均；
- micro-batch 改变可能同时影响数值 kernel、归一化和优化时钟。
