---
type: source
status: verified
area: [sources, language-models, privacy, extraction]
source_type: paper
title: "Extracting Training Data from Large Language Models"
author: "Nicholas Carlini et al."
year: 2021
url: "https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting"
accessed: 2026-08-26
source_tier: P1
license: "USENIX paper; independent summary"
scope_role: training-data-extraction-evidence
related: ["[[Memorization、Exposure、Canary 与训练数据抽取]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 训练数据抽取：从生成候选到人工核验

> [!abstract] 来源定位
> 论文展示从语言模型生成大量候选、按异常性排序并核验训练语料重合的抽取流程。结论绑定特定模型、可访问接口、采样与排序预算；“模型记住”与“攻击者在给定预算内抽取”必须分开。

课程仅讲攻击面、测量口径与防御审计，不复刻真实个人信息或提供面向在线系统的提取操作。
