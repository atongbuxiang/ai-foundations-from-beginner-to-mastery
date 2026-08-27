---
type: source
status: draft
area: [sources, ai/moe, sharding, routing]
source_type: paper
title: "GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding"
author: "Dmitry Lepikhin et al."
year: 2020
url: "https://arxiv.org/abs/2006.16668"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: scale-system-paper
related: ["[[Expert Capacity、Dispatch 与 Token Dropping]]", "[[Expert Parallel、All-to-All 与通信成本]]"]
created: 2026-08-24
updated: 2026-08-24
---

# GShard：Top-2 Gating 与自动分片

> [!abstract] 来源定位
> GShard 把稀疏 MoE Transformer 扩到大规模多设备，连接 Top-2 routing、capacity、dispatch 与编译器自动 sharding。

## 调用边界

- 600B 与 2048 TPU 等数字是该多语翻译系统的 `E`；
- 自动分片降低表达系统并行的门槛，不消除 all-to-all、负载和拓扑成本；
- Top-2、capacity 和 auxiliary terms 是具体设计，不是 MoE 唯一定义。
