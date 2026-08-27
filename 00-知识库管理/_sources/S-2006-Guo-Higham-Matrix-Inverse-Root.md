---
type: source
status: verified
area: [sources, numerical-linear-algebra, matrix-functions]
source_type: paper
title: "A Schur–Newton Method for the Matrix pth Root and its Inverse"
author: [Chun-Hua Guo, Nicholas J. Higham]
year: 2006
url: "https://doi.org/10.1137/050643374"
venue: "SIAM Journal on Matrix Analysis and Applications 28(3):788–804"
accessed: 2026-08-26
source_tier: A
scope_role: numerical-foundation
temporal_role: reference
related: ["[[Shampoo、逆矩阵根与 Kronecker 预条件]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Guo–Higham：Matrix pth Root 与 Inverse Root

> [!abstract] 来源定位
> 矩阵 $p$ 次根/逆根的 Schur–Newton 数值来源。它说明“只用矩阵乘法”的 basic Newton iteration 可能数值不稳定，coupled iteration、初始缩放、谱区域和 residual 证书不可省略。

## 课程采用

- SPD 情形可用 eigendecomposition 定义 principal $A^{-1/p}$，但近零特征值需 damping；
- 迭代法必须报告 scaling、convergence region、iteration count、working precision 和 backward/commutation residual；
- 训练优化器中的低频 root refresh、block size 与 accelerator kernel 属于额外系统层，不由矩阵函数定理自动覆盖。
