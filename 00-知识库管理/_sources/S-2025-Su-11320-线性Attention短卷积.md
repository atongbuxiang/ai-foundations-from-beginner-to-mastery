---
type: source
status: draft
area: [sources, scientific-spaces, linear-attention, convolution]
source_type: blog
title: "为什么线性注意力要加Short Conv？"
author: "苏剑林"
year: 2025
url: "https://spaces.ac.cn/archives/11320"
accessed: 2026-08-24
source_tier: C
license: "Science Space; independent notes, no article mirroring"
scope_role: mechanism-hypothesis
related: ["[[核特征、线性 Attention 与结合律重排]]", "[[局部、分块与稀疏 Attention]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 科学空间：线性 Attention 为什么加 Short Conv

> [!abstract] 来源定位
> 文章尝试解释显式局部卷积如何补充线性/递归状态对短程 token shift、局部顺序和高分辨率关系的建模缺口。

## Claim audit

- 卷积 receptive field 与额外成本可复算；
- “补局部缺口”是机制解释 `H`，作者也把文章定位为自构分析；
- 是否必要、最优 kernel size 与不同线性 attention 家族的收益必须由匹配消融回答。
