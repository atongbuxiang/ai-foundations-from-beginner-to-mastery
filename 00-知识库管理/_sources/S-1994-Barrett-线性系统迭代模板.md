---
type: source
status: draft
area: [sources, math/numerical-linear-algebra, software/iterative-solvers]
source_type: technical-book
title: "Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods"
author: "Richard Barrett, Michael Berry, Tony F. Chan, James Demmel, June Donato, Jack Dongarra, Victor Eijkhout, Roldan Pozo, Charles Romine, Henk van der Vorst"
year: 1994
url: "https://www.netlib.org/templates/templates.html"
accessed: 2026-08-15
source_tier: A
license: "Netlib 在线技术书；知识库仅保存独立摘要、算法映射与链接"
scope_role: implementation-and-selection-contract
temporal_role: foundational-software-methodology
aliases: [Netlib-Linear-System-Templates]
related: ["[[定常迭代法与谱半径]]", "[[Krylov 子空间与预条件]]", "[[共轭梯度法]]", "[[GMRES、MINRES 与残差最小化]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Netlib Templates：线性系统迭代方法的选择与实现契约

> [!abstract] 来源定位
> Netlib Templates 把 Jacobi、Gauss–Seidel、SOR、CG、MINRES、GMRES 等放在同一决策树中，并同时讨论停止准则、稀疏存储、预条件、并行内积和通信。它承担算法选择与生产实现边界，不取代正文中的初学者证明。

## 核心映射

| ID | 来源事实 | 纳入位置 |
|---|---|---|
| NTL-1 | 定常方法写成固定 $B,c$ 的 $x_k=Bx_{k-1}+c$ | [[定常迭代法与谱半径]] |
| NTL-2 | Jacobi 易并行；GS/SOR 依赖更新顺序；SSOR 常作为预条件器 | 分裂、排序与并行章节 |
| NTL-3 | CG 适用于 SPD，速度受预条件谱和条件数控制 | [[共轭梯度法]] |
| NTL-4 | PCG 要求 SPD 预条件器并保持相应内积结构 | [[Krylov 子空间与预条件]] |
| NTL-5 | CG 每步一个 matvec、少量向量更新和全局内积；同步可能主导 | 成本与通信章节 |
| NTL-6 | 停止时必须说明真残差、预条件残差、相对基准与浮点停滞 | 三章报告模板 |

## 证据边界

- Templates 给出算法骨架和经典选择规则，不固定当前某个 GPU/分布式 API；
- “GS 通常比 Jacobi 快”不是任意矩阵的无条件逐步定理；
- 条件数界是最坏情形，谱聚簇可带来明显更快的实际 CG；
- 预条件器必须按 setup、apply、内存、通信与失败状态整体比较。

## 生成节点

- [x] 三章算法选择表、成本表与停止准则
- [ ] [[GMRES、MINRES 与残差最小化]]后续扩展
