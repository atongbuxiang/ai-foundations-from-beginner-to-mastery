---
type: source
status: draft
area: [sources, ai/moe, switch-transformer]
source_type: paper
title: "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity"
author: "William Fedus, Barret Zoph, Noam Shazeer"
year: 2021
url: "https://arxiv.org/abs/2101.03961"
accessed: 2026-08-24
source_tier: A
license: "arXiv/JMLR; independent summary only"
scope_role: routing-system-paper
related: ["[[Router、Gate、Top-k 与稀疏组合]]", "[[Expert Capacity、Dispatch 与 Token Dropping]]", "[[MoE 负载均衡辅助损失与偏置]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Switch Transformer：Top-1 Routing

> [!abstract] 来源定位
> Switch 以每 token Top-1 简化 routing 与通信，并系统讨论 capacity、token dropping、load balancing、低精度稳定和与 Dense T5 的比较。

## 调用边界

- “constant computational cost”需固定 activated expert width/k，并另计 router、dispatch、padding 与通信；
- capacity factor 是吞吐、dropping 与内存之间的系统参数；
- speedup/质量是特定 T5、数据、硬件与训练预算的 `E`。
