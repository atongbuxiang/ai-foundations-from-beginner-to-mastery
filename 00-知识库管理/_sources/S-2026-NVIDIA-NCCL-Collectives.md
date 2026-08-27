---
type: source
status: verified
area: [sources, distributed-systems, nccl, collectives]
source_type: official-documentation
title: "NCCL Collective Operations"
author: NVIDIA
year: 2026
url: "https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html"
accessed: 2026-08-26
source_tier: B
license: "NVIDIA 官方文档；知识库仅保存接口语义、独立摘要与链接"
scope_role: implementation
temporal_role: current
related: ["[[数据并行、All-Reduce 与全局 Batch 语义]]", "[[Tensor、Pipeline、Sequence 与 Expert Parallel]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# NVIDIA NCCL：Collective Operations

> [!abstract] 来源定位
> NCCL 对 AllReduce、Broadcast、ReduceScatter、AllGather 与 AllToAll 的接口语义来源。所有 rank 必须以匹配顺序参与 collective，否则可能等待或失败。

## 本卷调用

- AllReduce 使每 rank 获得 reduction 结果；
- ReduceScatter 把 reduction 后结果按块分给 ranks，AllGather 做相反的拼接复制；
- collective 的 count、dtype、operator、communicator 和调用顺序属于执行合同；
- rank 顺序的数学语义不等于浮点实现逐比特不受归约树影响。

## 边界

- 当前 NCCL 会按 topology/protocol/message size 选算法；
- API 语义不提供某集群的实际带宽/latency；
- 自定义 compression hook 会改变数值 estimator，不能仍称精确 AllReduce。
