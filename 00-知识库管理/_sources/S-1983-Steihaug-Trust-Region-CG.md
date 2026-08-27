---
type: source
status: verified
area: [sources, optimization, trust-region, krylov]
source_type: paper
title: "The Conjugate Gradient Method and Trust Regions in Large Scale Optimization"
author: [Trond Steihaug]
year: 1983
url: "https://doi.org/10.1137/0720042"
venue: "SIAM Journal on Numerical Analysis 20(3):626–637"
accessed: 2026-08-26
source_tier: A
scope_role: primary
temporal_role: foundational
related: ["[[Newton、Damping、Trust Region 与 Levenberg–Marquardt]]", "[[Hessian-vector Product、共轭梯度与隐式二阶步]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Steihaug：Trust-Region Conjugate Gradient

> [!abstract] 来源定位
> 大规模 trust-region 子问题用预条件 CG 近似求解的经典来源。课程重点采用“不必解完整线性系统”的思想，以及遇到 negative curvature 或越过球边界时沿当前方向截到边界的停止合同。

## 课程采用与边界

- 内点 residual 收敛、negative-curvature exit、boundary intersection 是三种不同出口；
- CG 的 SPD 教科书性质不能在不定 Hessian 上原样套用；
- 子问题近似解仍需外层 actual/predicted reduction 接受门；
- 原论文保证属于规定的 trust-region 框架，不是任意固定步长 Hessian-free training 的证明。
