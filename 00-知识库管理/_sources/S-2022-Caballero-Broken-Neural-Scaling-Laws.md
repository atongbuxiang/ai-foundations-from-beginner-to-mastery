---
type: source
status: verified
area: [sources, ai/scaling-laws, broken-power-law]
source_type: paper
title: "Broken Neural Scaling Laws"
author: "Ethan Caballero, Kshitij Gupta, Irina Rish, David Krueger"
year: 2022
url: "https://arxiv.org/abs/2210.14891"
accessed: 2026-08-26
source_tier: B
license: "arXiv preprint; independent summary only"
scope_role: alternative-model
temporal_role: active-research
related: ["[[Broken Scaling、涌现表象与优化架构数据分解]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Broken Neural Scaling Laws

> [!abstract] 来源定位
> 论文提出 smoothly broken power-law 函数族，允许一个或多个尺度处的局部斜率平滑改变，并在多种任务/模态上比较拟合与外推。

## 可调用证据

- 单一 exponent 不是唯一候选；多个 regime 可由连续曲线连接；
- kink、double descent、延迟改善与非单调行为需要比简单直线更丰富的模型；
- 局部斜率和 breakpoint 位置本身需要不确定性；
- 更灵活模型必须用 held-out extrapolation 抵消额外自由度。

## 边界

- 更好拟合不证明 breakpoint 对应新的物理/学习机制；
- breakpoint 可由指标、优化不足、数据/架构变化或选择偏差制造；
- 高自由度 BNSL 在小样本窗口中可能过拟合。
