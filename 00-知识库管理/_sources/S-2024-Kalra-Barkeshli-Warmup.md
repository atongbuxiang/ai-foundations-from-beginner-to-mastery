---
type: source
status: verified
area: [sources, optimization, warmup, sharpness]
source_type: paper
title: "Why Warmup the Learning Rate? Underlying Mechanisms and Improvements"
author: "Kalra and Barkeshli"
year: 2024
url: "https://arxiv.org/abs/2406.09405"
accessed: 2026-08-26
source_tier: A
scope_role: mechanism-study
related: ["[[Warmup、早期曲率与优化器状态建立]]", "[[二次模型的学习率—动量稳定域与阻尼]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Kalra 与 Barkeshli：Warmup、Sharpness 与 Catapult

> [!abstract] 来源定位
> 论文系统研究 SGD/Adam 的 warmup，提出 warmup 主要帮助轨迹进入可容忍更大目标学习率的区域，并区分 progressive sharpening 与 sharpness reduction 等阶段。课程把它作为机制证据，不写成唯一解释。

## 课程采用

- 同时记录 target LR、初始 LR、初始化/参数化和 Hessian top eigenvalue；
- 用二次稳定条件解释“局部可容忍”，但不把非凸轨迹化约为固定 Hessian；
- 讨论 catapult 与修改 Adam 初始二阶矩减少 warmup 的实验结果。

## 边界

论文的机制结论依赖模型、初始化、参数化与优化器；不能排除更新角度、早期 batch noise、低精度 overflow 或状态偏差修正等并行机制。
