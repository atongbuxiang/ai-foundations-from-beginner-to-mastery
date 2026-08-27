---
type: source
status: draft
area: [sources, scientific-spaces, kv-cache, mla]
source_type: blog
title: "缓存与效果的极限拉扯：从MHA、MQA、GQA到MLA"
author: "苏剑林"
year: 2024
url: "https://spaces.ac.cn/archives/10091"
accessed: 2026-08-24
source_tier: C
license: "Science Space; independent notes, no article mirroring"
scope_role: derivation-and-systems-bridge
related: ["[[KV Cache、MHA、MQA 与 GQA]]", "[[MLA、潜变量缓存与推理成本证据]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 科学空间：MHA、MQA、GQA 到 MLA 的 Cache 主线

> [!abstract] 来源定位
> 文章以 head/group/latent shapes 统一推导四种 attention，突出 generation 阶段反复读取 cache 的 bandwidth 瓶颈，并展示 MLA 训练形式与解码重参数化形式不同。

## Claim audit

- Cache scalars、group mapping、线性投影吸收在给定 shape 下为 `I`；
- BF16 下重参数化顺序可有数值差异；
- MLA generation 增加某些算术但减少 bytes，最终速度是 hardware/kernel 下 `E`。
