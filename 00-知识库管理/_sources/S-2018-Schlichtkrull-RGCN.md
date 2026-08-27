---
type: source
status: draft
area: [sources, architecture/gnn, relational-graphs]
source_type: paper
title: "Modeling Relational Data with Graph Convolutional Networks"
author: "Michael Schlichtkrull, Thomas N. Kipf, Peter Bloem, Rianne van den Berg, Ivan Titov, Max Welling"
year: 2018
url: "https://arxiv.org/abs/1703.06103"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[图级读出、异构图与任务接口]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Schlichtkrull 等：R-GCN

> [!abstract] 来源定位
> 以 relation-specific transformations 扩展图卷积，并用于知识图谱实体分类与链接预测。

## 课程采用的断言

$$
h_i'=\sigma\!\left(W_0h_i+\sum_r\sum_{j\in\mathcal N_i^r}\frac1{c_{i,r}}W_rh_j\right).
$$

关系方向、逆边、自环、参数共享/基分解和 decoder 都是合同；链接预测划分必须防止目标边或其逆边泄漏到 encoder。

