---
type: source
status: verified
area: [sources, ai-frameworks, fsdp, memory-sharding]
source_type: official-documentation
title: "FullyShardedDataParallel"
author: PyTorch
year: 2026
url: "https://docs.pytorch.org/docs/stable/fsdp.html"
accessed: 2026-08-26
source_tier: B
license: "PyTorch 官方文档；知识库仅保存版本行为、独立摘要与链接"
scope_role: implementation
temporal_role: current
related: ["[[ZeRO、FSDP、激活重计算与 Offload]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# PyTorch：FullyShardedDataParallel

> [!abstract] 来源定位
> 当前 FSDP sharding strategy 与 mixed-precision 接口来源。FULL_SHARD 在计算外分片参数/梯度/状态，并在 forward/backward 前后执行 all-gather、reduce-scatter 与 reshard。

## 本卷调用

- FULL_SHARD、SHARD_GRAD_OP、NO_SHARD 与 HYBRID_SHARD 的驻留/通信时序不同；
- param、reduce、buffer dtype 可分别设置，不能用一个“FSDP dtype”概括；
- wrap 粒度决定 full-parameter materialization 的峰值与通信频度；
- optimizer state dict、checkpoint 与 CPU offload 有独立格式/时序合同。

## 边界

- 官方 API 与限制会随版本变化；
- steady-state 分片比例不等于峰值显存；
- 与 ZeRO stage 的类比只用于资源对象，不能假设所有调度完全相同。
