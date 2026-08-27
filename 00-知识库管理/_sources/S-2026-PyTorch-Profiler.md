---
type: source
status: verified
area: [sources, training, telemetry, performance]
source_type: official-documentation
title: "PyTorch Profiler"
author: PyTorch
year: 2026
url: "https://docs.pytorch.org/docs/main/profiler"
accessed: 2026-08-26
source_tier: B
scope_role: implementation
temporal_role: current
related: ["[[训练 Telemetry、损失梯度更新与激活总账]]", "[[NaN、Inf、梯度爆炸与训练失败决策树]]"]
created: 2026-08-26
updated: 2026-08-26
---

# PyTorch：Profiler

> [!abstract] 来源定位
> 当前框架对 CPU/CUDA operator 时间、memory、shape、stack 与 trace 的官方入口。它回答“在哪里花了时间/内存”，不能单独回答“为什么质量改变”。

## 本卷调用

- 用 warmup—active—repeat 窗口控制 profiler 扰动，并保存 schedule；
- 将 operator/self time、memory、kernel 与 distributed trace 对齐到 step/microstep；
- profile 结果只构成性能证据，需与 loss、gradient、update 和质量时间线联接；
- 高开销 stack/shape/module 采集按诊断窗口开启，而非默认全程开启。

## 边界

trace 受异步执行、同步点、编译预热和采样窗口影响；单次 top-op 表不等于关键路径，也不证明因果根因。
