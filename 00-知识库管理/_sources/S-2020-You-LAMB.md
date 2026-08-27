---
type: source
status: verified
area: [sources, optimization, large-batch, transformers]
source_type: paper
title: "Large Batch Optimization for Deep Learning: Training BERT in 76 minutes"
author: "You et al."
year: 2020
url: "https://arxiv.org/abs/1904.00962"
accessed: 2026-08-26
source_tier: A
venue: "ICLR 2020"
scope_role: original-method-and-evidence
related: ["[[Update-to-Weight Ratio、谱与尺度诊断]]"]
created: 2026-08-26
updated: 2026-08-26
---

# You 等：LAMB

> [!abstract] 来源定位
> LAMB 把 Adam-like coordinate normalization 与 layerwise adaptation 组合，用于大批量 BERT/ResNet 训练。本卷用它说明“方向预条件”和“层级步长归一”是两层机制。

## 本卷调用

- 先构造带 moment/epsilon/decay 的方向，再计算 layer trust ratio；
- telemetry 同时报 preconditioned direction norm、trust ratio 与 realized update norm；
- 比较必须匹配 batch、schedule、warmup、训练时长与 tuning budget。

## 边界

论文范围内的大批量加速不等于 layerwise ratio 是唯一原因；LAMB 与 LARS 的分母和 decay 语义不可混写。
