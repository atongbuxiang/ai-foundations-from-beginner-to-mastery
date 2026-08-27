---
type: source
status: verified
area: [sources, ai/scaling-laws, parameter-counting]
source_type: paper
title: "Reconciling Kaplan and Chinchilla Scaling Laws"
author: "Tim Pearce, Jinyeop Song"
year: 2024
url: "https://arxiv.org/abs/2406.12907"
accessed: 2026-08-26
source_tier: B
license: "arXiv preprint; independent summary only"
scope_role: counting-audit
temporal_role: active-research
related: ["[[Kaplan 参数数据律、联合拟合与有限区间]]", "[[IsoFLOP、训练算力口径与系统校正]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Reconciling Kaplan and Chinchilla Scaling Laws

> [!abstract] 来源定位
> 论文研究参数统计口径与小尺度窗口如何使 Kaplan/Chinchilla 的 compute-optimal 指数看似矛盾，主张 total/non-embedding parameter choice 是重要解释之一。

## 可调用证据

- 同一模型的 total parameter 与 non-embedding parameter 在小尺度不成稳定比例；
- 把横轴从一种参数口径换成另一种会改变局部 log slope；
- 小规模 embedding 占比和有限窗口可偏置外推；
- scaling 报告应同时给 total、active、non-embedding 参数及对应 compute formula。

## 边界

- 参数口径不是全部分歧的唯一解释；
- 模拟 Chinchilla 设置不等于获得原始训练日志；
- 论文结论不允许把 embedding 永远纳入或永远排除，关键是对象与公式一致。
