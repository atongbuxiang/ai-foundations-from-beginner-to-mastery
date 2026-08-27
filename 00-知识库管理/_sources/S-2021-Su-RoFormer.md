---
type: source
status: draft
area: [sources, ai/transformers, rope]
source_type: paper
title: "RoFormer: Enhanced Transformer with Rotary Position Embedding"
author: "Jianlin Su et al."
year: 2021
url: "https://arxiv.org/abs/2104.09864"
accessed: 2026-08-24
source_tier: A
license: "arXiv/journal paper; independent summary only"
scope_role: foundational
temporal_role: rope
related: ["[[RoPE 的旋转推导、群表示与内积]]", "[[长度外推、位置插值与 RoPE 缩放]]"]
created: 2026-08-24
updated: 2026-08-24
---

# RoFormer 与 Rotary Position Embedding

> [!abstract] 来源定位
> 原始 RoFormer 论文正式给出 RoPE：Q/K 先按绝对位置旋转，dot-product 中只留下相对位移；并报告长文本分类等实验。

## 证据分层

| 断言 | 等级 |
|---|---|
| $R_m^\top R_n=R_{n-m}$ 与 norm 保持 | I |
| 论文所给函数形式及线性 attention 接口 | I/T（按论文条件） |
| 论文 benchmark 改进 | E |
| 注意力必随距离衰减、任意长度均可外推 | 不作无条件采用 |

课程以论文为历史/方法主证据，以科学空间文章补中文推导与后续变体脉络。
