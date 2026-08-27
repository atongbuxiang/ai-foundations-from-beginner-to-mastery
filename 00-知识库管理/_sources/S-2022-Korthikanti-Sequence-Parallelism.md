---
type: source
status: verified
area: [sources, distributed-training, sequence-parallelism, recomputation]
source_type: paper
title: "Reducing Activation Recomputation in Large Transformer Models"
author: "Vijay Korthikanti et al."
year: 2022
url: "https://arxiv.org/abs/2205.05198"
accessed: 2026-08-26
source_tier: A
license: "arXiv / MLSys paper；知识库仅保存独立摘要与链接"
scope_role: sequence-parallelism
temporal_role: active-method
related: ["[[Tensor、Pipeline、Sequence 与 Expert Parallel]]", "[[ZeRO、FSDP、激活重计算与 Offload]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Reducing Activation Recomputation in Large Transformer Models

> [!abstract] 来源定位
> 论文把 sequence parallelism 与 selective activation recomputation 组合，说明“切 sequence”常是与 tensor parallel 配套的 activation 内存策略，不应和任意 context-parallel attention 混为一词。

## 可调用证据

- 对 tensor-parallel 区域外、沿 sequence 可独立的算子分片 activation；
- selective recomputation 只重算内存收益高、计算代价相对低的部分；
- 论文报告 activation memory 与重算开销的显著下降；
- memory、extra FLOPs 与 collective 必须联合比较。

## 边界

- 适用切分依赖算子是否沿 sequence 独立；attention 的全序列依赖需特殊处理；
- 论文性能数字绑定 Megatron/NVIDIA 系统；
- 后续 context parallel 有不同通信语义，不能仅靠名称归并。
