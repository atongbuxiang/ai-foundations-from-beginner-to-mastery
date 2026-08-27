---
type: source
status: draft
area: [sources, math/numerical-linear-algebra, math/iterative-methods]
source_type: course-notes
title: "Math 221 Lectures 12–15: Splitting, Krylov methods, CG and preconditioning"
author: James Demmel
year: 2023
url: "https://people.eecs.berkeley.edu/~demmel/ma221_Fall23/Lectures/"
accessed: 2026-08-15
source_tier: A
license: "作者公开课程讲义；知识库仅保存独立摘要、推导映射与链接"
scope_role: canonical-worked-analysis
temporal_role: foundational-teaching
aliases: [Demmel-2023-Splitting-Krylov-CG-PC]
related: ["[[定常迭代法与谱半径]]", "[[Krylov 子空间与预条件]]", "[[共轭梯度法]]", "[[Lanczos 方法]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Demmel：从矩阵分裂到 Krylov、CG 与预条件

> [!abstract] 来源定位
> Berkeley Math 221 第 12–15 讲构成连续算法链：分裂 $A=M-K$ 产生定常迭代；谱半径给出全初值收敛充要条件；Krylov 方法只需要黑盒 matvec；SPD 情形的 Galerkin 条件等价于能量范数最小化并导出 CG；SPD 预条件通过对称变换隐式保留 CG 结构。

## 官方入口

- [Lecture 12：Splitting Methods](https://people.eecs.berkeley.edu/~demmel/ma221_Fall23/Lectures/Lecture_12.pdf)
- [Lecture 13：Krylov subspace methods](https://people.eecs.berkeley.edu/~demmel/ma221_Fall23/Lectures/Lecture_13.pdf)
- [Lecture 14：GMRES and CG](https://people.eecs.berkeley.edu/~demmel/ma221_Fall23/Lectures/Lecture_14.pdf)
- [Lecture 15：Preconditioning](https://people.eecs.berkeley.edu/~demmel/ma221_Fall23/Lectures/Lecture_15.pdf)

## 核心映射

| ID | 断言或工具 | 纳入位置 |
|---|---|---|
| DEM-IT1 | $A=M-K$ 给出 $x_{k+1}=M^{-1}Kx_k+M^{-1}b$；对所有初值收敛当且仅当 $\rho(M^{-1}K)<1$ | [[定常迭代法与谱半径]]主定理 |
| DEM-IT2 | Jacobi、GS、SOR 对应不同 $M$；更新顺序和 $\omega$ 同时影响谱与并行性 | 分裂与实现章节 |
| DEM-K1 | Krylov 方法只需 $v\mapsto Av$，在 $\mathcal K_k(A,r_0)$ 中按不同“最佳”标准选解 | [[Krylov 子空间与预条件]] |
| DEM-CG1 | SPD 下 Galerkin 残差正交等价于 $A$-范数误差最小化 | [[共轭梯度法]]最优性证明 |
| DEM-CG2 | Lanczos 投影三对角的 $LDL^T$ 分解导出三向量 CG 递推 | CG 与 Lanczos 章节 |
| DEM-PC1 | SPD $M$ 对应 $M^{-1/2}AM^{-1/2}$；实现 PCG 无需形成平方根 | 预条件结构章节 |
| DEM-PC2 | Jacobi、block Jacobi、IC、multigrid 与 domain decomposition 是不同成本—质量层次 | 预条件选择表 |

## 证据边界

- $\rho(B)<1$ 是渐近充要条件，不保证给定欧氏范数中的单调误差下降；
- Jacobi/GS/SOR 的 Poisson 公式依赖离散、边界和排序，不能直接移植到任意稀疏矩阵；
- CG 的最优性、短递推和经典条件数界要求实 SPD 或复 Hermitian positive definite；
- “预条件改善条件数”不是唯一质量指标，谱聚簇、应用成本、并行性与稳健性同样重要。

## 生成节点

- [x] [[定常迭代法与谱半径]]
- [x] [[Krylov 子空间与预条件]]
- [x] [[共轭梯度法]]
