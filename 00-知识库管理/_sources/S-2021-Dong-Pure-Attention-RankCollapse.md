---
type: source
status: draft
area: [sources, ai/attention, ai/deep-networks, math/matrix-analysis]
source_type: paper
title: "Attention is not all you need: pure attention loses rank doubly exponentially with depth"
author: "Yihe Dong, Jean-Baptiste Cordonnier, Andreas Loukas"
year: 2021
url: "https://proceedings.mlr.press/v139/dong21a.html"
accessed: 2026-08-24
source_tier: A
license: "PMLR paper; independent summary only"
scope_role: core
temporal_role: theory
related: ["[[Attention 矩阵的秩、瓶颈与有效秩]]", "[[Attention 失效模式、反例与证据地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Pure Attention 深度下的秩退化

> [!abstract] 来源定位
> 论文在特定假设下证明：没有 skip connection 和 MLP 的 pure self-attention 堆叠会快速趋向 token uniformity/rank-one 结构。它证明了残差与 MLP 的结构角色，却不是“完整 Transformer 必然秩一”的定理。

## 阅读合同

| 层级 | 可采用结论 |
|---|---|
| `T` | 对论文规定的 pure attention map、范数与参数条件，residual component 随深度双指数衰减 |
| `I` | token 行完全相同的表示矩阵严格秩至多 1 |
| `E` | 论文实验支持相关趋势，但只覆盖其模型与协议 |
| 禁止外推 | 含 residual、MLP、normalization、position、causal mask 的任意 Transformer 都必然坍缩 |

## 课程补严

“秩退化”还要区分表示矩阵、logit、attention 权重与输出；严格秩、数值秩、stable rank、谱熵 effective rank 也不可混用。完整模型是否坍缩应以层间谱、token 差异、任务指标和干预共同验证。
