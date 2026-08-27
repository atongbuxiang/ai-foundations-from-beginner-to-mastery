---
type: source
status: verified
area: [sources, language-models, privacy, extraction]
source_type: paper
title: "Scalable Extraction of Training Data from (Production) Language Models"
author: "Milad Nasr et al."
year: 2023
url: "https://arxiv.org/abs/2311.17035"
accessed: 2026-08-26
source_tier: P1
license: "Research paper; independent summary"
scope_role: production-extraction-threat-model
related: ["[[Memorization、Exposure、Canary 与训练数据抽取]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 可扩展训练数据抽取

> [!abstract] 来源定位
> 论文研究面向生产语言模型的可扩展抽取，并强调常规行为与特殊生成条件下风险可能不同。课程只采用其 threat-model 与预算意识：访问级别、生成成本、去重、核验和伦理约束都属于结论的一部分。

本文是攻击研究证据，不是可直接照搬的测试手册；本库实验用有限玩具候选空间替代真实服务与真实训练语料。
