---
type: source
status: draft
area: [sources, math/numerical-linear-algebra, math/krylov-methods]
source_type: original-paper
title: "GMRES: A Generalized Minimal Residual Algorithm for Solving Nonsymmetric Linear Systems"
author: "Youcef Saad and Martin H. Schultz"
year: 1986
url: "https://doi.org/10.1137/0907058"
accessed: 2026-08-15
source_tier: A
license: "SIAM 原始论文；知识库仅保存独立摘要、推导映射与链接"
scope_role: original-algorithm
temporal_role: foundational
aliases: [Saad-Schultz-1986-GMRES]
related: ["[[GMRES、MINRES 与残差最小化]]", "[[Arnoldi 方法]]", "[[Krylov 子空间与预条件]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Saad–Schultz：GMRES 原始算法

> [!abstract] 来源定位
> 原论文从 Arnoldi 正交基导出一般非对称线性系统的逐阶二范数残差最小化，并明确给出完整 GMRES 的存储增长与重启方案。正文用现代投影、多项式和有限精度语言重建算法。

## 核心映射

| ID | 原始贡献 | 纳入位置 |
|---|---|---|
| SS86-1 | 在 $x_0+\mathcal K_k(A,r_0)$ 中最小化 $\|b-Ax\|_2$ | [[GMRES、MINRES 与残差最小化]]主定义 |
| SS86-2 | Arnoldi 关系把大问题化为 $\min_y\|\beta e_1-\bar H_ky\|_2$ | 小最小二乘推导 |
| SS86-3 | Givens 旋转可逐列更新 QR 与残差估计 | 实现章节 |
| SS86-4 | 完整方法的基存储和正交化成本随 $k$ 增长 | 成本章节 |
| SS86-5 | 重启控制资源，但会丢失先前多项式信息 | 重启边界与实验 |

## 证据边界

- GMRES 的残差最小性是当前 Krylov 仿射空间内的结论，不保证短重启仍复制完整 GMRES；
- 精确算术残差估计依赖 Arnoldi/QR 关系，有限精度最终仍需真残差；
- 特征值分布不足以完整预测非正规矩阵上的 GMRES 行为。

## 生成节点

- [x] [[GMRES、MINRES 与残差最小化]]

