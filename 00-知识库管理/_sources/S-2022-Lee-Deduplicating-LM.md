---
type: source
status: verified
area: [sources, pretraining-data, deduplication, memorization]
source_type: paper
title: "Deduplicating Training Data Makes Language Models Better"
author: "Katherine Lee et al."
year: 2022
url: "https://aclanthology.org/2022.acl-long.577/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: deduplication-evidence
temporal_role: modern-foundation
related: ["[[精确去重、MinHash、LSH 与近重复检测]]", "[[Benchmark 污染、时间截止与成员重叠审计]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Deduplicating Training Data Makes Language Models Better

> [!abstract] 来源定位
> 论文提出 exact substring 与 MinHash 近文档去重，并在其数据/模型协议中报告 memorized output、训练效率和 train–validation overlap 改善。课程调用算法与实验设计，不把“去重总会提高所有质量”写成定理。

删除哪一份 duplicate 会改变时间、来源和群体构成；cluster representative policy 与被拒文本日志必须保存。
