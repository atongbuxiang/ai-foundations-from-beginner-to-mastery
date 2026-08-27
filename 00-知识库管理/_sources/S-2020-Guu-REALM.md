---
type: source
status: verified
area: [sources, language-models, retrieval]
source_type: paper
title: "Retrieval Augmented Language Model Pre-Training"
author: "Kelvin Guu et al."
year: 2020
url: "https://proceedings.mlr.press/v119/guu20a.html"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: latent-retriever
related: ["[[参数记忆、外部记忆与 RAG 潜变量分解]]", "[[Retriever 训练、Negative Sampling 与 Query-Document 目标]]"]
created: 2026-08-26
updated: 2026-08-26
---

# REALM：用语言建模信号训练潜检索器

> [!abstract] 来源定位
> REALM 在预训练、微调和推理中访问大规模语料，以 masked-LM 信号对潜文档做边缘化并向 retriever 传播学习信号。课程借此说明“端到端”必须交代候选集、索引刷新与近似边缘化。

其结论绑定开放域问答、Wikipedia 快照和特定训练机制，不等同于任意生产 RAG 都已端到端优化。
