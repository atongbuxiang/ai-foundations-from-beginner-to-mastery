---
type: source
status: draft
area: [sources, scientific-spaces, moe, loss-free-balancing]
source_type: blog
title: "MoE环游记：3、换个思路来分配"
author: "苏剑林"
year: 2025
url: "https://spaces.ac.cn/archives/10757"
accessed: 2026-08-24
source_tier: C
license: "Science Space; independent notes, no article mirroring"
scope_role: feedback-balancing
related: ["[[Loss-Free 路由、偏置更新与分配视角]]", "[[MoE 负载均衡辅助损失与偏置]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 科学空间：Loss-Free Bias Feedback

> [!abstract] 来源定位
> 文章把 Expert 过载/欠载转成 Router selection bias 的外环反馈：高负载 Expert 降低选择偏置，低负载 Expert 提高偏置，而不把均衡项直接加进主 loss。

## Claim audit

- “loss-free”只表示不以可微正则项加入主目标，不表示没有超参数、状态或训练影响；
- bias 用于选择还是同时用于 gate weight，必须固定合同；
- 收敛、振荡和跨批/跨卡延迟属于控制系统问题，不能由更新方向直觉自动保证。
