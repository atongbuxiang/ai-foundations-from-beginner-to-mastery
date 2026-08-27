---
type: source
status: verified
area: [sources, optimization, large-batch, generalization]
source_type: paper
title: "On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima"
author: [Nitish Shirish Keskar, Dheevatsa Mudigere, Jorge Nocedal, Mikhail Smelyanskiy, Ping Tak Peter Tang]
year: 2017
url: "https://openreview.net/forum?id=H1oyRlYgg"
accessed: 2026-08-26
source_tier: A
venue: "ICLR 2017"
scope_role: primary
related: ["[[Critical Batch、隐式偏置与 SGD 证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Keskar 等 2017：Large-batch、generalization gap 与 sharpness

> [!abstract] 来源定位
> 论文在当时的模型和训练协议中报告 large-batch generalization gap，并给出 large-batch 更趋向 sharp minimizer 的数值证据。课程把它作为重要历史实证，不把“small batch → flat → generalize”写成已解决的因果链。

## 课程调用与反证接口

- 调用：原始实验问题、sharpness 指标和大/小 batch 现象；
- 对照：[[S-2017-Dinh-Sharp-Minima]]说明常见 sharpness 对 ReLU 重参数化不 invariant；
- 对照：[[S-2017-Hoffer-Large-Batch-Train-Longer]]说明 update 数和训练协议是混杂因素；
- 对照：大 batch 配合 LR scaling、warmup 与充足预算可在特定任务关闭 gap。

