---
type: source
status: draft
area: [sources, math/numerical-linear-algebra, software/numerics]
source_type: documentation
title: "LAPACK 3.12.1 least-squares drivers: DGELS, DGELSY, DGELSD"
author: LAPACK project
year: 2025
url: "https://www.netlib.org/lapack/explore-html/topics.html"
accessed: 2026-08-15
source_tier: A
license: "LAPACK BSD-style license；知识库保存接口摘要与链接"
scope_role: implementation-contract
temporal_role: active-implementation
aliases: [LAPACK-Least-Squares-Drivers]
related: ["[[稳定最小二乘与正规方程的风险]]", "[[Householder 与 Givens 变换]]", "[[Moore-Penrose 伪逆]]"]
created: 2026-08-15
updated: 2026-08-15
---

# LAPACK：满秩、秩揭示与 SVD 最小二乘驱动

> [!abstract] 来源定位
> LAPACK 3.12.1 的三个驱动体现了必须写进算法契约的分流：`DGELS` 用 QR/LQ 处理假定满秩的问题；`DGELSY` 用列主元 QR 和完全正交分解处理可能秩亏的问题；`DGELSD` 用 SVD 分治算法计算数值秩与最小范数解。

## 核心映射

| ID | 官方接口事实 | 纳入位置 |
|---|---|---|
| LAP-LS1 | `DGELS` 使用 QR/LQ，假定满秩，只对精确秩亏提供有限检测 | [[稳定最小二乘与正规方程的风险]]第十七节 |
| LAP-LS2 | `DGELSY` 先做 $AP=Q[R_{11}\ R_{12};0\ R_{22}]$，用 `RCOND` 和条件估计决定有效秩 | 第十三、十七节 |
| LAP-LS3 | `DGELSY` 再做右侧正交变换，形成完全正交分解并返回最小范数解 | 第十三节 |
| LAP-LS4 | `DGELSD` 通过双对角化、分治 SVD 和反向施加 Householder 变换求解 | 第十四、十七节 |
| LAP-LS5 | `DGELSD` 将小于 `RCOND·σ_max` 的奇异值视为零 | 第十四、十五节 |
| LAP-LS6 | 驱动会覆盖输入数组并有 workspace、缩放与多右端约定 | 第十七、二十一节 |

## 官方入口

- [`DGELS`](https://netlib.org/lapack/explore-html/d8/d83/group__gels_gaa65298f8ef218a625e40d0da3c95803c.html)
- [`DGELSY`](https://www.netlib.org/lapack/explore-html/dc/d8b/group__gelsy_ga6d1d46ead18df76e993cd4eda6dc1bbb.html)
- [`DGELSD`](https://netlib.org/lapack/explore-html/db/d6a/dgelsd_8f_source.html)

## 证据边界

- “有效秩”依赖 `RCOND`、缩放、数据噪声和算法估计，不是输入矩阵的无争议整数属性；
- `DGELSY` 的 QRCP 是实用秩揭示算法，但不是 strong RRQR 的全称保证；
- `DGELSD` 的奇异值阈值是一项建模/数值选择，改变它会改变返回解；
- 具体性能随版本、BLAS、线程、矩阵形状和硬件变化，正文不固化速度排行。

## 生成节点

- [x] [[稳定最小二乘与正规方程的风险]]第十三至十七节

