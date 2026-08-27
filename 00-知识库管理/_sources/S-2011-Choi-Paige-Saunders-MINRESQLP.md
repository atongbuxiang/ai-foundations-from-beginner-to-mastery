---
type: source
status: draft
area: [sources, math/numerical-linear-algebra, math/krylov-methods]
source_type: original-algorithm-paper
title: "MINRES-QLP: A Krylov Subspace Method for Indefinite or Singular Symmetric Systems"
author: "Sou-Cheng T. Choi, Christopher C. Paige, Michael A. Saunders"
year: 2011
url: "https://web.stanford.edu/group/SOL/reports/SOL-2010-3.pdf"
accessed: 2026-08-15
source_tier: A
license: "Stanford SOL 公开技术报告及论文版本；知识库保存独立摘要与链接"
scope_role: symmetric-indefinite-and-singular-boundary
temporal_role: established-algorithm
aliases: [MINRES-QLP-2011]
related: ["[[GMRES、MINRES 与残差最小化]]", "[[Lanczos 方法]]", "[[共轭梯度法]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Choi–Paige–Saunders：MINRES-QLP 与对称奇异边界

> [!abstract] 来源定位
> MINRES 以 Lanczos 三对角化在对称/Hermitian系统上最小化二范数残差；MINRES-QLP 进一步面向奇异、病态或不相容系统，改善解范数和最小长度解的处理。该来源承担 CG 之外的对称不定/奇异方法边界。

## 核心映射

| ID | 来源结论 | 纳入位置 |
|---|---|---|
| MQLP-1 | $A$ 可对称不定；预条件器必须对称正定 | 方法选择契约 |
| MQLP-2 | Lanczos 三项递推把问题压缩为小三对角最小二乘 | MINRES 推导 |
| MQLP-3 | 非奇异对称系统可用 MINRES；奇异/不相容系统需更谨慎 | 奇异系统边界 |
| MQLP-4 | QLP 分解改善病态小问题与最小长度解计算 | MINRES-QLP 扩展 |
| MQLP-5 | 预条件可能改变“最小长度”所对应的范数 | 报告与解释边界 |

## 证据边界

- MINRES 不适用于一般非对称矩阵；
- 随机对称性抽查不能证明算子全局对称；
- 奇异问题中的最小残差、最小长度和预条件坐标下最小长度必须分开陈述。

## 生成节点

- [x] [[GMRES、MINRES 与残差最小化]]

