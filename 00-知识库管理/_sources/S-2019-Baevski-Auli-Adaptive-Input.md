---
type: source
status: draft
area: [sources, neural-networks, language-modeling, adaptive-input, embeddings]
source_type: paper
title: "Adaptive Input Representations for Neural Language Modeling"
author: "Alexei Baevski; Michael Auli"
year: 2019
url: "https://openreview.net/forum?id=ByxZX20qFQ"
venue: "ICLR 2019"
accessed: 2026-08-24
source_tier: A
license: "OpenReview conference paper；本库仅保存独立摘要、必要公式与链接"
scope_role: adaptive-dimension-core
temporal_role: foundational
related: ["[[Embedding 初始化、缩放、分解与量化接口]]", "[[Sampled、Hierarchical 与 Adaptive Softmax]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Baevski、Auli：Adaptive Input Representations

> [!abstract] 来源定位
> 论文把 adaptive softmax 的频率分桶思想扩展到输入表示，为不同频率组分配不同容量，并系统比较 input/output factorization 与 tying 选择。它承担 frequency-adaptive embedding 的原始证据；速度和 perplexity 结论绑定论文模型、数据和硬件。

## 方法合同

高频词使用较大 embedding dimension，低频组使用更小 dimension，再投影到共同 hidden space。参数量成为各组 $V_gd_g$ 与 projection 的和，而非统一 $Vd$；必须保存 token-to-group 映射和 frequency ordering，词表漂移后需重验。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| AIR-C1 | 不同频率组可使用不同表示容量 | 结构 | 显式 group/projection | 成立 |
| AIR-C2 | 低频词永远只需低维语义 | 普遍外推 | rare 可关键且频率会漂移 | 不成立 |
| AIR-C3 | adaptive input 与 adaptive output 可独立或联合设计 | 实验合同 | 需注明 tying/projection | 成立 |
| AIR-C4 | 参数计数只需 $\sum_gV_gd_g$ | 计数遗漏 | 还需 group projections/元数据 | 错误 |
