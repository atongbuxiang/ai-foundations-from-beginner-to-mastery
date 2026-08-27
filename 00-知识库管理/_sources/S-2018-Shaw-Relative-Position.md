---
type: source
status: draft
area: [sources, ai/transformers, relative-position]
source_type: paper
title: "Self-Attention with Relative Position Representations"
author: "Peter Shaw, Jakob Uszkoreit, Ashish Vaswani"
year: 2018
url: "https://aclanthology.org/N18-2074/"
accessed: 2026-08-24
source_tier: A
license: "ACL Anthology; independent summary only"
scope_role: foundational
temporal_role: relative-position
related: ["[[相对位置表示、偏置与距离函数]]", "[[二维、多轴与多模态位置编码]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Shaw 相对位置表示

> [!abstract] 来源定位
> 论文将相对位移 embedding 分别加入 key-side score 与 value-side aggregation，并通过 clipping 支持有限相对距离表。课程用它区分 logit bias、relative key 和 relative value 三种注入点。

## 核心形式

$$
e_{ij}=\frac{q_i^\top(k_j+a^K_{ij})}{\sqrt{d_k}},
\qquad
z_i=\sum_j\alpha_{ij}(v_j+a^V_{ij}),
$$
其中 $a_{ij}$ 通常由 clip$(j-i)$ 查表。

## 边界

Clipping 使远距离共享同一参数，是归纳偏置也是分辨率损失。论文任务结果为 E，不证明所有任务应只使用相对位置。
