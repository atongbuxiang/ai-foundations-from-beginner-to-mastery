---
type: source
status: draft
area: [sources, architecture/gnn, graph-convolution]
source_type: paper
title: "Semi-Supervised Classification with Graph Convolutional Networks"
author: "Thomas N. Kipf, Max Welling"
year: 2017
url: "https://openreview.net/forum?id=SJU4ayYgl"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[谱图卷积、空间图卷积与归一化邻接]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Kipf–Welling：GCN

> [!abstract] 来源定位
> 从局部谱滤波近似导出一阶传播，并以加自环后的对称归一化邻接形成经典 GCN layer。

## 课程采用的断言

$$
H^{(l+1)}=\sigma\!\left(\tilde D^{-1/2}\tilde A\tilde D^{-1/2}H^{(l)}W^{(l)}\right),
\quad \tilde A=A+I.
$$

- 谱动机与最终的空间邻域平均是两种互补解释；
- 自环、归一化、无向化与 split 是模型合同的一部分；
- 原论文的半监督结果不自动外推异配图、动态图或任意数据划分。

