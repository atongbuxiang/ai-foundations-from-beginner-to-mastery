---
type: source
status: draft
area: [sources, ai/cnn, efficient-architecture]
source_type: paper
title: "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications"
author: [Andrew G. Howard, Menglong Zhu, Bo Chen, Dmitry Kalenichenko, Weijun Wang, Tobias Weyand, Marco Andreetto, Hartwig Adam]
year: 2017
url: "https://arxiv.org/abs/1704.04861"
accessed: 2026-08-24
source_tier: A
scope_role: core
temporal_role: original-method
related: ["[[CNN 阶段、残差块与深度可分离卷积]]", "[[通道、卷积核、步幅、填充与膨胀的形状账本]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Howard et al.：MobileNets

> [!abstract] 来源定位
> MobileNet v1 用 depthwise spatial convolution 与 $1\times1$ pointwise channel mixing 分解标准 convolution，并以 width/resolution multipliers 建立准确率—资源折衷。课程采用其参数/MAC 分解和架构预算思想；设备 latency、能耗和现代 kernel 表现必须另测。

## 核心断言审计

| 断言 | 类型 | 课程处理 |
|---|---|---|
| depthwise+pointwise 的参数/MAC 公式 | 代数 `I` | 独立重算 |
| width/resolution multiplier 的成本缩放 | 近似代数 | 写出层间宽度与取整条件 |
| 在论文设备/任务上形成更好 trade-off | `E` | 不跨硬件外推 |
| 少 FLOPs 必然少 latency/energy | 不成立 | 加 IO、并行、kernel audit |

## 课程补严

- 分开空间混合与通道混合带来的表达限制；
- early high-resolution stages 可能 memory-bound；
- 与 ResNet bottleneck 的 $1\times1$ 用途比较但不混同。
