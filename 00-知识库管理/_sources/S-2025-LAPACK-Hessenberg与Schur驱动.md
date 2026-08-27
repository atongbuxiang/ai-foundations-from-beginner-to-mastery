---
type: source
status: draft
area: [sources, math/numerical-linear-algebra, software/numerics]
source_type: documentation
title: "LAPACK 3.12.1 DGEHRD and DHSEQR"
author: LAPACK project
year: 2025
url: "https://www.netlib.org/lapack/explore-html/topics.html"
accessed: 2026-08-15
source_tier: A
license: "LAPACK BSD-style license；知识库保存接口摘要与链接"
scope_role: implementation-contract
temporal_role: active-implementation
aliases: [LAPACK-Hessenberg-Schur-Drivers]
related: ["[[Hessenberg 化与 QR 特征值算法]]", "[[Householder 与 Givens 变换]]", "[[Schur 分解]]"]
created: 2026-08-15
updated: 2026-08-15
---

# LAPACK：Hessenberg 约化与实 Schur 驱动

> [!abstract] 来源定位
> `DGEHRD` 与 `DHSEQR` 给出生产级稠密非对称特征值路线的核心接口：先用正交相似变换把一般实矩阵约化为上 Hessenberg 形，再对 Hessenberg 矩阵执行 QR 迭代，返回特征值并可选返回实 Schur 形式与 Schur 向量。

## 核心映射

| ID | 官方接口事实 | 纳入位置 |
|---|---|---|
| LAP-E1 | `DGEHRD` 计算 $Q^TAQ=H$，其中 $H$ 为上 Hessenberg | [[Hessenberg 化与 QR 特征值算法]]第四至六节 |
| LAP-E2 | `DGEHRD` 在上三角和第一条次对角线保存 $H$，在更下方与 `TAU` 紧凑保存反射器 | 第六节 |
| LAP-E3 | `DHSEQR` 从 $H$ 计算特征值，并可返回 $H=ZTZ^T$ | 第十五、十六节 |
| LAP-E4 | 实 Schur 形式含 $1\times1$ 与表示复共轭对的标准 $2\times2$ 块 | 第十四、十五节 |
| LAP-E5 | `COMPZ='V'` 可把 Hessenberg 阶段的 $Q$ 与 QR 阶段的 $Z$ 累积成原矩阵的 Schur 向量 | 第十五节 |
| LAP-E6 | `INFO>0` 表示仍有未收敛块，成功计算的特征值与最终 Hessenberg 状态仍有明确契约 | 第十六、二十一节 |

## 官方入口

- [`DGEHRD`](https://www.netlib.org/lapack/explore-html/d2/d28/group__gehrd_ga74cea8f05a014cca243674999f71c238.html)
- [`DHSEQR`](https://www.netlib.org/lapack/explore-html/d9/dc6/group__hseqr_ga62c3f96d2f67f96d6dc10334e118e451.html)

## 证据边界

- `DGEHRD + DHSEQR` 是内部计算阶段，不等同于完整用户驱动；实际常由 `xGEES/xGEEV` 负责平衡、向量与工作区管理；
- 实现包含多重移位、bulge chasing、deflation 等工程细节，不能用课堂上的显式单移位 QR 代码替代；
- 正交相似变换后向稳定，不保证非正规矩阵的单个特征值或特征向量前向稳定；
- `INFO>0` 不能被静默忽略，调用者必须报告未收敛区间。

## 生成节点

- [x] [[Hessenberg 化与 QR 特征值算法]]
- [x] [[实验 - Hessenberg 约化、移位与 QR deflation]]

