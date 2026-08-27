---
type: source
status: verified
area: [sources, language-models, security, structured-query]
source_type: paper
title: "StruQ: Defending Against Prompt Injection with Structured Queries"
author: "Sizhe Chen et al."
year: 2024
url: "https://arxiv.org/abs/2402.06363"
accessed: 2026-08-26
source_tier: P1
license: "Research paper; independent summary"
scope_role: structured-query-defense
related: ["[[Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]"]
created: 2026-08-26
updated: 2026-08-26
---

# StruQ：结构化查询防注入

> [!abstract] 来源定位
> 论文以结构化查询和训练方法分隔 prompt 与不可信数据。课程把它作为 defense-in-depth 的一层：序列化边界若不被模型学习并由系统权限约束，纯分隔符不能成为证明。

防御证据绑定其模型、训练、攻击集和效用指标；对工具调用还需 schema validation、least privilege 与 human confirmation。
