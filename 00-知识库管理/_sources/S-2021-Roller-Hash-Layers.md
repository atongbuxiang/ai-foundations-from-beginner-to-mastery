---
type: source
status: draft
area: [sources, ai/moe, hash-routing]
source_type: paper
title: "Hash Layers For Large Sparse Models"
author: "Stephen Roller et al."
year: 2021
url: "https://arxiv.org/abs/2106.04426"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: routing-alternative
related: ["[[Router、Gate、Top-k 与稀疏组合]]", "[[MoE 门控归一化、证据地图与开放问题]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Hash Layers：无需可学习 Router 的稀疏参数选择

> [!abstract] 来源定位
> Hash Layers 用 token/local feature 的预定映射选择不同 FFN 参数，比较 learned routing、balanced/random hashes 与 downstream transfer。

## 调用边界

- 无 router/aux loss 不等于无数据分布假设；hash table 与 tokenizer/词频耦合；
- 原论文的竞争力是其任务和预算下的 `E`；
- hash routing 改变条件信息来源，不能与 learned context routing 只按负载比较。
