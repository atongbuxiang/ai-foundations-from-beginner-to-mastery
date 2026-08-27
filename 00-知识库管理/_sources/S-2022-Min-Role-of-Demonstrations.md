---
type: source
status: verified
area: [sources, in-context-learning, demonstrations]
source_type: paper
title: "Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?"
author: "Sewon Min et al."
year: 2022
url: "https://aclanthology.org/2022.emnlp-main.759/"
accessed: 2026-08-26
source_tier: P1
license: "ACL Anthology; independent summary"
scope_role: component-ablation
related: ["[[Zero-shot、Few-shot ICL、示例顺序与标签映射]]"]
created: 2026-08-26
updated: 2026-08-26
---

# ICL demonstrations 的成分消融

> [!abstract] 来源定位
> 论文在一组分类与多选协议上随机替换 demonstration labels，发现正确 input-label 对应的贡献可低于直觉，同时 label space、输入分布和格式仍重要。课程采用“示例内容—标签映射—格式”拆分，而不把全部效果叫作学会任务。

“随机标签影响小”是被测模型、任务与模板下的经验结果，不是正确标签永远无用；后续研究若改变模型、类别数、样例数或 instruction verbosity，必须重新测交互效应。
