---
type: source
status: active
area: [sources, neural-networks, dynamical-isometry, random-matrix-theory]
source_type: paper
title: "Resurrecting the Sigmoid in Deep Learning through Dynamical Isometry: Theory and Practice"
author: [Jeffrey Pennington, Samuel S. Schoenholz, Surya Ganguli]
year: 2017
url: "https://proceedings.neurips.cc/paper/7064-resurrecting-the-sigmoid-in-deep-learning-through-dynamical-isometry-theory-and-practice"
accessed: 2026-08-23
source_tier: A
venue: "NeurIPS 2017"
related: ["[[正交初始化与 Dynamical Isometry]]", "[[相关传播、Edge of Chaos 与临界初始化]]", "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Pennington、Schoenholz、Ganguli 2017：Dynamical Isometry

> [!abstract] 来源定位
> 原论文研究深网输入—输出 Jacobian 的完整奇异值分布，明确区分均方奇异值为 $O(1)$ 与全部奇异值集中在 1 附近。本库调用 dynamical isometry 的定义、正交权重的作用与非线性边界；具体结论绑定论文所分析的初始化 ensemble、activation 与宽深极限。
