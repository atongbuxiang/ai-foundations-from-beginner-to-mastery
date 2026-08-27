---
type: source
status: draft
area: [sources, ai/transformers, rope-scaling, long-context]
source_type: blog
title: "Transformer升级之路：11、将β进制位置进行到底"
author: 苏剑林
year: 2023
url: "https://spaces.ac.cn/archives/9706"
accessed: 2026-08-24
source_tier: C
license: "科学空间；仅保存独立摘要、方法接口与链接"
scope_role: method-exposition
temporal_role: long-context
related: ["[[长度外推、位置插值与 RoPE 缩放]]", "[[位置分辨率、混叠与长度外推评测]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 混合进制与逐频率 RoPE 缩放

> [!abstract] 来源定位
> 文章沿 β 进制类比，把统一 base scaling 推广为频率依赖的混合缩放，并以小型实验比较免微调外推策略。

## 课程采用

把频率变换统一写成
$$
\omega_i'=\omega_i/s_i.
$$
$s_i=1$ 是原 RoPE，所有 $s_i=k$ 是线性位置插值；频率依赖 $s_i$ 覆盖 NTK-aware/混合方案。这样可在同一相位分辨率账中比较方法。

## 边界

缩放函数是设计选择；博客实验为特定模型/数据上的 E。NTK-aware 是历史名称，不能据此声称继承 neural tangent kernel 理论保证。
