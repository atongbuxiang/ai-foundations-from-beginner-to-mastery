---
type: source
status: verified
area: [sources, ai-training, gpu-systems]
source_type: official-documentation
title: "Train With Mixed Precision"
author: NVIDIA
year: 2023
url: "https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html"
accessed: 2026-08-15
source_tier: B
license: "NVIDIA 官方文档；知识库仅保存独立摘要、流程映射与链接"
scope_role: implementation
temporal_role: current-guidance
aliases: [NVIDIA-2023-Mixed-Precision]
related: ["[[浮点数与舍入误差]]", "[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]", "[[Loss Scaling、Master Weight 与低精度梯度累积]]"]
created: 2026-08-15
updated: 2026-08-15
---

# NVIDIA：混合精度训练指南

> [!abstract] 来源定位
> 该指南把 FP16 数值范围与训练流程连接起来：loss scaling 保留小梯度，FP32 主权重累积小更新，大归约和统计量使用 FP32。它是本章 AI 接口的工程主来源。

## 核心流程

1. 适当算子使用 FP16 输入/执行；
2. 对 loss 乘缩放因子 $S$；
3. 反向得到放大后的梯度；
4. 检查 Inf/NaN；
5. 更新前反缩放；
6. 关键权重/状态和大归约保留 FP32；
7. 动态调整 $S$，溢出时跳过更新。

## 边界

- loss scaling 管理范围，不增加 significand bits；
- FP16 最大有限数 $65504$ 约束 scale 上界；
- SoftMax、BatchNorm 统计与大 reductions 的高精度建议属于实现经验，不是数学定理；
- 当前框架 AMP 的具体 allowlist/precision policy 需查对应版本文档。

## 视觉与文本核验

- 已抽取 PDF 并定位 FP16 范围、gradient histogram、loss scaling、FP32 主权重和大归约；
- 已渲染并目视检查 PDF 第 8–12 页，范围数据、直方图与动态 scaling 流程清晰。

## 生成节点

- [x] [[浮点数与舍入误差]]
- [x] [[习题 - 浮点数与舍入误差]]
