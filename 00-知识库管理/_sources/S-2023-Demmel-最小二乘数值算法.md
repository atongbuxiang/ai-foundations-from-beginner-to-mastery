---
type: source
status: draft
area: [sources, math/numerical-analysis, math/numerical-linear-algebra]
source_type: course-notes
title: "Notes for Ma221 Lecture 7: Least Squares, Householder and Givens QR"
author: James Demmel
year: 2023
url: "https://people.eecs.berkeley.edu/~demmel/ma221_Fall23/Lectures/Lecture_07.pdf"
accessed: 2026-08-15
source_tier: A
license: "作者公开课程讲义；知识库仅保存独立摘要、推导映射与链接"
scope_role: canonical-worked-analysis
temporal_role: foundational-teaching
aliases: [Demmel-2023-Stable-Least-Squares]
related: ["[[稳定最小二乘与正规方程的风险]]", "[[Householder 与 Givens 变换]]", "[[条件数]]", "[[奇异值分解]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Demmel：正规方程、QR 与 SVD 的最小二乘路线

> [!abstract] 来源定位
> Berkeley Math 221 第七讲把最小二乘的正规方程、Householder QR、SVD 与稀疏增广系统放在同一算法选择框架中。它承担本章的经典推导、主要成本与稳定性排序；秩亏接口和软件容差由 LAPACK 来源补足。

## 核心映射

| ID | 断言或工具 | 纳入位置 |
|---|---|---|
| LS-D1 | 满列秩最小二乘解满足 $A^T(Ax-b)=0$，可由勾股分解证明最优性 | [[稳定最小二乘与正规方程的风险]]第三、四节 |
| LS-D2 | 正规方程需要形成 $A^TA$，并用 Cholesky 求解 | 第六、七节 |
| LS-D3 | Householder QR 通过正交不变性把问题化为 $Rx=Q^Tb$ | 第八节 |
| LS-D4 | SVD 给出病态、秩亏和欠定问题的最完整诊断 | 第十二至十五节 |
| LS-D5 | Cholesky QR/正规方程计算快，但继承 Gram 矩阵的条件数平方问题 | 第七、十七节 |
| LS-D6 | 算法评价同时涉及 flops、数据移动、稀疏性和需要的诊断 | 第十六、十七节 |

## 证据边界

- 满列秩正规方程的数学正确性不等于浮点实现可靠；正文将二者分开陈述；
- “SVD 最完整”指它显式暴露奇异值、数值秩与最小范数解，不表示任何 SVD 驱动在所有硬件上都最快；
- 讲义中的量级判断依赖 $m\ge n$ 的稠密问题；稀疏、多右端和流式问题需要独立分析；
- 前向误差还取决于问题条件性、残差方向和 $b$ 的扰动模型，不应只写成单一 $\kappa(A)$ 因子。

## 生成节点

- [x] [[稳定最小二乘与正规方程的风险]]
- [x] [[实验 - 正规方程、QR 与截断 SVD 的稳定性]]

