---
type: source
status: draft
area: [sources, ai/moe, block-sparse, systems]
source_type: paper
title: "MegaBlocks: Efficient Sparse Training with Mixture-of-Experts"
author: "Trevor Gale et al."
year: 2022
url: "https://arxiv.org/abs/2211.15841"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: systems-paper
related: ["[[Expert Capacity、Dispatch 与 Token Dropping]]", "[[Expert Parallel、All-to-All 与通信成本]]"]
created: 2026-08-24
updated: 2026-08-24
---

# MegaBlocks：Dropless Block-Sparse MoE

> [!abstract] 来源定位
> MegaBlocks 用 block-sparse operations 处理动态 token–expert 分配，避免“drop tokens”与“padding 浪费”二选一，并给出 GPU 系统实验。

## 调用边界

- dropless 改变执行表示，不自动解决负载、网络 all-to-all 或尾延迟；
- 速度数字依 GPU、kernel、shape 与 Tutel/Megatron 版本；
- block sparsity 仍可能有分块碎片，必须报告有效与 padded workload。
