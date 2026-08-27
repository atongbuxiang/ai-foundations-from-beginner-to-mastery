---
type: source
status: active
area: [sources, neural-networks, elu]
source_type: paper
title: "Fast and Accurate Deep Network Learning by Exponential Linear Units"
author: [Djork-Arné Clevert, Thomas Unterthiner, Sepp Hochreiter]
year: 2016
url: "https://arxiv.org/abs/1511.07289"
accessed: 2026-08-23
source_tier: A
venue: "ICLR 2016"
scope_role: origin
temporal_role: classic
related: ["[[ELU、SELU 与自归一化接口]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Clevert–Unterthiner–Hochreiter 2016：ELU

> [!abstract] 来源定位
> 原论文提出 ELU，强调正侧 identity、负输出与负侧饱和，并在当时的 CIFAR/ImageNet 架构中报告训练和准确率结果。本库采用函数定义与机制假设，同时把“bias shift/natural-gradient 接近性”保留为条件性解释，不视为任意现代架构上的完整因果证明。
