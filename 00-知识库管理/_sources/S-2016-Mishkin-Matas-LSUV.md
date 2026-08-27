---
type: source
status: active
area: [sources, neural-networks, initialization, data-dependent-initialization]
source_type: paper
title: "All You Need Is a Good Init"
author: [Dmytro Mishkin, Jiri Matas]
year: 2016
url: "https://arxiv.org/abs/1511.06422"
accessed: 2026-08-23
source_tier: A
venue: "ICLR 2016"
related: ["[[LSUV、Fixup 与现代初始化诊断]]", "[[正交初始化与 Dynamical Isometry]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Mishkin、Matas 2016：LSUV Initialization

> [!abstract] 来源定位
> 原论文提出 layer-sequential unit-variance：先用正交/半正交矩阵预初始化，再按一次校准 mini-batch 从浅到深测量各层输出 variance，并反复缩放当前层权重到接近 1。本库保留算法、停止条件与实验边界，不把一次 batch 校准等同于永久 normalization 或 Jacobian 全谱控制。
