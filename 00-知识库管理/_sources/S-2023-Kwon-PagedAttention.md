---
type: source
status: verified
area: [sources, language-models, serving, kv-cache]
source_type: paper
title: "Efficient Memory Management for Large Language Model Serving with PagedAttention"
author: "Woosuk Kwon et al."
year: 2023
url: "https://doi.org/10.1145/3600006.3613165"
accessed: 2026-08-26
source_tier: P1
license: "SOSP paper; independent summary"
scope_role: paged-kv-memory
related: ["[[Prefill、Decode、KV Cache 与 Continuous Batching]]"]
created: 2026-08-26
updated: 2026-08-26
---

# PagedAttention：把 KV cache 管理问题显式化

> [!abstract] 来源定位
> 论文以类似虚拟内存分页的块管理减少 KV cache 内外部碎片，并支持跨序列共享，构建 vLLM serving system。课程采用 logical block→physical block 映射、fragmentation 与 copy-on-write 账。

它不改变模型概率分布；吞吐增益依请求长度分布、硬件、scheduler 与对照系统。
