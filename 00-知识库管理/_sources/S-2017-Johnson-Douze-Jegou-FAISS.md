---
type: source
status: verified
area: [sources, information-retrieval, ann]
source_type: paper
title: "Billion-scale Similarity Search with GPUs"
author: "Jeff Johnson; Matthijs Douze; Hervé Jégou"
year: 2017
url: "https://arxiv.org/abs/1702.08734"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: vector-search-systems
related: ["[[ANN Recall、Latency、Reranker 与两阶段检索]]", "[[Chunk、Metadata、Embedding 与 Index 合同]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Faiss：GPU k-selection、近似搜索与压缩域搜索

> [!abstract] 来源定位
> 论文研究高吞吐 GPU k-selection，并覆盖精确、近似和乘积量化搜索。课程用它说明“向量索引”包含距离、精度、压缩、候选和硬件合同。

系统吞吐数字依赖论文硬件与数据，不作为当前部署性能承诺。
