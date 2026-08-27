---
type: source
status: verified
area: [sources, information-retrieval, sparse-retrieval]
source_type: monograph
title: "The Probabilistic Relevance Framework: BM25 and Beyond"
author: "Stephen Robertson; Hugo Zaragoza"
year: 2009
url: "https://doi.org/10.1561/1500000019"
accessed: 2026-08-26
source_tier: P1
license: "Publisher work; independent summary"
scope_role: canonical-sparse-retrieval
related: ["[[BM25、Dense Retrieval、Hybrid 与 Score Fusion]]"]
created: 2026-08-26
updated: 2026-08-26
---

# BM25：概率相关框架中的词项饱和与长度校正

> [!abstract] 来源定位
> 该综述系统整理 Binary Independence Model、BM25/BM25F 与相关反馈。课程采用 BM25 的词频饱和、逆文档频率和文档长度归一化，并强调实现变体会改变分数。

BM25 分数通常只在同一实现与查询内有排序意义；不应与 dense score 未经校准地直接相加。
