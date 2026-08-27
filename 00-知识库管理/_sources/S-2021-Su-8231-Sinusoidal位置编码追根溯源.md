---
type: source
status: draft
area: [sources, ai/transformers, positional-encoding]
source_type: blog
title: "Transformer升级之路：1、Sinusoidal位置编码追根溯源"
author: 苏剑林
year: 2021
url: "https://spaces.ac.cn/archives/8231"
accessed: 2026-08-24
source_tier: C
license: "科学空间；仅保存独立摘要、推导接口与链接"
scope_role: derivation-bridge
temporal_role: foundational-exposition
related: ["[[置换对称性与位置编码的必要性]]", "[[Sinusoidal 位置编码、频率与相对位移]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Sinusoidal 位置编码追根溯源

> [!abstract] 来源定位
> 文章尝试从“绝对位置内积应表达相对位移”和平均远程衰减等要求反推频率式位置编码。课程采用三角恒等式与平移旋转关系；Taylor 小量、近似 Hessian 及频率选择理由保留为带假设的 H。

## 可核验接口

对每个频率 $\omega$，二维块
$$
p_\omega(n)=(\cos\omega n,\sin\omega n)
$$
满足
$$
p_\omega(n+\Delta)=R(\omega\Delta)p_\omega(n),
\qquad
p_\omega(m)^\top p_\omega(n)=\cos\omega(m-n).
$$
二式为 I；它们说明绝对坐标可在线性/内积运算中产生相对位移结构。

## 边界

几何频率表、远程衰减与效果之间不是定理等价。文章也明确回顾了小位置扰动、近似矩阵与频率选择假设；“能表达相对位移”不等于“必然学会顺序或长度外推”。
