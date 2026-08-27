---
type: source
status: verified
area: [sources, ai-training, bfloat16]
source_type: paper
title: "A Study of BFLOAT16 for Deep Learning Training"
author: "Dhiraj Kalamkar et al."
year: 2019
url: "https://arxiv.org/abs/1905.12322"
accessed: 2026-08-26
source_tier: A
license: "arXiv paper；知识库仅保存独立摘要与链接"
scope_role: format-evidence
temporal_role: foundational
related: ["[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]", "[[Loss Scaling、Master Weight 与低精度梯度累积]]"]
created: 2026-08-26
updated: 2026-08-26
---

# A Study of BFLOAT16 for Deep Learning Training

> [!abstract] 来源定位
> 论文系统比较 BF16 的范围与训练行为：它保留与 FP32 相同数量的 exponent bits、减少 fraction bits，从而把“range”和“precision”两类风险清楚分开。

## 可调用证据

- BF16 的动态范围接近 FP32，通常比 FP16 少依赖 loss scaling；
- 更少 fraction bits 意味着相对舍入误差更大，累加/统计仍常需 FP32；
- 转换舍入模式、特殊值和硬件实现是数值合同的一部分；
- 论文在图像、语音、语言模型、生成模型和推荐系统上给出当时的训练对照。

## 边界

- “无需改超参”是论文实验范围内的观察，不是所有模型的保证；
- 相同 exponent range 不等于相同精度或逐比特轨迹；
- 今天的 autocast、flush-to-zero 与 accumulation policy 应以具体设备/框架为准。
