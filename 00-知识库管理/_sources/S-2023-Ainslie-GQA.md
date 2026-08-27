---
type: source
status: draft
area: [sources, ai/transformers, inference, gqa]
source_type: paper
title: "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints"
author: "Joshua Ainslie et al."
year: 2023
url: "https://arxiv.org/abs/2305.13245"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: method-paper
related: ["[[KV Cache、MHA、MQA 与 GQA]]"]
created: 2026-08-24
updated: 2026-08-24
---

# GQA：Query Heads 与 KV Groups 的中间谱系

> [!abstract] 来源定位
> GQA 使用介于 1 与 query-head 数之间的 KV groups，并研究从 MHA checkpoint uptraining 的方法；MHA 和 MQA 是两个端点。

## 调用边界

- $h_q/h_{kv}$ 的 head mapping 与 cache 比例是结构事实；
- “接近 MHA 质量、接近 MQA 速度”限定论文模型、uptraining 预算与硬件；
- 参数对齐、FFN 补偿与 tensor parallel 映射必须单列。
