---
type: source
status: verified
area: [sources, distributed-training, memory-sharding]
source_type: paper
title: "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models"
author: "Samyam Rajbhandari et al."
year: 2020
url: "https://doi.org/10.1109/SC41405.2020.00024"
accessed: 2026-08-26
source_tier: A
license: "IEEE SC paper；知识库仅保存独立摘要与链接"
scope_role: state-sharding
temporal_role: foundational
related: ["[[ZeRO、FSDP、激活重计算与 Offload]]", "[[数据并行、All-Reduce 与全局 Batch 语义]]"]
created: 2026-08-26
updated: 2026-08-26
---

# ZeRO

> [!abstract] 来源定位
> ZeRO 将数据并行中冗余复制的 optimizer states、gradients 和 parameters 分阶段分片，是本卷每参数内存账与通信重建的原始来源。

## 可调用证据

- stage 1 分片 optimizer states；stage 2 再分片 gradients；stage 3 再分片 parameters；
- 分片降低每 rank steady-state memory，但需要 reduce-scatter、all-gather 等动态通信；
- 论文区分 model states 与 residual states（activation、buffer、fragmentation 等）；
- 数据并行语义可保留，但瞬时 materialization 和通信峰值必须另外计算。

## 边界

- “除以 world size”只适合被完整均匀分片的 steady state 项；
- bucket、prefetch、临时 full parameter 和 allocator 会决定真实峰值；
- ZeRO 术语与具体框架版本/配置需单独核对。
