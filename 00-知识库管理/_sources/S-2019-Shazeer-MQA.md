---
type: source
status: draft
area: [sources, ai/transformers, inference, kv-cache]
source_type: paper
title: "Fast Transformer Decoding: One Write-Head is All You Need"
author: "Noam Shazeer"
year: 2019
url: "https://arxiv.org/abs/1911.02150"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: method-paper
related: ["[[KV Cache、MHA、MQA 与 GQA]]"]
created: 2026-08-24
updated: 2026-08-24
---

# MQA：共享 K/V Head 的增量解码

> [!abstract] 来源定位
> MQA 保留多个 query heads、让所有 heads 共享一组 K/V，直接减少增量解码需要反复读取的 cache bytes。论文动机明确指向 memory bandwidth，而非只看 FLOPs。

## 调用边界

- Cache 压缩比由 KV-head 数与维度精确计算；
- 质量损失和速度收益是论文模型/硬件下的 `E`；
- kernel、batch、context、quantization 和并行布局会改变实际 crossover。
