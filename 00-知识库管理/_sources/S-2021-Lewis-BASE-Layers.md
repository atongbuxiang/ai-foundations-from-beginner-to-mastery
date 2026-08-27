---
type: source
status: draft
area: [sources, ai/moe, balanced-assignment]
source_type: paper
title: "BASE Layers: Simplifying Training of Large, Sparse Models"
author: "Mike Lewis et al."
year: 2021
url: "https://arxiv.org/abs/2103.16716"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: assignment-paper
related: ["[[Loss-Free 路由、偏置更新与分配视角]]", "[[Expert Capacity、Dispatch 与 Token Dropping]]"]
created: 2026-08-24
updated: 2026-08-24
---

# BASE Layers：Balanced Assignment

> [!abstract] 来源定位
> BASE 把 token–expert allocation 写成 linear assignment，以等量 token 配额直接保证 batch 内负载，并避免传统 auxiliary balancing loss。

## 调用边界

- assignment 的最优性针对给定 score 与等容量约束，不等于主任务全局最优；
- 求解、跨设备统计与 batch granularity 形成额外系统成本；
- 相等 token 数不等于相等实际执行时间，Expert shape 与 token cost 仍需固定。
