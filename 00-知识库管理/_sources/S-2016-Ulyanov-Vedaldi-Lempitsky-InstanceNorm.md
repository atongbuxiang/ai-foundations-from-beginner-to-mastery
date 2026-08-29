---
type: source
status: active
area: [sources, neural-networks/normalization, vision]
source_type: paper
title: "Instance Normalization: The Missing Ingredient for Fast Stylization"
author: "Dmitry Ulyanov; Andrea Vedaldi; Victor Lempitsky"
year: 2016
url: "https://arxiv.org/abs/1607.08022"
venue: "arXiv 1607.08022；扩展工作发表于 CVPR 2017"
accessed: 2026-08-23
source_tier: A
license: "author/arXiv paper；本库仅保存独立摘要、短公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[InstanceNorm、GroupNorm 与 WeightNorm]]", "[[归一化的对象、轴与不变性]]"]
created: 2026-08-23
updated: 2026-08-29
---

# Ulyanov–Vedaldi–Lempitsky：Instance Normalization

> [!abstract] 来源定位
> 论文把卷积特征的统计组从跨样本 BatchNorm 改为每个样本、每个 channel 的空间位置，并在快速风格化任务中报告质量改善。它支持 InstanceNorm 的历史动机与经验角色；统计轴、状态和 affine 默认值仍需与具体实现合同分开。

## 数学对象

对 $X\in\mathbb R^{N\times C\times H\times W}$，固定 $(n,c)$，在 $(h,w)$ 上计算

$$
\mu_{nc}=\frac1{HW}\sum_{h,w}X_{nchw},
\qquad
q_{nc}=\frac1{HW}\sum_{h,w}(X_{nchw}-\mu_{nc})^2.
$$

所以其他样本不进入该统计组；同一 channel 的空间位置仍然前向、反向耦合。

## 断言表

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| IN-C1 | InstanceNorm 按 instance/channel 归约空间轴 | 定义 | 卷积布局明确 | 已建立 |
| IN-C2 | 不需要跨 batch 统计即可运行 | 数学结构 | 使用当前 instance 统计 | 已建立 |
| IN-C3 | 替换 BN 改善快速风格化质量 | 经验 | 原论文生成器与任务 | 保留设置边界 |
| IN-C4 | train/eval 必然同路径 | 实现命题 | 取决于是否跟踪 running statistics | 非普遍 |

## 限制

- 原论文不是“InstanceNorm 对所有视觉任务优于 BatchNorm”的证据；
- 删除每通道空间均值与对比度可能同时删除任务需要的绝对强度信息；
- $HW=1$ 时 centered normalization 退化；
- 若归约轴含时间，离线计算可能读取未来位置；
- framework 的 affine/state 默认值不是论文数学定义的一部分。
