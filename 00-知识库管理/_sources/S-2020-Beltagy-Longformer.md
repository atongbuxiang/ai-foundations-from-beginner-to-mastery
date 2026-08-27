---
type: source
status: draft
area: [sources, ai/transformers, sparse-attention, long-context]
source_type: paper
title: "Longformer: The Long-Document Transformer"
author: "Iz Beltagy, Matthew E. Peters, Arman Cohan"
year: 2020
url: "https://arxiv.org/abs/2004.05150"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: method-paper
related: ["[[局部、分块与稀疏 Attention]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Longformer：滑动窗口与任务驱动 Global Tokens

> [!abstract] 来源定位
> Longformer 组合局部滑动窗口和少量任务相关 global attention，使 edge 数在固定窗口下随长度线性增长。Global token 提供短图距离，但其选择和数量属于任务设计。

## 调用边界

- 线性 pair count 以窗口宽度和 global token 数不随 $n$ 同阶增长为前提；
- 局部窗口的全局感受野需要随层数传播，不等于单层任意两点直连；
- 论文下游收益为特定预训练/微调设置的 `E`。
