---
type: source
status: verified
area: [sources, pretraining-data, gopher, filtering]
source_type: paper
title: "Scaling Language Models: Methods, Analysis & Insights from Training Gopher"
author: "Jack W. Rae et al."
year: 2021
url: "https://arxiv.org/abs/2112.11446"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: large-scale-recipe
temporal_role: historical-large-lm
related: ["[[解析、语言识别、质量过滤与数据偏差]]", "[[数据混合、温度采样、重加权与域损失]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Gopher / MassiveText 数据配方

> [!abstract] 来源定位
> Gopher 报告包含 MassiveText 来源混合、质量过滤、重复处理和模型分析。课程用它作为大型配方实例，要求把启发式规则、训练数据构成和论文实验拆开；某阈值在该设置有效不构成通用 quality 定义。

与 C4/RefinedWeb 比较时必须对齐 snapshot、语言、tokenizer、去重顺序、训练 FLOPs 和评测，而非只比较最终 token 数。

