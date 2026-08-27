---
type: source
status: verified
area: [sources, training, debugging, autodiff]
source_type: official-documentation
title: "Automatic differentiation package — anomaly detection"
author: PyTorch
year: 2026
url: "https://docs.pytorch.org/docs/stable/autograd"
accessed: 2026-08-26
source_tier: B
scope_role: implementation
temporal_role: current
related: ["[[NaN、Inf、梯度爆炸与训练失败决策树]]"]
created: 2026-08-26
updated: 2026-08-26
---

# PyTorch：Autograd Anomaly Detection

> [!abstract] 来源定位
> `detect_anomaly(check_nan=True)` 可在 backward 失败时给出相应 forward traceback，并在 backward 生成 NaN 时抛错，是定位首个异常算子的官方调试接口。

## 本卷调用

- 先用低开销 finite/amax hooks 缩小 step 与 module，再在最小窗口启用 anomaly detection；
- forward traceback 指向产生失败 backward function 的前向上下文，不自动等于根因；
- 将异常 tensor、输入 batch、RNG、checkpoint 与 backend 一起冻结为复现包。

## 边界

该模式有显著开销，只用于调试；它不能捕捉所有“大但仍有限”的先兆，也不能替代数据、optimizer 或系统层反事实实验。
