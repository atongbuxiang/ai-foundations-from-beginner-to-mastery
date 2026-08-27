---
type: source
status: active
area: [sources, learning-theory, k-means, approximation-algorithms]
source_type: paper
title: "k-means++: The Advantages of Careful Seeding"
author: [David Arthur, Sergei Vassilvitskii]
year: 2007
url: "https://research.google/pubs/k-means-the-advantages-of-careful-seeding/"
accessed: 2026-08-23
source_tier: A
license: "SODA paper; author PDF available, retain citation"
venue: "SODA 2007, 1027–1035"
scope_role: primary
temporal_role: classical-foundation
related: ["[[K-Means、聚类风险与不可辨识性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# k-means++: The Advantages of Careful Seeding

> [!abstract] 来源定位
> Arthur 与 Vassilvitskii 用 squared-distance proportional seeding改善 K-Means初始化，并对初始 potential给 expected logarithmic approximation guarantee。本库用它说明 initialization guarantee、Lloyd descent与 statistical recovery是三件事。

## 本库调用

1. 第一个 center均匀选取，后续按到已有 centers的 squared distance加权；
2. seeding guarantee比较的是 K-Means objective与 global optimum；
3. 后续 Lloyd updates不增加 objective；
4. approximation factor不保证真实 cluster labels、稳定性或 deployment utility；
5. randomness必须通过多 seeds与完整 selection protocol审计。
