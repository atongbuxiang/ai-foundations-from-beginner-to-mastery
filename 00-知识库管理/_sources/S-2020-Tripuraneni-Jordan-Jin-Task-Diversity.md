---
type: source
status: active
area: [sources, representation-learning, transfer-learning, task-diversity]
source_type: paper
title: "On the Theory of Transfer Learning: The Importance of Task Diversity"
author: [Nilesh Tripuraneni, Michael I. Jordan, Chi Jin]
year: 2020
url: "https://proceedings.neurips.cc/paper_files/paper/2020/hash/59587bffec1c7846f3e34230141556ae-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "NeurIPS 2020"
scope_role: primary
temporal_role: modern-theory
related: ["[[表示学习的任务、表示与下游风险]]", "[[Linear Probe、Fine-Tuning 与迁移评估]]"]
created: 2026-08-23
updated: 2026-08-23
---

# On the Theory of Transfer Learning: The Importance of Task Diversity

> [!abstract] 来源定位
> 以 task-specific heads composed with a shared representation 形式化 transfer，并说明 training task diversity 是识别共享表示、降低 new-task labeled sample complexity 的关键。本库用它反驳“任务数量多就自动通用”。

## 本库调用

1. task family 可写成 task head 与 shared representation 的复合；
2. representation complexity 与 head complexity 分账；
3. task diversity 不是 task count 的同义词；
4. guarantee 只覆盖声明的 task/data model；
5. 新任务超出共享结构时可出现 negative transfer；
