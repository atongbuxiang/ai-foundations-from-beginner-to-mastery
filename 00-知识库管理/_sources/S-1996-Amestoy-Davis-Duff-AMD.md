---
type: source
status: draft
area: [sources, math/sparse-linear-algebra, math/graph-ordering]
source_type: original-paper
title: "An Approximate Minimum Degree Ordering Algorithm"
author: "Patrick R. Amestoy, Timothy A. Davis, Iain S. Duff"
year: 1996
url: "https://people.engr.tamu.edu/davis/publications_files/An_Approximate_Minimum_Degree_Ordering_Algorithm.pdf"
accessed: 2026-08-15
source_tier: A
license: "作者公开论文；知识库仅保存独立摘要、机制映射与链接"
scope_role: fill-reducing-ordering
temporal_role: foundational-sparse-algorithm
aliases: [AMD-1996]
related: ["[[稀疏矩阵计算与存储复杂度]]", "[[Cholesky 分解]]", "[[稳定求解线性方程组]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Amestoy–Davis–Duff：近似最小度排序

> [!abstract] 来源定位
> AMD 用廉价度数上界近似最小度消元排序，在稀疏对称分解前减少 fill-in。该来源承担“重排不改变数学问题，却能改变分解存储与工作量”的算法依据。

## 核心映射

| ID | 原始贡献 | 纳入位置 |
|---|---|---|
| AMD-1 | 消元图中的邻居团化产生 fill-in | 图消元解释 |
| AMD-2 | 最小度思想优先消去当前低度顶点 | 手算与实验 |
| AMD-3 | 近似度数避免精确最小度的高维护成本 | 排序成本边界 |
| AMD-4 | 排序质量以预测 $\operatorname{nnz}(L)$ 和 flop 评估 | 生产验收 |
| AMD-5 | 排序可在同一稀疏结构的多次数值分解间复用 | symbolic/numeric 分层 |

## 证据边界

- AMD 是启发式近似，不保证全局最小 fill；
- 数值主元选取可能修改符号分析预测的结构；
- 规则网格上 nested dissection 可能更适合并行和渐近复杂度。

## 生成节点

- [x] [[稀疏矩阵计算与存储复杂度]]

