---
type: source
status: verified
area: [sources, language-models, security, prompt-injection]
source_type: paper
title: "More than you've asked for: A Comprehensive Analysis of Novel Prompt Injection Threats to Application-Integrated Large Language Models"
author: "Kai Greshake et al."
year: 2023
url: "https://arxiv.org/abs/2302.12173"
accessed: 2026-08-26
source_tier: P1
license: "Research paper; independent summary"
scope_role: indirect-injection-threat-model
related: ["[[Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 间接 Prompt Injection

> [!abstract] 来源定位
> 论文系统讨论应用集成语言模型从网页、邮件或检索内容读取不可信文本时，数据可被模型解释为指令的间接注入风险。课程以此建立 trust boundary、asset、attacker capability 与 tool consequence 图。

正文不收录可复用攻击载荷；防御重点是权限、数据流、动作确认和审计，而非假设一句系统提示可形成可靠安全边界。
