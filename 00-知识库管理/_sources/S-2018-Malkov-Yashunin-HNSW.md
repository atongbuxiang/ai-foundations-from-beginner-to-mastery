---
type: source
status: verified
area: [sources, information-retrieval, ann]
source_type: paper
title: "Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs"
author: "Yu. A. Malkov; D. A. Yashunin"
year: 2018
url: "https://arxiv.org/abs/1603.09320"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: ann-index
related: ["[[ANN Recall、Latency、Reranker 与两阶段检索]]"]
created: 2026-08-26
updated: 2026-08-26
---

# HNSW：分层可导航小世界图的近邻搜索

> [!abstract] 来源定位
> HNSW 用随机层级和邻接图从粗到细导航，暴露构建参数、搜索宽度、内存与 recall/latency 权衡。课程把 ANN recall 与语义 retriever recall 严格分开。

“对数复杂度”是论文分析与经验趋势，不应替代给定数据、维度、距离和参数下的实测尾延迟。
