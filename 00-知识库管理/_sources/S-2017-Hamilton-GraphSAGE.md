---
type: source
status: draft
area: [sources, architecture/gnn, inductive-learning]
source_type: paper
title: "Inductive Representation Learning on Large Graphs"
author: "William L. Hamilton, Rex Ying, Jure Leskovec"
year: 2017
url: "https://proceedings.neurips.cc/paper/2017/hash/5dd9db5e033da9c6fb5ba83c7a7ebea9-Abstract.html"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[消息传递神经网络的统一形式]]", "[[聚合器、可辨识性与 Graph Isomorphism Network]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Hamilton 等：GraphSAGE

> [!abstract] 来源定位
> 通过学习邻域聚合函数而不是为每个节点保存独立 embedding，建立采样式归纳节点表示框架。

## 边界

- “归纳”要求新节点/新图仍具备可用特征与相容的生成机制；
- 固定 fan-out 采样改变方差、覆盖范围和计算树，不能当作精确全邻域聚合；
- mean、pooling、LSTM aggregator 的顺序与置换性质不同，LSTM 版本需随机顺序或额外处理。

