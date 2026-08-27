---
type: source
status: draft
area: [sources, math/numerical-analysis, math/numerical-linear-algebra]
source_type: journal-article
title: "Accurate Sum and Dot Product"
author: Takeshi Ogita, Siegfried M. Rump, Shin'ichi Oishi
year: 2005
url: "https://ogilab.w.waseda.jp/ogita/math/doc/2005_OgRuOi.pdf"
accessed: 2026-08-15
source_tier: A
license: "作者公开论文；知识库仅保存独立摘要、推导映射与链接"
scope_role: canonical-accurate-reductions
temporal_role: foundational
aliases: [Ogita-Rump-Oishi-2005, Accurate-Sum-Dot]
related: ["[[稳定求和、点积与矩阵乘法]]", "[[浮点数与舍入误差]]", "[[数值稳定性]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Ogita–Rump–Oishi：精确求和与点积

> [!abstract] 来源定位
> 该文把 `TwoSum`/`TwoProd` 类无误差变换组合成补偿求和和点积算法，使返回值达到类似更高精度计算后再舍入的质量，却主要使用工作精度的基本运算。

## 核心映射

| ID | 断言或工具 | 纳入位置 |
|---|---|---|
| SD-O1 | `TwoSum` 把一次浮点和分解为已舍入部分与精确尾项 | [[稳定求和、点积与矩阵乘法]] |
| SD-O2 | `TwoProd` 或 FMA 可暴露乘法舍入尾项 | 精确变换与 FMA |
| SD-O3 | 补偿算法对消去严重的求和/点积可显著改善精度 | 稳定归约 |
| SD-O4 | 多层补偿以额外运算换取近似多倍工作精度 | 精度—吞吐权衡 |

## 使用边界

- “更准”不等于数学结果可识别；当求和条件数极大时，输入量化误差仍可主导；
- 无误差变换依赖明确的浮点语义，编译器重排、扩展精度或 flush-to-zero 可改变契约；
- 并行归约还要同时考虑通信树、确定性与性能。

## 生成节点

- [x] [[稳定求和、点积与矩阵乘法]]
- [x] [[实验 - 稳定归约、点积消去与混合精度累加]]

