---
type: source
status: draft
area: [sources, architecture/gnn, graph-attention]
source_type: paper
title: "Graph Attention Networks"
author: "Petar Veličković, Guillem Cucurull, Arantxa Casanova, Adriana Romero, Pietro Liò, Yoshua Bengio"
year: 2018
url: "https://openreview.net/forum?id=rJXMpikCZ"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[图注意力与结构偏置]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Veličković 等：GAT

> [!abstract] 来源定位
> 在被图结构 mask 的邻域内计算输入依赖的 attention coefficient，并用 multi-head 聚合节点表示。

## 课程采用的断言

$$
e_{ij}=a(Wh_i,Wh_j),\qquad
\alpha_{ij}=\operatorname{softmax}_{j\in\mathcal N(i)}e_{ij}.
$$

归一化域是目标节点的邻域，而非整图。GAT 仍是局部 message passing；注意力权重不自动构成因果解释，也不自动越过标准 1-WL 表达边界。

