---
type: source
status: verified
area: [sources, generative-models, evaluation]
source_type: paper
title: "A note on the evaluation of generative models"
author: "Lucas Theis; Aäron van den Oord; Matthias Bethge"
year: 2015
url: "https://arxiv.org/abs/1511.01844"
venue: "ICLR 2016"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: evaluation-boundary
temporal_role: foundational
related: ["[[Mode Collapse、模式覆盖与生成器熵]]", "[[GAN 稳定化方法、受控比较与证据地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Theis et al.：生成模型评价边界

> [!abstract] 来源定位
> 论文用反例强调 likelihood、Parzen estimate 与视觉样本质量在高维可相当独立；模型应按实际用途直接评价。课程借此阻止“样本清晰→覆盖好”“FID 低→likelihood 好”之类跨指标外推。

## 课程采用

- 生成质量、覆盖、density 与任务效用分账；
- 明确 evaluator feature、样本量、preprocess 与估计偏差；
- 避免以 Parzen-window likelihood 作为高维通用排名；
- 画廊用于失败发现，不能单独做分布结论。

