---
type: source
status: draft
area: [sources, math/numerical-analysis, math/numerical-linear-algebra]
source_type: journal-article
title: "FORTRAN Codes for Estimating the One-Norm of a Real or Complex Matrix, with Applications to Condition Estimation"
author: Nicholas J. Higham
year: 1988
url: "https://doi.org/10.1145/50063.214386"
accessed: 2026-08-15
source_tier: A
license: "ACM 论文；知识库仅保存独立摘要、推导映射与引用链接"
scope_role: canonical-condition-estimation
temporal_role: foundational
aliases: [Higham-1988-One-Norm-Estimator, Hager-Higham-Estimator]
related: ["[[误差传播、条件估计与停止准则]]", "[[条件数]]", "[[稳定求解线性方程组]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Higham：一范数估计与条件数

> [!abstract] 来源定位
> 该文给出只需要矩阵—向量乘的一范数估计程序，并通过反向通信把“如何乘 $A$ 或 $A^*$”交给调用者。对条件数而言，对 $A^{-1}$ 的一范数估计可由解 $Ax=v$ 和 $A^*x=v$ 实现，无需显式形成逆矩阵。

## 核心映射

| ID | 断言或工具 | 纳入位置 |
|---|---|---|
| CE-H1 | 用反复的 $Ax$ 与 $A^*x$ 估计 $\|A\|_1$ | [[误差传播、条件估计与停止准则]] |
| CE-H2 | $\kappa_1(A)=\|A\|_1\|A^{-1}\|_1$ 中的逆范数可用线性求解代替显式求逆 | 条件估计算法契约 |
| CE-H3 | 反向通信把估计器与稀疏、分布式或隐式算子解耦 | AI 隐式算子迁移 |
| CE-H4 | 估计值是廉价诊断，不是对所有矩阵的精确条件数证书 | 失效边界 |

## 使用边界

- 估计质量依赖迭代向量与终止规则，某些构造矩阵会使下界偏低；
- 估计 $\|A^{-1}\|_1$ 时，每次“乘逆”都是一次求解，其稳定性和残差也要纳入契约；
- 一范数条件估计不能自动替代分量型或结构化敏感度。

## 生成节点

- [x] [[误差传播、条件估计与停止准则]]
- [x] [[实验 - 条件估计、误差传播与可信停止]]

