---
type: source
status: draft
area: [sources, ai/attention, ai/efficient-transformers]
source_type: blog
title: "线性Transformer应该不是你要等的那个模型"
author: 苏剑林
year: 2021
url: "https://spaces.ac.cn/archives/8610"
accessed: 2026-08-24
source_tier: C
license: "科学空间；仅保存独立摘要与链接"
scope_role: counterexample-bridge
temporal_role: modern-exposition
related: ["[[Attention 矩阵的秩、瓶颈与有效秩]]", "[[Attention 失效模式、反例与证据地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 线性 Transformer 的反直觉问题

> [!abstract] 来源定位
> 文章从 feature dimension、低秩结构和经验配置讨论：线性 Attention 为保持效果可能需要更宽特征，因而理论复杂度下降未必转化为所期待的速度/质量收益。课程把它当作“反例与实验设计”入口，不采用固定倍数为普遍规律。

## 课程采用

- factorized affinity 的代数秩不超过 feature dimension；
- 减少 token-pair 中间量可能增加 feature-width、投影或 kernel 成本；
- 特定实验中出现的约四倍宽度是 `E` 级观察，依模型、数据、长度、实现而变；
- “不是你要等的模型”是评论性判断，不是理论不可能性定理。

## 必做核验

比较 exact 与 linear attention 时同时对齐质量、参数、FLOP、显存、训练/推理长度、batch、dtype、kernel 和 wall-clock；分开报告 kernel approximation error 与完整 normalized output error。
