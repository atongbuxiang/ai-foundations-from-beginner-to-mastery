---
type: source
status: draft
area: [sources, math/numerical-analysis, math/numerical-linear-algebra]
source_type: journal-article
title: "Accelerating the Solution of Linear Systems by Iterative Refinement in Three Precisions"
author: Erin Carson, Nicholas J. Higham
year: 2018
url: "https://eprints.maths.manchester.ac.uk/2629/"
accessed: 2026-08-15
source_tier: A
license: "机构仓储公开论文；知识库仅保存独立摘要、推导映射与链接"
scope_role: canonical-three-precision-refinement
temporal_role: foundational-modern
aliases: [Carson-Higham-2018, Three-Precision-IR, GMRES-IR]
related: ["[[迭代改进、混合精度与残差校正]]", "[[稳定求解线性方程组]]", "[[GMRES、MINRES 与残差最小化]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Carson–Higham：三精度迭代改进

> [!abstract] 来源定位
> 该文系统区分低精度分解/校正求解、工作精度解向量更新和更高精度残差，并分析经典迭代改进与 GMRES 预条件校正可用的条件数区间。

## 核心映射

| ID | 断言或工具 | 纳入位置 |
|---|---|---|
| IR-C1 | 三个单位舍入误差 $u_f,u,u_r$ 必须分开声明 | [[迭代改进、混合精度与残差校正]] |
| IR-C2 | 经典 IR 的收缩受低精度校正求解质量限制 | 误差递推与收敛边界 |
| IR-C3 | 高精度计算 $r=b-Ax$ 避免可信信号被工作精度吞没 | 误差地板 |
| IR-C4 | GMRES-IR 用低精度分解作预条件器，可扩展可收敛区间 | 内外迭代 |
| IR-C5 | FP16/FP32/FP64 组合的可用阈值是充分条件与实验结果，不是任意矩阵的绝对保证 | 结论边界 |

## 使用边界

- $\kappa(A)u_f<1$ 是有用直觉，但实际界受增长因子、缩放、分量条件性与求解器实现影响；
- GMRES-IR 的扩展以内层 Krylov 能收敛为前提，不是无条件修复；
- 低精度 LU 若已溢出、出现零主元或成为坏预条件器，需回退精度或换算法。

## 生成节点

- [x] [[迭代改进、混合精度与残差校正]]
- [x] [[实验 - 三精度迭代改进与 GMRES-IR 边界]]

