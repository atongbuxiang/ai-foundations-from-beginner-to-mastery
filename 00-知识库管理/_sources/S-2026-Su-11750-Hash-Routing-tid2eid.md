---
type: source
status: draft
area: [sources, scientific-spaces, moe, hash-routing]
source_type: blog
title: "DeepSeek V4的tid2eid是怎么来的？"
author: "苏剑林"
year: 2026
url: "https://spaces.ac.cn/archives/11750"
accessed: 2026-08-24
source_tier: C
license: "Science Space; independent notes, no article mirroring"
scope_role: contemporary-hypothesis
related: ["[[Router、Gate、Top-k 与稀疏组合]]", "[[MoE 门控归一化、证据地图与开放问题]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 科学空间：Token-ID Hash Routing 与 tid2eid

> [!abstract] 来源定位
> 文章讨论早层 context 较弱时用 token ID 预分配 Experts，并按 token frequency 构造较平衡的 tid2eid 表。

## Claim audit

- 文章明确说明具体 DeepSeek V4 表格生成细节未公开，所给 greedy 构造是作者推测；
- 若单 token 频率超过每 Expert 可承受份额，只依 token ID 的静态 mapping 无法完美均衡；
- 无 Router 参数不代表无数据依赖：词频估计、tokenizer、域漂移与多语言分布都会改变负载。
