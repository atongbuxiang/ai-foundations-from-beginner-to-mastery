---
type: source
status: verified
area: [sources, instruction-data, mixtures, templates]
source_type: paper
title: "The Flan Collection: Designing Data and Methods for Effective Instruction Tuning"
author: "Shayne Longpre et al."
year: 2023
url: "https://arxiv.org/abs/2301.13688"
accessed: 2026-08-26
source_tier: P1
license: "Paper and public collection; independent summary"
scope_role: instruction-data-design
temporal_role: foundational-study
related: ["[[指令数据质量、混合、多轮状态与选择偏差]]", "[[指令、消息、Chat Template 与任务序列化合同]]"]
created: 2026-08-26
updated: 2026-08-26
---

# The Flan Collection

> [!abstract] 来源定位
> 论文拆解 Flan 2022 的 task balancing、template、zero/few-shot 与 CoT mixture 等设计，并公开集合与方法。课程用它说明一个 instruction example 由 task、template、demonstrations 与 target 共同生成，任务数不等于独立语义覆盖。

公开 collection 仍需版本、祖先数据许可、benchmark overlap、每任务 draws/tokens/targets 和模板重复审计；其报告增益绑定具体模型与评估集。

