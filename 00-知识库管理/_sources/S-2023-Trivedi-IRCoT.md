---
type: source
status: verified
area: [sources, language-models, multi-hop-retrieval]
source_type: paper
title: "Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions"
author: "Harsh Trivedi et al."
year: 2023
url: "https://aclanthology.org/2023.acl-long.557/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: iterative-retrieval
related: ["[[Multi-hop、Iterative、Graph Retrieval 与 Tool Interface]]"]
created: 2026-08-26
updated: 2026-08-26
---

# IRCoT：在推理步骤之间交错检索

> [!abstract] 来源定位
> IRCoT 让已生成的中间推理更新下一次查询，再由新证据更新后续推理，针对单次 query 无法表达后继信息需求的多跳问题。

可见 CoT 仍可能不忠实；因此课程把 query state、retrieved IDs、support graph 与 final answer 分开保存。
