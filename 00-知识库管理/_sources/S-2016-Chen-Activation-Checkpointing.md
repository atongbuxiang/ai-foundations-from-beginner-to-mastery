---
type: source
status: verified
area: [sources, ai-training, activation-memory]
source_type: paper
title: "Training Deep Nets with Sublinear Memory Cost"
author: "Tianqi Chen, Bing Xu, Chiyuan Zhang, Carlos Guestrin"
year: 2016
url: "https://arxiv.org/abs/1604.06174"
accessed: 2026-08-26
source_tier: A
license: "arXiv paper；知识库仅保存独立摘要与链接"
scope_role: activation-checkpointing
temporal_role: foundational
related: ["[[ZeRO、FSDP、激活重计算与 Offload]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Training Deep Nets with Sublinear Memory Cost

> [!abstract] 来源定位
> 论文把 activation checkpointing 写成计算—内存权衡：只保存部分中间状态，反向时重算缺失前向段。它用于区分“state sharding”和“activation recomputation”。

## 可调用证据

- 对 $n$ 层链式网络可构造 $O(\sqrt n)$ activation memory 与额外 forward work 的方案；
- 更极端递归可继续降内存但增加更多计算；
- checkpoint placement 依赖计算图与张量大小；
- 论文展示深层网络的显著内存下降和运行开销。

## 边界

- 理论阶数不含 allocator、通信、attention workspace 和参数状态；
- 重算可能改变 RNG/dropout 或低精度运算顺序，必须保存/恢复状态；
- “重算一遍”只是规则链的简化，真实图需逐段记账。
