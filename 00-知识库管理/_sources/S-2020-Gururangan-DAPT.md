---
type: source
status: verified
area: [sources, domain-adaptation, continual-pretraining]
source_type: paper
title: "Don't Stop Pretraining: Adapt Language Models to Domains and Tasks"
author: "Suchin Gururangan et al."
year: 2020
url: "https://aclanthology.org/2020.acl-main.740/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: continued-pretraining
temporal_role: foundational
related: ["[[Curriculum、持续预训练与域适配数据路径]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Don't Stop Pretraining：DAPT/TAPT

> [!abstract] 来源定位
> 论文比较 domain-adaptive 与 task-adaptive continued pretraining，并在具体任务上报告收益。课程用它建立 base checkpoint→域数据→任务数据→下游的路径账，要求同时测 in-domain gain、out-of-domain drift 和重复训练预算。

论文不证明任何 continued pretraining 都有益；数据量、域距离、objective、学习率、checkpoint 与下游监督共同决定结果。

