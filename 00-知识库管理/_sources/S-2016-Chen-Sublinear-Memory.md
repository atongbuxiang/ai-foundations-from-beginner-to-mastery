---
type: source
status: active
area: [sources, neural-networks, memory-efficiency, checkpointing]
source_type: paper
title: "Training Deep Nets with Sublinear Memory Cost"
author: [Tianqi Chen, Bing Xu, Chiyuan Zhang, Carlos Guestrin]
year: 2016
url: "https://arxiv.org/abs/1604.06174"
accessed: 2026-08-23
source_tier: A
venue: "arXiv:1604.06174"
scope_role: primary
temporal_role: foundational
related: ["[[Gradient Checking、Checkpointing 与高阶微分边界]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Chen et al. 2016：Training Deep Nets with Sublinear Memory
> [!abstract] 来源定位
> 深网络 activation checkpointing/rematerialization 的经典系统论文，给出 $n$ 层链的 $O(\sqrt n)$ 内存—额外前向工作权衡，并讨论更极端的 $O(\log n)$ 内存调度。本库不把链式渐近量直接外推为 Transformer/GPU 上的最优分割；真实结果还依 block bytes/FLOPs、skip connections、RNG/state 与 compiler。
