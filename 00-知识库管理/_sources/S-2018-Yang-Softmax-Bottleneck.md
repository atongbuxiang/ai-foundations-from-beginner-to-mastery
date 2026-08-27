---
type: source
status: draft
area: [sources, neural-networks, language-modeling, softmax-bottleneck]
source_type: paper
title: "Breaking the Softmax Bottleneck: A High-Rank RNN Language Model"
author: "Zhilin Yang; Zihang Dai; Ruslan Salakhutdinov; William W. Cohen"
year: 2018
url: "https://openreview.net/forum?id=HkwZSG-CZ"
venue: "ICLR 2018"
accessed: 2026-08-24
source_tier: A
license: "OpenReview conference paper；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[Softmax Bottleneck 与低秩限制]]", "[[Softmax 输出层、Logit 尺度与概率参数化]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Yang et al.：Softmax Bottleneck 与 Mixture of Softmaxes

> [!abstract] 来源定位
> 论文把多上下文语言建模写成 log-probability matrix factorization，指出标准 hidden–output dot product 加 Softmax 受到低秩限制，并提出 Mixture of Softmaxes（MoS）。它承担 bottleneck 与 MoS 的原始论证；本库改用 centered log-ratio matrix 显式处理 row-shift gauge，并不把论文的自然语言高秩主张外推到任意数据分布。

## 核心对象

对多个 contexts，把目标条件分布的 log probabilities 排成矩阵。标准 logits 由 hidden matrix 与 output embeddings 的低维乘积产生；Softmax 只再减去逐 context 的 log-partition，因此可表达矩阵族受 hidden dimension 限制。MoS 使用 context-dependent mixture weights 混合多个 Softmax distributions，`log(sum)` 的非线性可越出单一低秩族。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| SB-C1 | 标准线性 Softmax head 的跨 context log-probability family 受秩约束 | 代数 | 固定有限 hidden dimension 与线性 head | 精确 |
| SB-C2 | 单个 context 的 Softmax 不能表示任意正 categorical law | 对象混淆 | 自由 logits 可覆盖 simplex interior | 错误 |
| SB-C3 | MoS 可突破单一线性 Softmax 的低秩族 | 结构 | mixture 权重/分量依赖 context | 成立 |
| SB-C4 | 所有自然语言数据的最小所需秩都有同一数值 | 普遍外推 | tokenizer、contexts、样本与估计有关 | 不成立 |
