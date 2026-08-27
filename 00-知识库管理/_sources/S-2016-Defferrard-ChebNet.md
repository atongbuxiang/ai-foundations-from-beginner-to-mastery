---
type: source
status: draft
area: [sources, architecture/gnn, spectral-graph]
source_type: paper
title: "Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering"
author: "Michaël Defferrard, Xavier Bresson, Pierre Vandergheynst"
year: 2016
url: "https://proceedings.neurips.cc/paper/2016/hash/04df4d434d481c5bb723be1b6df1ee65-Abstract.html"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[谱图卷积、空间图卷积与归一化邻接]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Defferrard 等：ChebNet

> [!abstract] 来源定位
> 以图 Laplacian 的 Chebyshev 多项式构造严格局部化的谱滤波器，连接“频域函数”与“有限跳邻域计算”。

## 课程采用的断言

| 断言 | 边界 |
|---|---|
| $K$ 阶 Laplacian 多项式只传播到 $K$ 跳 | 依赖所选 Laplacian 与稀疏图乘法合同 |
| Chebyshev 递推避免显式特征分解 | 不表示所有谱滤波器都天然跨图可迁移 |
| 复杂度可按 $O(K|E|)$ 组织 | 常数、特征通道和 batch 仍须计入 |

