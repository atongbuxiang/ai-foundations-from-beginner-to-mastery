---
type: source
status: verified
area: [sources, instruction-tuning, multitask]
source_type: paper
title: "Scaling Instruction-Finetuned Language Models"
author: "Hyung Won Chung et al."
year: 2022
url: "https://arxiv.org/abs/2210.11416"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: instruction-tuning-scaling
temporal_role: foundational-study
related: ["[[监督微调、Teacher Forcing 与 Response-only Loss]]", "[[指令数据质量、混合、多轮状态与选择偏差]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Scaling Instruction-Finetuned Language Models

> [!abstract] 来源定位
> 论文系统考察任务数量、模型规模与 chain-of-thought 数据对 instruction tuning 的影响，并报告跨模型族与评估设置的结果。课程调用其多任务 SFT 设计与 scaling 证据，但不把相关消融升级为“任何指令数据越多越好”的定理。

比较时必须保存任务集合、templates、mixture、held-out 定义、base checkpoint、训练预算和 selection protocol；模型规模与数据数量同时变化时不能唯一归因。

