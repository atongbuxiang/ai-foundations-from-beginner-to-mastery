---
type: source
status: verified
area: [sources, nlp, summarization, metrics]
source_type: paper
title: "ROUGE: A Package for Automatic Evaluation of Summaries"
author: "Chin-Yew Lin"
year: 2004
url: "https://aclanthology.org/W04-1013/"
accessed: 2026-08-26
source_tier: P1
license: "ACL workshop paper; independent summary"
scope_role: rouge-definition
related: ["[[Exact Match、F1、BLEU、ROUGE 与语义指标边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# ROUGE：Recall-Oriented Overlap 与 LCS

> [!abstract] 来源定位
> ROUGE 包含 ROUGE-N、ROUGE-L、ROUGE-W、ROUGE-S 等参考重叠指标。本库重点手算 ROUGE-N recall 与基于 longest common subsequence 的 ROUGE-L，并要求披露 stemming、tokenization、多参考聚合与 precision/recall/F 方向。

高 ROUGE 可来自复制参考，低 ROUGE 可来自正确释义；它不是无参考事实性或整体写作质量的充分统计量。
