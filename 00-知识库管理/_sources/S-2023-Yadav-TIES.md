---
type: source
status: verified
area: [sources, model-merging, ties]
source_type: paper
title: "TIES-Merging: Resolving Interference When Merging Models"
author: "Prateek Yadav et al."
year: 2023
url: "https://proceedings.neurips.cc/paper_files/paper/2023/hash/1644c9af28ab7916874f6fd6228a9bcf-Abstract-Conference.html"
accessed: 2026-08-26
source_tier: P1
license: "NeurIPS paper; independent summary"
scope_role: sign-aware-task-vector-merging
temporal_role: foundational-method
related: ["[[Model Soup、Task Arithmetic、TIES 与适配证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# TIES-Merging

> [!abstract] 来源定位
> TIES 以 trim、elect sign、merge 三步处理小幅更新与 task-vector 符号冲突。课程逐坐标重建算法，并把 density、sign election、aggregation 与 scale 作为必须记录的超参数。

符号冲突是参数坐标中的 proxy，不等于功能冲突的完整刻画；TIES 的经验优势不能外推到不同 base、未对齐参数或所有 LLM 任务组合。

