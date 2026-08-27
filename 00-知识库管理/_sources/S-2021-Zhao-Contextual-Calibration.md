---
type: source
status: verified
area: [sources, in-context-learning, calibration]
source_type: paper
title: "Calibrate Before Use: Improving Few-shot Performance of Language Models"
author: "Zihao Zhao et al."
year: 2021
url: "https://proceedings.mlr.press/v139/zhao21c.html"
accessed: 2026-08-26
source_tier: P1
license: "PMLR; independent summary"
scope_role: prompt-bias-diagnostic
related: ["[[Zero-shot、Few-shot ICL、示例顺序与标签映射]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Contextual Calibration：内容空输入与标签偏置

> [!abstract] 来源定位
> 论文显示 prompt 格式、示例与顺序可使 few-shot 分类显著波动，并用内容空输入估计标签偏置后做输出变换。课程采用 label-token prior、content-free probe 和校准前后分账。

这里的 contextual calibration 不等于通用概率校准；它依赖可获得的 label probability、verbalizer 和内容空输入选择，不能自动修复任务误解或示例泄漏。
