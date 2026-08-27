---
type: source
status: draft
area: [sources, ai/transformers, positional-interpolation, long-context]
source_type: paper
title: "Extending Context Window of Large Language Models via Positional Interpolation"
author: "Shouyuan Chen, Sherman Wong, Liangjian Chen, Yuandong Tian"
year: 2023
url: "https://arxiv.org/abs/2306.15595"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: method-paper
temporal_role: context-extension
related: ["[[长度外推、位置插值与 RoPE 缩放]]", "[[位置分辨率、混叠与长度外推评测]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Position Interpolation

> [!abstract] 来源定位
> 论文把目标长上下文 position indices 线性压回原训练范围，并通过少量长序列微调扩展 RoPE 模型；同时比较直接 extrapolation 与 interpolation 的 attention score bound。

## 核心变换

训练范围 $L_0$、目标范围 $L_1=kL_0$ 时，用
$$
n\mapsto n/k
$$
进入 RoPE。最大相对相位回到原范围，但相邻位置相位差缩小，产生分辨率拥挤。

## 边界

理论 bound 保留论文范数与最坏情形假设；32K 等结果属于所测 LLaMA、微调和任务协议的 E。线性插值不是无需训练的通用保证。
