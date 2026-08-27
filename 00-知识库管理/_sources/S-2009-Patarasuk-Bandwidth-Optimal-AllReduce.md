---
type: source
status: verified
area: [sources, distributed-systems, collectives]
source_type: paper
title: "Bandwidth Optimal All-reduce Algorithms for Clusters of Workstations"
author: "Pitch Patarasuk, Xin Yuan"
year: 2009
url: "https://doi.org/10.1016/j.jpdc.2008.09.002"
accessed: 2026-08-26
source_tier: A
license: "Journal paper；知识库仅保存独立摘要与链接"
scope_role: collective-algorithms
temporal_role: foundational
related: ["[[数据并行、All-Reduce 与全局 Batch 语义]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Bandwidth Optimal All-reduce Algorithms

> [!abstract] 来源定位
> 论文给出大消息 All-Reduce 的通信下界与环式带宽最优算法，是推导 reduce-scatter + all-gather 数据量，而不是背诵“通信约为参数量”的主要来源。

## 可调用内容

- All-Reduce 等价于 reduction 后让所有 rank 获得结果；
- 对大消息，ring 路线把 tensor 分块并执行 reduce-scatter 与 all-gather；
- 每 rank 的主导发送量趋近 $2(P-1)M/P$；
- latency、拓扑、contention 与小消息会使带宽最优不等于最快。

## 边界

- 下界假设与网络模型必须声明；
- 现代 NCCL 会按拓扑和协议选择算法，不能只凭 ring 式预测 wall time；
- 浮点 reduction 的括号顺序还引入数值差异。
