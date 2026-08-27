---
type: source
status: verified
area: [sources, model-merging, task-vectors]
source_type: paper
title: "Editing Models with Task Arithmetic"
author: "Gabriel Ilharco et al."
year: 2023
url: "https://openreview.net/forum?id=6t0Kwf8-jrj"
accessed: 2026-08-26
source_tier: P1
license: "ICLR paper; independent summary"
scope_role: task-vector-arithmetic
temporal_role: foundational-method
related: ["[[Model Soup、Task Arithmetic、TIES 与适配证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Task Arithmetic

> [!abstract] 来源定位
> Task arithmetic 把同一 base 与 task checkpoint 的差定义为 task vector，并实验加、减与缩放后的行为编辑。课程调用坐标差、线性组合和缩放系数，同时明确这不是函数空间线性的普遍定理。

所有 vectors 必须共享精确 base、架构、参数命名与 tokenizer；成功合并取决于局部几何、任务冲突和 evaluation，不由向量加法语法保证。

