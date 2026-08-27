---
type: source
status: draft
area: [sources, scientific-spaces, performer, random-features]
source_type: blog
title: "Performer：用随机投影将Attention的复杂度线性化"
author: "苏剑林"
year: 2020
url: "https://spaces.ac.cn/archives/7921"
accessed: 2026-08-24
source_tier: C
license: "Science Space; independent notes, no article mirroring"
scope_role: derivation-and-critique
related: ["[[Performer、随机特征与近似误差]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 科学空间：Performer 随机投影

> [!abstract] 来源定位
> 文章重写正随机特征恒等式，讨论正交随机特征降方差与实际 crossover。它适合初学者理解“无偏 kernel 估计”和“归一化后 attention 误差”不是同一层。

## Claim audit

- Gaussian 指数矩恒等式为 `I`；有限 features 为随机估计；
- 正交化方差与精度回查 Performer 原论文；
- “价值打问号”等工程判断限定作者当时硬件/实现，不作为长期裁决。
