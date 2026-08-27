---
type: source
status: verified
area: [sources, fine-tuning, catastrophic-forgetting]
source_type: paper
title: "An Empirical Study of Catastrophic Forgetting in Large Language Models During Continual Fine-tuning"
author: "Yun Luo et al."
year: 2023
url: "https://arxiv.org/abs/2308.08747"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: continual-finetuning-forgetting
temporal_role: empirical-study
related: ["[[全量微调、冻结表示与灾难性遗忘]]", "[[Curriculum、持续预训练与域适配数据路径]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Continual Fine-tuning 中的灾难性遗忘

> [!abstract] 来源定位
> 论文在特定 1B—7B 模型与持续 instruction-tuning 设置中测量域知识、推理和阅读理解遗忘。课程调用其“功能遗忘须按旧能力切片实测”的实验范式，而不把模型规模趋势外推到所有架构、任务序列或训练配方。

参数距离、旧域 loss、行为准确率和安全变化是不同对象；checkpoint selection、原始能力 ceiling、训练预算与 replay 必须控制。

