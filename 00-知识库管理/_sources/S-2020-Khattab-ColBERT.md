---
type: source
status: verified
area: [sources, information-retrieval, late-interaction]
source_type: paper
title: "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT"
author: "Omar Khattab; Matei Zaharia"
year: 2020
url: "https://arxiv.org/abs/2004.12832"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: late-interaction
related: ["[[ANN Recall、Latency、Reranker 与两阶段检索]]"]
created: 2026-08-26
updated: 2026-08-26
---

# ColBERT：可预计算文档 token 表示的晚交互

> [!abstract] 来源定位
> ColBERT 独立编码 query/document token，再用 MaxSim 聚合细粒度相似度，在 cross-encoder 表达力与 single-vector 可索引性之间建立另一工作点。

晚交互仍有多向量存储和索引成本；论文的速度倍数取决于硬件、候选规模和对比系统。
