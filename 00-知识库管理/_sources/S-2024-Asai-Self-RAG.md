---
type: source
status: verified
area: [sources, language-models, adaptive-retrieval]
source_type: paper
title: "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection"
author: "Akari Asai et al."
year: 2024
url: "https://openreview.net/forum?id=hSyW5go0v8"
accessed: 2026-08-26
source_tier: P1
license: "ICLR paper; independent summary"
scope_role: adaptive-retrieval-control
related: ["[[Multi-hop、Iterative、Graph Retrieval 与 Tool Interface]]", "[[RAG 的 Retrieval—Generation—Attribution 评估地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Self-RAG：学习何时检索以及如何批判支持性

> [!abstract] 来源定位
> Self-RAG 以 reflection tokens 表示是否检索、文档相关性、生成支持性和总体效用。课程借此区分 retrieve policy、critic 与 generator，而不把“自反思”当不可观测能力。

反思 token 是训练出的预测，不是真值；仍需外部标注或审计评估其校准和失败模式。
