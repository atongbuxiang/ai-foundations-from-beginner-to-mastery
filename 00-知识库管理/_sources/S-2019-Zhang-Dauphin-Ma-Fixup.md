---
type: source
status: active
area: [sources, neural-networks, initialization, residual-networks]
source_type: paper
title: "Fixup Initialization: Residual Learning Without Normalization"
author: [Hongyi Zhang, Yann N. Dauphin, Tengyu Ma]
year: 2019
url: "https://openreview.net/forum?id=H1gsz30cKX"
accessed: 2026-08-23
source_tier: A
venue: "ICLR 2019"
related: ["[[LSUV、Fixup 与现代初始化诊断]]", "[[偏置、输出层与零初始化的对称性边界]]", "[[ReZero、Fixup、DeepNorm 与深网缩放]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Zhang、Dauphin、Ma 2019：Fixup Initialization

> [!abstract] 来源定位
> 原论文为无 normalization 的 residual network 设计 depth-aware 初始化：分支内非末层按 $L^{-1/(2m-2)}$ 缩放，分支末层与分类层置零，并加入少量 scalar multiplier/bias。本库用它说明“受结构保护的零初始化”和“全网全零”不同；性能结论仍绑定论文架构、优化与实验设置。
