---
type: source
status: draft
area: [sources, architecture/gnn, depth]
source_type: paper
title: "On the Bottleneck of Graph Neural Networks and its Practical Implications"
author: "Uri Alon, Eran Yahav"
year: 2021
url: "https://arxiv.org/abs/2006.05205"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[图网络深度、过平滑与过挤压]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Alon–Yahav：Over-squashing

> [!abstract] 来源定位
> 指出局部消息传递会把随距离快速增长的远程信息压入固定宽度表示，形成长程依赖瓶颈，并以受控任务和图结构分析支持该机制。

## 使用纪律

Over-squashing 是信息流瓶颈，over-smoothing 是表示趋同；两者可共存但不可互换。增加深度只扩大理论 receptive field，不保证远程信号有足够可辨梯度或容量。

