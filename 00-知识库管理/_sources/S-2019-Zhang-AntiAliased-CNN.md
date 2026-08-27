---
type: source
status: draft
area: [sources, ai/cnn, signal-processing, equivariance]
source_type: paper
title: "Making Convolutional Networks Shift-Invariant Again"
author: Richard Zhang
year: 2019
url: "https://proceedings.mlr.press/v97/zhang19a.html"
accessed: 2026-08-24
source_tier: A
scope_role: core
temporal_role: original-method
related: ["[[池化、下采样、混叠与不变性边界]]", "[[局部连接、参数共享与平移等变性]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Zhang：Making Convolutional Networks Shift-Invariant Again

> [!abstract] 来源定位
> 论文将 CNN 中 stride/pooling 的 shift sensitivity 与采样前缺少低通联系起来，提出在下采样前加入固定 blur filter 的模块化方案，并在特定架构/任务上报告 shift consistency 与精度变化。课程用它连接 sampling theorem、aliasing 和经验 shift robustness；“重新获得 shift-invariance”不能脱离离散边界、滤波器、任务与实验协议理解。

## 核心断言审计

| 断言 | 类型 | 课程处理 |
|---|---|---|
| 下采样前应限制超过新 Nyquist 频率的成分 | 经典采样理论 `T` | 独立推导 |
| 常用 strided/pooling 算子可能对小平移敏感 | 结构 + 实验 `I/E` | 用最小反例和原实验分开 |
| BlurPool 改善若干模型/任务的 shift consistency | `E` | 保留模型、filter 与指标 |
| anti-aliasing 普遍提升准确率/鲁棒性 | 非普遍 | 不采用无条件表述 |

## 课程补严

- 区分 exact integer-shift equivariance、subpixel stability、classification consistency；
- 低通会丢高频，不是免费增强；
- max-pool 的非线性与 decimation 分开分析；
- 实际结果需回到 filter、padding、stride 和 dataset。
