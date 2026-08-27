---
type: source
status: active
area: [sources, neural-networks, activations, initialization]
source_type: paper
title: "Understanding the Difficulty of Training Deep Feedforward Neural Networks"
author: [Xavier Glorot, Yoshua Bengio]
year: 2010
url: "https://proceedings.mlr.press/v9/glorot10a.html"
accessed: 2026-08-23
source_tier: A
venue: "AISTATS 2010, PMLR 9:249–256"
scope_role: foundation
temporal_role: classic
related: ["[[激活函数的角色、选择准则与函数性质]]", "[[Sigmoid、Tanh 与饱和梯度]]", "[[Xavier、Glorot 初始化]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Glorot–Bengio 2010：训练深层前馈网络的困难

> [!abstract] 来源定位
> 原论文分析 logistic sigmoid 的非零均值与饱和、逐层 activation/gradient statistics 和 Jacobian singular-value 直觉，并提出后来称为 Xavier/Glorot 的初始化。本库用它连接激活、均值漂移和初始化；论文中的架构、数据与 2010 年实验不能被外推为所有现代 residual/normalized 网络的排名结论。
