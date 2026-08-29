---
type: source
status: active
area: [sources, neural-networks, label-smoothing, calibration, distillation]
source_type: paper
title: "When Does Label Smoothing Help?"
author: "Rafael Müller; Simon Kornblith; Geoffrey E. Hinton"
year: 2019
url: "https://proceedings.neurips.cc/paper/2019/hash/f1748d6b0fd9d439f71450117eba2725-Abstract.html"
venue: "NeurIPS 2019"
accessed: 2026-08-24
source_tier: A
license: "NeurIPS proceedings paper；本库仅保存独立摘要、必要结论与链接"
scope_role: mechanism-and-boundary
temporal_role: empirical-study
related: ["[[Label Smoothing、置信度与目标偏置]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]"]
created: 2026-08-24
updated: 2026-08-29
---

# Müller、Kornblith、Hinton：Label Smoothing 的帮助与代价

> [!abstract] 来源定位
> 论文研究 Label Smoothing 对表示、calibration、beam search 与 knowledge distillation 的影响，报告类内表示收紧以及 smoothed teacher 可能损失实例相似信息。它承担受控经验机制来源；这些结果绑定论文设置，不能简化为“低置信度总是更好”或“所有 teacher 都不应平滑”。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| LSH-C1 | Label Smoothing 可改变倒数第二层表示几何 | 经验机制 | 论文模型与数据 | 有证据，非普遍定理 |
| LSH-C2 | 某些设置下改善 calibration/beam search | 经验 | 指标与任务依赖 | 原范围成立 |
| LSH-C3 | smoothed teacher 在论文设置下不利 distillation | 经验边界 | teacher/student/protocol 依赖 | 不作普遍外推 |
| LSH-C4 | 较低 maximum confidence 等于更高 epistemic uncertainty | 概念外推 | target bias 不识别知识状态 | 错误 |
