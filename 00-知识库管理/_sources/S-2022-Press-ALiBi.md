---
type: source
status: draft
area: [sources, ai/transformers, alibi, length-extrapolation]
source_type: paper
title: "Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation"
author: "Ofir Press, Noah A. Smith, Mike Lewis"
year: 2022
url: "https://openreview.net/forum?id=R8sQPpGCv0"
accessed: 2026-08-24
source_tier: A
license: "ICLR/OpenReview; independent summary only"
scope_role: method-paper
temporal_role: long-context
related: ["[[相对位置表示、偏置与距离函数]]", "[[长度外推、位置插值与 RoPE 缩放]]", "[[位置分辨率、混叠与长度外推评测]]"]
created: 2026-08-24
updated: 2026-08-24
---

# ALiBi：Attention Logits 上的线性距离偏置

> [!abstract] 来源定位
> ALiBi 不向 token state 添加 position vector，而在各 head 的 causal attention logits 加随距离线性下降的固定斜率，并以 train-short/test-long 语言模型实验验证。

## 形式

对 causal $j\le i$，
$$
\ell^{(h)}_{ij}=\frac{q_i^\top k_j}{\sqrt{d_h}}-m_h(i-j),
$$
$m_h>0$ 为 head-specific slope。它对距离施加显式 recency prior，无新 learned position table。

## 边界

线性偏置定义可外算到任意距离，不等于模型能有效使用任意长度。局部语言模型收益与非局部算法/检索任务必须分别评价。
