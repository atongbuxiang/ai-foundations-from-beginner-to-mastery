---
type: source
status: verified
area: [sources, optimization, schedule-free, averaging]
source_type: paper
title: "The Road Less Scheduled"
author: "Defazio et al."
year: 2024
url: "https://arxiv.org/abs/2405.15682"
accessed: 2026-08-26
source_tier: A
scope_role: original-method-and-theory
related: ["[[训练时域、Restart、Schedule-Free 与末端学习率]]", "[[参数 EMA、SWA 与 Checkpoint Averaging]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Defazio 等：Schedule-Free 优化

> [!abstract] 来源定位
> 论文从“依赖停止时刻 $T$ 的 schedule 通常更强”出发，用插值点与在线平均统一 scheduling 和 iterate averaging，并给出 Schedule-Free SGD/AdamW。课程采用其状态变量和 train/eval 语义，不把名称理解为“没有任何时间依赖”。

## 课程采用

- 区分优化点 $y_t$、平均点 $z_t$ 与插值/评估点 $x_t$；
- 记录 warmup、权重序列、momentum 和 train/eval 切换；
- 比较时同时匹配 peak LR、总 step、averaging state 和 checkpoint selection。

## 边界

“不预先声明停止时刻”不等于不需要 LR、warmup、状态或部署时选择规则；官方实现版本仍需锁定。
