---
type: source
status: verified
area: [sources, ai/long-context, positional-bias, evaluation]
source_type: paper
title: "Lost in the Middle: How Language Models Use Long Contexts"
author: "Nelson F. Liu et al."
year: 2024
url: "https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/Lost-in-the-Middle-How-Language-Models-Use-Long"
accessed: 2026-08-24
source_tier: A
license: "TACL/MIT Press; independent summary only"
scope_role: empirical-diagnostic
temporal_role: long-context-evaluation
related: ["[[位置分辨率、混叠与长度外推评测]]", "[[长上下文利用、Lost-in-the-Middle 与推理证据地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Lost in the Middle：证据位置效应

> [!abstract] 来源定位
> 论文系统改变相关信息在长输入中的位置，观察到多种模型对开头/结尾信息利用较好、中部较差的非单调位置效应。

## 课程采用

任何长上下文评测都应把 evidence position 作为自变量，而非固定 needle 在末尾；同时控制 context length、干扰文档数、任务与 prompt。

## 边界

U 形曲线是被测模型/任务的 E，不是所有模型的结构定理。位置效应也不能只归因于 RoPE；训练分布、causal recency、prompt 和 decoding 都可能贡献。
