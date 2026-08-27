---
type: source
status: verified
area: [sources, language-models, llm-as-judge, preference]
source_type: paper
title: "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
author: "Lianmin Zheng et al."
year: 2023
url: "https://arxiv.org/abs/2306.05685"
accessed: 2026-08-26
source_tier: P1
license: "NeurIPS Datasets and Benchmarks paper; independent summary"
scope_role: llm-judge-benchmark
related: ["[[LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]"]
created: 2026-08-26
updated: 2026-08-26
---

# MT-Bench / Chatbot Arena：LLM Judge 与人类偏好

> [!abstract] 来源定位
> 论文用 MT-Bench 和 Chatbot Arena 研究强模型作为开放回答裁判，并显式讨论 position、verbosity、self-enhancement 与推理限制。本库采用 judge 需被独立验证和公开 prompt/顺序的原则。

特定 judge 与人类的一致率不能外推为“LLM judge 等于人类”；agreement 受样本、标签定义、人群、tie 处理、judge 版本与候选系统范围影响。
