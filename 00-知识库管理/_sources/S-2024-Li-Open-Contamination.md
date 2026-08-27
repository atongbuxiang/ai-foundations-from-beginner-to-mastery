---
type: source
status: verified
area: [sources, evaluation, data-contamination]
source_type: paper
title: "An Open-Source Data Contamination Report for Large Language Models"
author: "Yucheng Li, Yunhao Guo, Frank Guerin, Chenghua Lin"
year: 2024
url: "https://aclanthology.org/2024.findings-emnlp.30/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: contamination-audit
temporal_role: modern-audit
related: ["[[Benchmark 污染、时间截止与成员重叠审计]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Open-Source Data Contamination Report

> [!abstract] 来源定位
> 论文提供开放污染检测管线并比较多模型/benchmark，显示污染比例与分数增益不必一一对应。课程用它区分 exposure、memorization 和 exploitation，并要求报告 detector operating point、假阳/假阴与模型版本。

黑箱检测结果是统计证据，不是训练 membership 的逐样本法证结论；API 更新和未公开 post-training data 会改变可解释范围。

