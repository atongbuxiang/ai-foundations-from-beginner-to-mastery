---
type: source
status: draft
area: [sources, ai/transformers, mla, kv-cache]
source_type: technical-report
title: "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model"
author: "DeepSeek-AI"
year: 2024
url: "https://arxiv.org/abs/2405.04434"
accessed: 2026-08-24
source_tier: A
license: "arXiv and project repository; independent summary only"
scope_role: architecture-report
related: ["[[MLA、潜变量缓存与推理成本证据]]", "[[KV Cache、MHA、MQA 与 GQA]]"]
created: 2026-08-24
updated: 2026-08-24
---

# DeepSeek-V2：Multi-Head Latent Attention

> [!abstract] 来源定位
> DeepSeek-V2 提出联合低维 KV latent cache，并以可吸收的线性投影及 decoupled/partial RoPE 处理 score 与位置接口。报告同时含 MoE，MLA 效应不能从整模型比较中单独识别。

## 调用边界

- 线性投影吸收是精确代数重参数化的条件结论；RoPE 部分不能任意吸收；
- cache scalars 可精确计数，速度/吞吐仍依 kernel 和 bandwidth；
- 93.3% cache 减少与 5.76× throughput 是该报告比较协议的 `E`，不是通用常数。
