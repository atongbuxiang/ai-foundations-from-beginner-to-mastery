---
type: source
status: verified
area: [sources, language-models, llm-as-judge, bias]
source_type: paper
title: "Large Language Models are not Fair Evaluators"
author: "Peiyi Wang et al."
year: 2024
url: "https://aclanthology.org/2024.acl-long.511/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: position-bias-audit
related: ["[[LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]"]
created: 2026-08-26
updated: 2026-08-26
---

# LLM Judge 的位置偏差

> [!abstract] 来源定位
> 论文构造交换候选顺序的审计，显示 LLM evaluator 可产生系统性 position bias，并研究 balanced position 等校正。本库把 A/B 与 B/A 双评、冲突率和 human adjudication 作为最小门。

交换平均只能缓解可检测的位置效应，不消除长度、风格、模型家族、提示、事实知识和共同失误；校正后的 judge 仍需对独立人标集验证。
