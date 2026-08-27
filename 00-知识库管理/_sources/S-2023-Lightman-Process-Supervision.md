---
type: source
status: verified
area: [sources, reasoning, process-verification]
source_type: paper
title: "Let's Verify Step by Step"
author: "Hunter Lightman et al."
year: 2023
url: "https://arxiv.org/abs/2305.20050"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: process-supervision
related: ["[[Test-time Compute、Search、Verifier 与预算]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Process Reward Model 与步骤监督

> [!abstract] 来源定位
> 论文在 MATH 协议上比较 outcome supervision 与逐步 process supervision，并发布 PRM800K。课程采用 step label、first-error、trajectory score 聚合与 active-learning 记录。

特定数据与模型上的过程监督优势不是所有领域的定理；步骤标签可能不完备，局部正确也不保证全局解答正确，PRM 还可能被搜索策略利用。
