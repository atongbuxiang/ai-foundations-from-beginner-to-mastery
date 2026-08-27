---
type: source
status: draft
area: [sources, ai/transformers, ai/attention, ai/architecture]
source_type: blog
title: "为什么现在的LLM都是Decoder-only的架构？"
author: 苏剑林
year: 2023
url: "https://spaces.ac.cn/archives/9529"
accessed: 2026-08-24
source_tier: C
license: "科学空间；仅保存独立摘要、短推理与链接"
scope_role: hypothesis-bridge
temporal_role: active-research
related: ["[[Attention Mask、因果性与可见性合同]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]", "[[Attention 失效模式、反例与证据地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Decoder-only、因果掩码与低秩猜想

> [!abstract] 来源定位
> 文章从训练目标、架构统一性及 Attention 秩提出 decoder-only 流行原因的解释。课程保留其中一个可严格核验的线性代数事实，并把“这解释了架构优越性”明确标为机制猜想。

## 可严格核验的部分

inclusive causal softmax attention matrix 是下三角矩阵；若每个对角位置 logit 有限，则 softmax 后对角权重严格为正，因此

$$
\det A=\prod_i A_{ii}>0,
$$

故 $A$ 满秩。这不表示它条件良好：对角元素可极小，奇异值可高度集中，有效秩也可很低。

## 证据分级

| 断言 | 等级 |
|---|---|
| 正对角下三角矩阵满秩 | `I` |
| 某些双向 attention 在数据/训练中呈低有效秩 | `E`，需实测 |
| 满秩因果 attention 因而解释 decoder-only 的总体优势 | `H` |
| Decoder-only 在所有任务/资源上最优 | 不采用 |

后续必须比较 objective、data mixture、parameter allocation、KV cache、训练并行、质量与长度外推，不能用一个秩事实替代架构裁决。
