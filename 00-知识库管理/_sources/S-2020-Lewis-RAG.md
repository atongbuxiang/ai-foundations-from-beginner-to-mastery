---
type: source
status: verified
area: [sources, language-models, rag]
source_type: paper
title: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
author: "Patrick Lewis et al."
year: 2020
url: "https://arxiv.org/abs/2005.11401"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: foundational-model
related: ["[[参数记忆、外部记忆与 RAG 潜变量分解]]", "[[RAG 的 Retrieval—Generation—Attribution 评估地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# RAG：参数记忆与非参数记忆的生成式结合

> [!abstract] 来源定位
> 论文把检索文档写成生成模型的潜变量，提出序列级共享文档的 RAG-Sequence 与 token 级边缘化的 RAG-Token。课程采用其概率分解、可更新外部知识和 provenance 动机。

论文实验不证明检索必然减少幻觉；若语料缺失、retriever 失败或 generator 不使用证据，端到端答案仍会失败。
