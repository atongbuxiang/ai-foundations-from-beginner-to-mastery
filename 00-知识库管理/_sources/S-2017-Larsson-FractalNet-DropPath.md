---
type: source
status: active
area: [sources, neural-networks, droppath, fractalnet]
source_type: paper
title: "FractalNet: Ultra-Deep Neural Networks without Residuals"
author: "Gustav Larsson; Michael Maire; Gregory Shakhnarovich"
year: 2017
url: "https://openreview.net/forum?id=S1VaB4cex"
venue: "ICLR 2017"
accessed: 2026-08-29
source_tier: A
license: "OpenReview conference paper；本库仅保存独立摘要、必要结论与链接"
scope_role: terminology-history
temporal_role: foundational
related: ["[[Stochastic Depth、DropPath 与有效深度]]"]
created: 2026-08-24
updated: 2026-08-29
---

# Larsson、Maire、Shakhnarovich：FractalNet 与 Drop-Path

> [!abstract] 来源定位
> 论文在 fractal multi-path architecture 中使用 drop-path，随机删除整条路径以减少子路径共适应。它承担术语的历史来源；现代库常把 residual-branch stochastic depth 也称为 DropPath，两者结构语境不完全相同。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| FDP-C1 | path-level mask 与 element dropout 的随机对象不同 | 定义 | 明确广播轴/结构路径 | 精确 |
| FDP-C2 | FractalNet drop-path 与 residual stochastic depth 完全同义 | 术语外推 | 原架构与 rail 不同 | 错误 |
| FDP-C3 | 现代 `DropPath` 常实现 per-sample residual-branch gate | 实现惯例 | 需逐库核对 | 常见但非定义 |
| FDP-C4 | 删除路径必然减少实际 FLOP | 系统外推 | 需条件执行/短路 | 不成立 |
