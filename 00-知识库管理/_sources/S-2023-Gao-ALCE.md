---
type: source
status: verified
area: [sources, language-models, citations]
source_type: paper
title: "Enabling Large Language Models to Generate Text with Citations"
author: "Tianyu Gao; Howard Yen; Jiatong Yu; Danqi Chen"
year: 2023
url: "https://aclanthology.org/2023.emnlp-main.398/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: citation-evaluation
related: ["[[Context Construction、Citation、Grounding 与冲突证据]]", "[[RAG 的 Retrieval—Generation—Attribution 评估地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# ALCE：答案正确性、引用完整性与引用正确性

> [!abstract] 来源定位
> ALCE 把带引用长文本生成做成端到端基准，并分开流畅性、答案正确性与 citation quality。课程据此建立 claim—citation—passage 三层账。

自动 entailment 指标只是人工支持判断的代理；不能把“引用了某页”直接当成该页蕴含对应命题。
