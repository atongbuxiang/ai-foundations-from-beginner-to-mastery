---
type: source
status: draft
area: [sources, software/numerics, math/iterative-methods]
source_type: documentation
title: "PETSc 3.25 KSP, KSPCG and preconditioner documentation"
author: PETSc project
year: 2026
url: "https://petsc.org/release/manual/ksp/"
accessed: 2026-08-15
source_tier: A
license: "PETSc 开源官方文档；知识库保存接口摘要与链接"
scope_role: current-implementation-contract
temporal_role: active-implementation
aliases: [PETSc-3.25-KSP-PCG]
related: ["[[Krylov 子空间与预条件]]", "[[共轭梯度法]]", "[[GMRES、MINRES 与残差最小化]]", "[[稀疏矩阵计算与存储复杂度]]"]
created: 2026-08-15
updated: 2026-08-15
---

# PETSc：KSP、PCG、残差范数与预条件接口

> [!abstract] 来源定位
> PETSc 当前文档把数学假设落实为软件契约：`KSPCG` 要求矩阵与预条件器满足相应正定对称/Hermitian 条件；KSP 的默认停止量可能是真残差、预条件残差或自然范数；预条件器以 `PC` 对象独立配置。它承担当前 API 与报告边界。

## 官方入口

- [`KSPCG`](https://petsc.org/release/manualpages/KSP/KSPCG/)
- [`KSPGMRES`](https://petsc.org/release/manualpages/KSP/KSPGMRES/)
- [`KSPMINRES`](https://petsc.org/release/manualpages/KSP/KSPMINRES/)
- [KSP linear solvers manual](https://petsc.org/release/manual/ksp/)
- [Preconditioners (`PC`)](https://petsc.org/release/manualpages/PC/)
- [`PCJACOBI`](https://petsc.org/release/manualpages/PC/PCJACOBI/)

## 核心映射

| ID | 官方接口事实 | 纳入位置 |
|---|---|---|
| PET-K1 | `KSPCG` 要求矩阵和预条件器满足正定对称/Hermitian 结构 | [[共轭梯度法]]生产契约 |
| PET-K2 | PCG 的左、右、对称变换可导出相同核心算法，但实现中只需应用预条件算子 | [[Krylov 子空间与预条件]] |
| PET-K3 | 默认收敛范数随 KSP 类型和 preconditioning side 改变 | 停止准则章节 |
| PET-K4 | 真残差监控需显式重算 $b-Ax$，更适合验证而非无代价计时 | 有限精度章节 |
| PET-K5 | Jacobi、block、ICC、AMG、domain decomposition 等是可替换 PC 家族 | 预条件选择表 |
| PET-K6 | 单归约/流水 CG 变体用于降低并行同步，但改变舍入路径 | 通信与 AI/分布式接口 |
| PET-K7 | `KSPGMRES` 的 restart、正交化与 refinement 都是显式运行时选择 | [[GMRES、MINRES 与残差最小化]]重启/有限精度契约 |
| PET-K8 | `KSPMINRES` 要求矩阵/预条件器对称且预条件器正定，并采用左预条件 | 同章 MINRES 结构契约 |

## 证据边界

- 当前 API 事实可能随版本变化，正文数学结论不依赖 PETSc；
- “默认 residual norm”不是普适数学定义，报告必须记录 KSP norm type 和 preconditioning side；
- 库返回 `converged` 仍需结合容差、原因码、真残差抽查和任务误差解释；
- 本来源不承担经典 CG 收敛定理的唯一证明。

## 生成节点

- [x] [[Krylov 子空间与预条件]]软件契约
- [x] [[共轭梯度法]]停止、失败和通信章节
- [x] [[GMRES、MINRES 与残差最小化]]重启、MINRES 与残差范数契约
