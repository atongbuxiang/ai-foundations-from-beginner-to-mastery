---
type: source
status: verified
area: [sources, nlp, semantic-metrics]
source_type: paper
title: "BERTScore: Evaluating Text Generation with BERT"
author: "Tianyi Zhang et al."
year: 2020
url: "https://arxiv.org/abs/1904.09675"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: contextual-similarity-metric
related: ["[[Exact Match、F1、BLEU、ROUGE 与语义指标边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# BERTScore：Contextual Token Matching

> [!abstract] 来源定位
> BERTScore 用上下文化 token embedding 的相似度做候选—参考的软匹配并聚合 precision/recall/F。本库用它解释“语义指标”仍依赖 encoder、layer、tokenization、IDF、baseline rescaling 与聚合版本。

Embedding 相似不等于逻辑蕴含、事实一致或任务成功；报告相关性必须绑定人评维度、数据域和比较系统，不能把原论文相关性普遍外推。
