---
type: source
status: verified
area: [sources, pretraining-data, refinedweb, web-filtering]
source_type: paper
title: "The RefinedWeb Dataset for Falcon LLM"
author: "Guilherme Penedo et al."
year: 2023
url: "https://arxiv.org/abs/2306.01116"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: web-corpus-recipe
temporal_role: large-web-data
related: ["[[解析、语言识别、质量过滤与数据偏差]]", "[[精确去重、MinHash、LSH 与近重复检测]]"]
created: 2026-08-26
updated: 2026-08-26
---

# RefinedWeb

> [!abstract] 来源定位
> RefinedWeb 报告以大规模过滤、去重的 Common Crawl web data 训练 Falcon 系列并提供数据抽取。课程调用其可扩展 pipeline、filter/dedup 次序与 web-only 实验；论文中优于特定 curated-corpus 对照的结果不外推为“web-only 永远最优”。

复现需锁定 crawl 列表、URL/content normalization、语言与质量 classifier、重复阈值、保留代表策略和 tokenizer。

