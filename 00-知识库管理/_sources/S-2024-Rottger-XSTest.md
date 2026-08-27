---
type: source
status: verified
area: [sources, language-models, safety, over-refusal]
source_type: paper
title: "XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models"
author: "Paul Röttger et al."
year: 2024
url: "https://aclanthology.org/2024.naacl-long.301/"
accessed: 2026-08-26
source_tier: P1
license: "ACL Anthology paper; independent summary"
scope_role: exaggerated-safety-evaluation
related: ["[[Abstention、Refusal、Over-refusal 与风险覆盖]]"]
created: 2026-08-26
updated: 2026-08-26
---

# XSTest：过度安全行为

> [!abstract] 来源定位
> XSTest 以看似敏感但应正常回答的提示识别 exaggerated safety。课程用它补齐拒答评估的负类：只测危险请求上的拒答率，会奖励“全部拒绝”的无用系统。

测试集是诊断切片，不能替代真实 benign population；语义、文化和多语言迁移需单独审计。
