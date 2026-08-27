---
type: source
status: draft
area: [sources, architecture/gnn, expressivity]
source_type: paper
title: "How Powerful are Graph Neural Networks?"
author: "Keyulu Xu, Weihua Hu, Jure Leskovec, Stefanie Jegelka"
year: 2019
url: "https://openreview.net/forum?id=ryGs6iA5Km"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[聚合器、可辨识性与 Graph Isomorphism Network]]", "[[WL 表达界、反例与 GNN 证据地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Xu 等：GIN

> [!abstract] 来源定位
> 用多重集函数分析 neighborhood aggregation，说明常见 mean/max 的碰撞，并在明确假设下构造达到 1-WL 区分能力的 GIN。

## 课程采用的断言

$$
h_v^{(k)}=\operatorname{MLP}^{(k)}\!\left((1+\epsilon^{(k)})h_v^{(k-1)}+\sum_{u\in\mathcal N(v)}h_u^{(k-1)}\right).
$$

“与 1-WL 一样强”限定在相应 MPNN 类、离散/可数标签、injective aggregation/update/readout 与足够容量假设下；它不是一般图同构判定器。

