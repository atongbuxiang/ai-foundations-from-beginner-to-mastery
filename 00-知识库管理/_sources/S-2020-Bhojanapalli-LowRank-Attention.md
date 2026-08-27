---
type: source
status: draft
area: [sources, ai/attention, math/matrix-analysis]
source_type: paper
title: "Low-Rank Bottleneck in Multi-head Attention Models"
author: "Srinadh Bhojanapalli et al."
year: 2020
url: "https://proceedings.mlr.press/v119/bhojanapalli20a.html"
accessed: 2026-08-24
source_tier: A
license: "PMLR paper; independent summary only"
scope_role: core
temporal_role: foundational-analysis
related: ["[[Multi-Head Attention、投影子空间与参数量]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Multi-head Attention 的低秩瓶颈

> [!abstract] 来源定位
> 论文研究给定 head projection dimension 时，softmax attention matrix 的可表示性何时受限。课程用它补充“logit rank 小”之外更精确的表达问题，并保留序列长度、头宽、输入/投影与构造条件。

## 课程判断

- $QK^\top$ 的严格秩至多为 $d_k$ 是直接线性代数恒等式；
- row-wise softmax 是非线性映射，所以 $\operatorname{rank}(\operatorname{softmax}(QK^\top))$ **不**自动受 $d_k$ 同样约束；
- 论文的瓶颈结论讨论哪些 stochastic attention matrices 能由特定维度的 dot-product/softmax 形式表达，不能简化成“attention matrix 的秩永远不超过 head dimension”；
- 增大 head dimension 可解除某些表示障碍，但不保证优化、泛化或吞吐更优。

## 调用

- [[Multi-Head Attention、投影子空间与参数量]]：固定总宽下 head 数与 per-head width 的权衡；
- [[Attention 矩阵的秩、瓶颈与有效秩]]：区分 logit rank、attention rank、output rank 与表示可达性；
- [[Attention 失效模式、反例与证据地图]]：防止把论文标题误读成无条件低秩定理。
