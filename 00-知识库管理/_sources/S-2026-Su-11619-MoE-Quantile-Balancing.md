---
type: source
status: draft
area: [sources, scientific-spaces, moe, assignment, quantile]
source_type: blog
title: "MoE环游记：6、最优分配促均衡"
author: "苏剑林"
year: 2026
url: "https://spaces.ac.cn/archives/11619"
accessed: 2026-08-24
source_tier: C
license: "Science Space; independent notes, no article mirroring"
scope_role: assignment-dual-derivation
related: ["[[Loss-Free 路由、偏置更新与分配视角]]", "[[Expert Capacity、Dispatch 与 Token Dropping]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 科学空间：Optimal Assignment 与 Quantile Balancing

> [!abstract] 来源定位
> 文章把 token–expert routing 写成有行/列配额的 assignment，借对偶偏置与交替分位数更新近似求解，连接 BASE/BIP 与 Loss-Free 路线。

## Claim audit

- 给定 batch score matrix 的平衡 assignment 与训练中在线 Router 更新不是同一个优化对象；
- 松弛、min–max 交换、ties、整数可行性与有限轮 alternating quantile 都需写明；
- “无额外超参”不包括迭代数、统计窗口、EMA、分布式近似与实现选择。
