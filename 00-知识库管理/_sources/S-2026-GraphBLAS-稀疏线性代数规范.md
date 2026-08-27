---
type: source
status: draft
area: [sources, math/sparse-linear-algebra, software/graph-computing]
source_type: standard
title: "GraphBLAS C API Specification 2.1.0"
author: GraphBLAS Forum
year: 2026
url: "https://graphblas.org/docs/GraphBLAS_API_C_v2.1.0.pdf"
accessed: 2026-08-15
source_tier: A
license: "GraphBLAS Forum 公开标准；知识库仅保存接口与数学语义摘要"
scope_role: sparse-operator-standard
temporal_role: active-standard
aliases: [GraphBLAS-C-2.1]
related: ["[[稀疏矩阵计算与存储复杂度]]", "[[图与图拉普拉斯]]"]
created: 2026-08-15
updated: 2026-08-15
---

# GraphBLAS：稀疏容器、半环与图计算规范

> [!abstract] 来源定位
> GraphBLAS 把图算法表达为稀疏矩阵/向量上的广义线性代数：存储位置、值域、掩码和半环共同决定运算。它承担“空位置不必等于普通算术零”和图—稀疏算子接口，不替代 CSR/CSC 的硬件实现分析。

## 核心映射

| ID | 标准语义 | 纳入位置 |
|---|---|---|
| GB-1 | 稀疏容器由形状、存储位置和值组成 | 稀疏对象定义 |
| GB-2 | 空位置与显式存储值必须区分 | 显式零和结构零 |
| GB-3 | 矩阵乘、逐元素运算、归约可建立在不同半环上 | 图算法章节 |
| GB-4 | 掩码控制输出位置，避免无意义稠密中间量 | 稀疏闭包与实现 |
| GB-5 | 邻接矩阵上的稀疏乘法可表达 BFS 等图过程 | AI/图学习接口 |

## 证据边界

- API 数学语义不指定某个后端必须使用 CSR、CSC 或特定 GPU kernel；
- 普通数值线性代数的零与 GraphBLAS 某个半环的加法单位元不能不加说明地混同；
- 稀疏输出规模可能依赖数据模式，不能只由输入 nnz 推出。

## 生成节点

- [x] [[稀疏矩阵计算与存储复杂度]]

