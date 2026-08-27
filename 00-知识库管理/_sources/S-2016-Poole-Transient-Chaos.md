---
type: source
status: active
area: [sources, neural-networks, signal-propagation, edge-of-chaos]
source_type: paper
title: "Exponential Expressivity in Deep Neural Networks through Transient Chaos"
author: [Ben Poole, Subhaneil Lahiri, Maithra Raghu, Jascha Sohl-Dickstein, Surya Ganguli]
year: 2016
url: "https://proceedings.neurips.cc/paper/2016/hash/148510031349642de5ca0c544f31b2ef-Abstract.html"
accessed: 2026-08-23
source_tier: A
venue: "NeurIPS 2016"
related: ["[[相关传播、Edge of Chaos 与临界初始化]]", "[[方差传播与宽层均值场近似]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Poole et al. 2016：Transient Chaos 与相关传播

> [!abstract] 来源定位
> 原论文把宽随机深网的两输入相关性写成深度方向的 mean-field 动力系统，并研究 ordered/chaotic phase、临界线与流形几何。本库调用 covariance/correlation map 和局部稳定性主线；“chaos 提升表达”不自动等于更易训练或更好泛化。
