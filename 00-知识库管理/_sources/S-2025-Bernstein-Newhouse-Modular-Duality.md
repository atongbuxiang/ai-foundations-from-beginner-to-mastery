---
type: source
status: verified
area: [sources, optimization, modular-duality, muon]
source_type: paper
title: "Modular Duality in Deep Learning"
author: [Jeremy Bernstein, Laker Newhouse]
year: 2025
url: "https://proceedings.mlr.press/v267/bernstein25a.html"
venue: "ICML 2025, PMLR 267:3920–3930"
accessed: 2026-08-26
source_tier: A
scope_role: primary-theory
temporal_role: current-theory
related: ["[[最速下降、范数选择与对偶范数]]", "[[矩阵梯度、谱核范数对偶与 Matrix Sign]]", "[[Muon 形状缩放、Update RMS 与版本差异]]"]
---

# S-2025 Bernstein–Newhouse - Modular Duality

## 核心贡献

- 将网络拆成 typed modules，为每种输入/输出和 weight space 指定 norm；
- 从 duality map 推导 layer-wise optimizer，并给出跨 module 组合规则；
- 为 Muon 的 linear-layer spectral direction 和 shape-aware scale 提供正式理论背景。

## 采用边界

承担 norm/duality 与模块化尺度的正式证据；不承担任何特定 benchmark 的普遍优势，也不等同于 Hessian/Fisher preconditioning。
