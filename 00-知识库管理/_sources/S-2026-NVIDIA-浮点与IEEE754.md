---
type: source
status: verified
area: [sources, gpu-systems, math/numerical-analysis]
source_type: official-documentation
title: "Floating Point and IEEE 754"
author: NVIDIA
year: 2026
url: "https://docs.nvidia.com/cuda/pdf/Floating_Point_on_NVIDIA_GPU.pdf"
accessed: 2026-08-15
source_tier: B
license: "NVIDIA 官方文档；知识库仅保存独立摘要、实验映射与链接"
scope_role: implementation
temporal_role: current
aliases: [NVIDIA-2026-Floating-Point]
related: ["[[浮点数与舍入误差]]", "[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
created: 2026-08-15
updated: 2026-08-15
---

# NVIDIA：Floating Point and IEEE 754

> [!abstract] 来源定位
> 当前 CUDA 官方浮点指南。它承担 GPU 上格式字段、舍入模式、FMA、点积运算树、编译选项和 CPU/GPU 比较的实现事实，不承担通用数值稳定性定义。

## 核心映射

| 文档主题 | 本章用途 |
|---|---|
| format fields | sign/exponent/fraction 的实现图 |
| operations and accuracy | 不同括号可产生不同合法结果 |
| FMA | $\operatorname{RN}(ab+c)$ 只有一次舍入 |
| dot product | serial、FMA、parallel 三种运算树 |
| rounding modes | rn/rz/ru/rd 的 CUDA 对应 |
| compiler flags | FMA contraction、FTZ 与精确除法/平方根边界 |

## 视觉与文本核验

- 已抽取全文并定位 formats、operations、FMA、dot product、rounding modes 与 compiler flags；
- 已渲染并目视检查 PDF 第 5–14 页，字段图、FMA 示例和点积树图清晰；
- 旧硬件举例不写入稳定理论；当前实现事实优先引用在线 Programming Guide。

## 生成节点

- [x] [[浮点数与舍入误差]]
