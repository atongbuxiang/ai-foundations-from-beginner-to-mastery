---
type: source
status: verified
area: [sources, numerical-linear-algebra, polar-decomposition]
source_type: paper
title: "Computing the Polar Decomposition—with Applications"
author: [Nicholas J. Higham]
year: 1986
url: "https://doi.org/10.1137/0907079"
venue: "SIAM Journal on Scientific and Statistical Computing 7(4):1160–1174"
accessed: 2026-08-26
source_tier: A
scope_role: numerical-foundation
temporal_role: foundational
related: ["[[矩阵梯度、谱核范数对偶与 Matrix Sign]]", "[[Newton–Schulz Matrix Sign 的收敛与有限精度]]"]
---

# S-1986 Higham - Polar Decomposition

## 核心贡献

- 给出 full-rank polar decomposition 的 Newton 计算与加速分析；
- 建立 unitary/semi-orthogonal polar factor 的 best-approximation 与 perturbation 视角；
- 为 SVD $UV^T$、matrix sign/polar 和迭代残差提供经典数值基础。

## 采用边界

精确 polar factor 与 Muon 的有限步 BF16 多项式必须分开；秩亏时 polar factor 的唯一性、矩形方向和 pseudoinverse convention 需额外声明。
