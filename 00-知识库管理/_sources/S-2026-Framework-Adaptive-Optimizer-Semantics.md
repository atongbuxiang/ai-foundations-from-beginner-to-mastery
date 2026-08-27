---
type: source
status: verified
area: [sources, software, optimization, pytorch, tensorflow]
source_type: documentation
title: "PyTorch and TensorFlow Adaptive Optimizer Documentation"
author: [PyTorch Contributors, TensorFlow Contributors]
year: 2026
url: "https://docs.pytorch.org/docs/main/optim.html"
accessed: 2026-08-26
source_tier: A
scope_role: implementation-authority
temporal_role: current-documentation
related: ["[[AdaGrad、累计平方梯度与稀疏几何]]", "[[RMSProp、滑动二阶矩与非平稳尺度]]", "[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]", "[[Adam 的 Epsilon、数值稳定与实现分歧]]", "[[L2 正则、Coupled Decay 与 AdamW]]", "[[Lion、Adafactor 与自适应优化器证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 当前框架的自适应优化器语义

> [!abstract] 来源定位
> 当前官方文档承担 API 和更新顺序，不承担一般收敛理论。所有事实以 2026-08-26 访问的 PyTorch `main/stable` 与 TensorFlow API 文档为准；升级框架后需重新核对。

## 已核对事实

1. PyTorch Adam 的 `weight_decay` 默认是 coupled L2-style gradient modification；当前 `decoupled_weight_decay=True` 与 AdamW 语义对齐；
2. PyTorch AdamW 明确不让 decay 累积进 momentum 或 variance state；
3. PyTorch Adam/AdamW 的展示公式使用 $\sqrt{\widehat v_t}+\epsilon$；
4. PyTorch RMSprop 明确说明先开根再加 epsilon，而 TensorFlow 的 RMSProp 交换这两步；
5. TensorFlow/Keras Adam 文档称其 `epsilon` 对应原论文中的 “epsilon hat”，不能只凭同一个参数名认定公式相同；
6. PyTorch AdaGrad 另有 `initial_accumulator_value` 与 `lr_decay`；
7. PyTorch Adafactor 文档明确说明其 LR、$\epsilon_1$ 与原论文/部分框架不同，并采用 LR-scaled decoupled decay；
8. `foreach`/`fused`/capturable/differentiable 路径会影响性能、内存与末位数值，实验必须记录。

## 使用规则

课程里的“Adam”先指明抽象更新；涉及真实 checkpoint 或逐步复现时，再附框架、版本、param group、step counter、epsilon placement、decay coupling、AMSGrad、dtype、overflow/skip 和执行后端。
