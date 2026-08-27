---
type: source
status: draft
area: [sources, neural-networks, language-modeling, embedding-factorization, parameter-sharing]
source_type: paper
title: "ALBERT: A Lite BERT for Self-supervised Learning of Language Representations"
author: "Zhenzhong Lan; Mingda Chen; Sebastian Goodman; Kevin Gimpel; Piyush Sharma; Radu Soricut"
year: 2020
url: "https://openreview.net/forum?id=H1eA7AEtvS"
arxiv: "https://arxiv.org/abs/1909.11942"
venue: "ICLR 2020"
accessed: 2026-08-24
source_tier: A
license: "OpenReview/arXiv paper；本库仅保存独立摘要、必要公式与链接"
scope_role: factorization-core
temporal_role: foundational
related: ["[[Embedding 初始化、缩放、分解与量化接口]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Lan et al.：ALBERT 的 Factorized Embedding Parameterization

> [!abstract] 来源定位
> ALBERT 用较小 embedding dimension 把大词表表与较大 hidden dimension 解耦，并另用跨层参数共享降低深度参数量。它承担 $V\times H$ 词表矩阵分解为 $V\times E$ 与 $E\times H$ 的代表性原始证据；本库不把 ALBERT 的整体实验归因于单一因子分解。

## 参数合同

传统 token-to-hidden 表需要 $VH$ 参数；factorized parameterization 需要 $VE+EH$，当 $E\ll H$ 且 $V$ 很大时显著减少词表参数。它同时施加 rank/共享中间空间约束，并为每 token 增加小矩阵 projection；与论文的 cross-layer sharing、SOP objective 必须分开消融。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| ALB-C1 | $VE+EH$ 可替代直接 $VH$ 参数化 | 结构 | 中间维 $E$ | 精确 |
| ALB-C2 | 因子分解不改变可表示 embedding table 集合 | 线性代数 | $E<H$ 时 rank 受限 | 错误 |
| ALB-C3 | 参数更少必然等比例降低 wall time | 系统外推 | projection、kernel、带宽相关 | 不成立 |
| ALB-C4 | ALBERT 全部改进都来自 factorized embedding | 归因混淆 | 还有跨层共享与 objective | 不成立 |
