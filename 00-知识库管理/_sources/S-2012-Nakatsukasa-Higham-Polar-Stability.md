---
type: source
status: verified
area: [sources, numerical-linear-algebra, polar-decomposition, stability]
source_type: paper
title: "Backward Stability of Iterations for Computing the Polar Decomposition"
author: [Yuji Nakatsukasa, Nicholas J. Higham]
year: 2012
url: "https://doi.org/10.1137/110857544"
venue: "SIAM Journal on Matrix Analysis and Applications 33(2):460–479"
accessed: 2026-08-26
source_tier: A
scope_role: numerical-stability
temporal_role: reference
related: ["[[Newton–Schulz Matrix Sign 的收敛与有限精度]]"]
---

# S-2012 Nakatsukasa–Higham - Polar Iteration Stability

## 核心贡献

- 给出 polar iterations 的 backward-stability 分析框架；
- 证明 scaled Newton/QDWH 等方法的相应稳定性质，并指出 Newton–Schulz 仅条件稳定；
- 强调 singular-value map 不能把小奇异值相对最大值压得过低。

## 采用边界

用于反驳“全 GEMM、BF16 可跑 ⇒ 自动稳定”。Muon 的特定五次多项式还需按其系数、归一化、步数和 dtype 做独立 residual audit。
