---
type: source
status: verified
area: [sources, distributed-training, tensor-parallelism]
source_type: paper
title: "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism"
author: "Mohammad Shoeybi et al."
year: 2019
url: "https://arxiv.org/abs/1909.08053"
accessed: 2026-08-26
source_tier: A
license: "arXiv paper；知识库仅保存独立摘要与链接"
scope_role: tensor-parallelism
temporal_role: foundational
related: ["[[Tensor、Pipeline、Sequence 与 Expert Parallel]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Megatron-LM

> [!abstract] 来源定位
> 论文给出 Transformer 层内 tensor parallel 的经典结构：按列/行切分线性层，使相邻算子消化分片并把 collective 数量压缩到少数同步点。

## 可调用证据

- column-parallel 与 row-parallel 的切分轴决定中间 activation 是分片还是复制；
- MLP 与 attention 的切分需结合非线性/多头结构，不能任意切矩阵；
- forward/backward 的 All-Reduce/All-Gather 位置可从 shape 推导；
- 论文在 512 GPU、最高 8.3B 模型上报告当时的扩展效率。

## 边界

- 2019 实现与今天 Megatron-Core 的 sequence/context/expert parallel 不同；
- 论文性能依赖当时硬件和拓扑；
- “插入少量 collective”不等于通信成本可忽略。
