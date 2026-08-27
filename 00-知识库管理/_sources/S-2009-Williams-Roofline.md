---
type: source
status: verified
area: [sources, computer-systems, roofline]
source_type: paper
title: "Roofline: An Insightful Visual Performance Model for Multicore Architectures"
author: "Samuel Williams, Andrew Waterman, David Patterson"
year: 2009
url: "https://doi.org/10.1145/1498765.1498785"
accessed: 2026-08-26
source_tier: A
license: "CACM paper；知识库仅保存独立摘要与链接"
scope_role: performance-model
temporal_role: foundational
related: ["[[通信 Roofline、非确定性与分布式训练证据地图]]", "[[Tensor、Pipeline、Sequence 与 Expert Parallel]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Roofline

> [!abstract] 来源定位
> Roofline 用 arithmetic intensity 把峰值计算吞吐与峰值内存带宽合成上界：$P\le\min(P_{peak},B\,I)$。本卷再把同一思想扩展为计算与 collective 通信的时间下界分账。

## 可调用内容

- arithmetic intensity 是 FLOPs/byte，不是“模型参数量”；
- ridge point $I^*=P_{peak}/B$ 区分 bandwidth-bound 与 compute-bound；
- 上界用于定位瓶颈，实际性能还受 latency、occupancy、cache 与算法效率影响；
- 不同 kernel 的 intensity 不可用整模型一个平均数掩盖。

## 边界

- 原 Roofline 主要建模处理器/内存，不直接给网络 collective 公式；
- 通信 roofline 是课程类比扩展，必须另写 latency/bandwidth/topology；
- 达不到 roof 不等于只有一个原因。
