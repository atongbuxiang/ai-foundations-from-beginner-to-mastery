---
type: source
status: draft
area: [sources, math/numerical-linear-algebra, software/numerics]
source_type: documentation
title: "LAPACK 3.12.1 SVD drivers and bidiagonal reduction"
author: LAPACK project
year: 2025
url: "https://www.netlib.org/lapack/explore-html/topics.html"
accessed: 2026-08-15
source_tier: A
license: "LAPACK BSD-style license；知识库保存接口摘要与链接"
scope_role: implementation-contract
temporal_role: active-implementation
aliases: [LAPACK-SVD-Drivers]
related: ["[[SVD 算法与谱范数估计]]", "[[稳定最小二乘与正规方程的风险]]", "[[Householder 与 Givens 变换]]"]
created: 2026-08-15
updated: 2026-08-15
---

# LAPACK：双对角约化、QR SVD 与分治 SVD

> [!abstract] 来源定位
> LAPACK 3.12.1 把稠密 SVD 的结构与用户契约具体化：`DGEBRD` 做双对角约化；`DGESVD` 使用双对角 QR 路线；`DGESDD` 在需要奇异向量时采用分治算法。输出形状、覆盖语义、工作区和 `INFO` 都是算法选择的一部分。

## 核心映射

| ID | 官方接口事实 | 纳入位置 |
|---|---|---|
| LAP-S1 | `DGEBRD` 将 $m\times n$ 一般矩阵约化为上/下双对角形并紧凑保存左右反射器 | [[SVD 算法与谱范数估计]]第七节 |
| LAP-S2 | `DGESVD` 是 QR-iteration SVD 驱动 | 第十节 |
| LAP-S3 | `DGESDD` 在请求奇异向量时使用 divide-and-conquer | 第十节 |
| LAP-S4 | `JOBU/JOBVT/JOBZ` 控制全量、经济型、覆盖或不计算向量 | 第十二、十六节 |
| LAP-S5 | 返回的是 $V^T$，输入通常被覆盖；workspace query 应用于生产调用 | 软件契约章节 |
| LAP-S6 | `INFO>0` 表示双对角阶段没有完全收敛，不能静默标记成功 | 失败与报告章节 |

## 官方入口

- [`DGEBRD`](https://www.netlib.org/lapack/explore-html/dc/d1c/group__gebrd_ga1314f3a906c316785fe32996698901a8.html)
- [`DGESVD`](https://netlib.org/lapack/explore-html/d1/d7f/group__gesvd_gac6bd5d4e645049e49bb70691180abf07.html)
- [`DGESDD`](https://www.netlib.org/lapack/explore-html/df/d22/group__gesdd_ga8941e5ff50de36580dae8940015e9cb0.html)
- [`DBDSQR`](https://netlib.org/lapack/explore-html/d6/d51/group__bdsqr_gade20fbf9c91aa7de0c3d565b39588dc5.html)

## 证据边界

- `DGESDD` 常为大量奇异向量提供高性能，但实际速度和内存取决于形状、后端、线程与工作区；
- “只要奇异值”与“要经济型/完整左右向量”的成本和存储不同；
- 驱动文档不替用户决定数值秩或截断阈值；
- 大型稀疏矩阵只求少量奇异值时，应转向 Golub–Kahan–Lanczos、随机化或专门迭代库。

## 生成节点

- [x] [[SVD 算法与谱范数估计]]软件路线与报告模板

