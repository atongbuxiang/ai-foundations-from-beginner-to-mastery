---
type: source
status: draft
area: [sources, ai/transformers, sparse-attention, theory]
source_type: paper
title: "Big Bird: Transformers for Longer Sequences"
author: "Manzil Zaheer et al."
year: 2020
url: "https://arxiv.org/abs/2007.14062"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: theory-and-method
related: ["[[局部、分块与稀疏 Attention]]", "[[Transformer 表达、稳定性与证据边界]]"]
created: 2026-08-24
updated: 2026-08-24
---

# BigBird：Local、Random 与 Global 稀疏图

> [!abstract] 来源定位
> BigBird 把局部边、随机边和 global-token 边组合为稀疏 attention graph，并在明确结构/规模条件下给出表达理论和实验。

## 调用边界

- 稀疏图的连通、直径与表达定理不能移植到任意 local mask；
- “通用逼近/Turing complete”是存在型理论，不等于有限深宽可训练性；
- 线性复杂度仍需真正的 block-sparse kernel 承担。
