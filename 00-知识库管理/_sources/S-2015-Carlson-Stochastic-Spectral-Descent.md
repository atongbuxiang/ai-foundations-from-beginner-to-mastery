---
type: source
status: verified
area: [sources, optimization, spectral-descent]
source_type: paper
title: "Stochastic Spectral Descent for Restricted Boltzmann Machines"
author: [David Carlson, Volkan Cevher, Lawrence Carin]
year: 2015
url: "https://proceedings.mlr.press/v38/carlson15.html"
venue: "AISTATS 2015, PMLR 38:111–119"
accessed: 2026-08-26
source_tier: A
scope_role: historical-primary
temporal_role: precursor
related: ["[[矩阵梯度、谱核范数对偶与 Matrix Sign]]", "[[Muon 的扩展证据、系统成本与迁移边界]]"]
---

# S-2015 Carlson–Cevher–Carin - Stochastic Spectral Descent

## 核心贡献

- 在 RBM 训练中按 Schatten-$\infty$/spectral normed space 构造 stochastic descent；
- 证明矩阵变量应按矩阵 norm 而非逐元素向量 norm 处理的早期先例；
- 给出特定 RBM 上的原始经验结果。

## 采用边界

它是 Muon/spectral descent 的历史前驱，不是现代 Transformer Muon 的完整实现合同；momentum、NS approximation、shape scaling、parameter groups 和分布式证据均需后续来源补齐。
