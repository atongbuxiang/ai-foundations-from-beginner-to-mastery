---
type: source
status: draft
area: [sources, architecture/gnn, depth]
source_type: paper
title: "Graph Neural Networks Exponentially Lose Expressive Power for Node Classification"
author: "Kenta Oono, Taiji Suzuki"
year: 2020
url: "https://openreview.net/forum?id=S1ldO2EFPr"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[图网络深度、过平滑与过挤压]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Oono–Suzuki：深层 GNN 表达退化

> [!abstract] 来源定位
> 把 GCN 类传播视为动力系统，在权重与增广归一化 Laplacian 谱满足条件时，证明表示指数接近只携带连通分量与度信息的子空间。

## 使用纪律

课程将其作为条件化 over-smoothing 理论，不写成“所有深 GNN 必然指数坍缩”。残差、归一化、异配结构、非线性和训练得到的权重都会改变适用条件。

