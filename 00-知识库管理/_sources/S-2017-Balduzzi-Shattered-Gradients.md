---
type: source
status: draft
area: [sources, neural-networks, residual-networks, gradient-correlation]
source_type: paper
title: "The Shattered Gradients Problem: If ResNets Are the Answer, Then What Is the Question?"
author: "David Balduzzi; Marcus Frean; Lennox Leary; J. P. Lewis; Kurt Wan-Duo Ma; Brian McWilliams"
year: 2017
url: "https://proceedings.mlr.press/v70/balduzzi17b.html"
venue: "ICML 2017, PMLR 70"
accessed: 2026-08-23
source_tier: A
license: "PMLR paper；本库仅保存独立摘要、必要结论与链接"
scope_role: core
temporal_role: foundational
related: ["[[深度、有效路径与稳定性证据地图]]", "[[残差块 Jacobian 与梯度直通]]", "[[相关传播、Edge of Chaos 与临界初始化]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Balduzzi et al.：Shattered Gradients

> [!abstract] 来源定位
> 论文把“梯度 norm 是否消失/爆炸”与“不同输入上的梯度相关性是否快速衰减”分开，研究 skips 对 shattered-gradient 现象的影响。它承担 gradient-correlation 问题的原始定义和特定模型分析；本库不把相关性结果替代 Jacobian singular values 或优化收敛证明。

## 核心对象

给定不同输入 $x,x'$，可比较参数或激活梯度的相关系数，而不只比较

$$
\|\nabla \mathcal L(x)\|.
$$

两个梯度都可有正常 norm，却近乎正交、对输入呈噪声般不稳定。论文在其随机网络模型与实验中发现，plain network 的相关性可随深度指数衰减，而带 skip 的模型可改善为更慢的衰减。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| SG-C1 | 梯度大小与梯度相关性是不同诊断量 | 对象定义 | 需声明梯度对象和输入分布 | 精确 |
| SG-C2 | 正常 gradient norm 排除 shattered gradients | 对象混淆 | 相关性仍可接近零 | 错误 |
| SG-C3 | skips 在论文模型中减缓相关性衰减 | 理论+经验 | 指定随机模型、初始化与架构 | 有条件成立 |
| SG-C4 | 相关性改善自动推出泛化或收敛 | 结论外推 | 缺少损失、优化与分布假设 | 不成立 |

## 课程调用边界

使用本卡时必须同时登记 forward signal、gradient norm、gradient correlation、parameter update 与任务性能，不能用其中一个代理全体。

