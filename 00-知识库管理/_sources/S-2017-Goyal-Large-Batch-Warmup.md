---
type: source
status: verified
area: [sources, optimization, warmup, large-batch]
source_type: paper
title: "Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour"
author: "Goyal et al."
year: 2017
url: "https://arxiv.org/abs/1706.02677"
accessed: 2026-08-26
source_tier: A
scope_role: original-empirical-protocol
related: ["[[Warmup、早期曲率与优化器状态建立]]", "[[学习率、局部损失变化与相对更新尺度]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Goyal 等：大批量线性缩放与渐进 Warmup

> [!abstract] 来源定位
> 论文在 ResNet-50/ImageNet、同步 SGD 和大批量扩展协议中联合使用线性学习率缩放与 gradual warmup。它是重要工程证据，不是“学习率必随 batch 线性增长”的一般定理。

## 课程采用

- 把 batch、每 epoch 更新次数、base/target LR 和 warmup 时长写成同一协议；
- 说明突然切到大 target LR 会在训练早期破坏近似等价；
- 把“batch 8192 无精度损失”限定在论文的模型、数据、实现和调参范围内。

## 不外推

Adam/Muon、不同归一化、token batch、长上下文与改变训练 token 数时，线性缩放和 warmup 都必须重新验证。
