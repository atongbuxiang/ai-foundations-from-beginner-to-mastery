---
type: source
status: verified
area: [sources, optimization, norm-geometry]
source_type: paper
title: "Old Optimizer, New Norm: An Anthology"
author: [Jeremy Bernstein, Laker Newhouse]
year: 2024
url: "https://arxiv.org/abs/2409.20325"
accessed: 2026-08-26
source_tier: B
scope_role: theoretical-design
temporal_role: recent-foundation
related: ["[[最速下降、范数选择与对偶范数]]", "[[矩阵梯度、谱核范数对偶与 Matrix Sign]]", "[[Muon、Shampoo、SOAP 与隐式曲率关系]]"]
---

# S-2024 Bernstein–Newhouse - Old Optimizer, New Norm

## 核心贡献

- 以 normed steepest descent 重新解释关闭 EMA 后的 Adam、Shampoo、Prodigy 等方向；
- 强调 gradient 是 dual object，必须由选定 norm/duality map 转到 parameter space；
- 提出不同 layer role 应采用不同 norm，矩阵 shape 相同不等于优化几何相同。

## 采用边界

用于第一阶 norm geometry 与 optimizer-design 视角；不把该重解释升级为带 momentum、finite precision、weight decay 和 stochastic state 的完整轨迹等价。
