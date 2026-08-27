---
type: source
status: verified
area: [sources, ai-training, qat, integer-inference]
source_type: paper
title: "Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference"
author: "Benoit Jacob et al."
year: 2018
url: "https://openaccess.thecvf.com/content_cvpr_2018/html/Jacob_Quantization_and_Training_CVPR_2018_paper.html"
accessed: 2026-08-26
source_tier: A
license: "CVF open-access paper；知识库仅保存独立摘要与链接"
scope_role: qat
temporal_role: foundational
related: ["[[训练量化、优化器状态压缩与 QAT]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Quantization and Training for Integer-Arithmetic-Only Inference

> [!abstract] 来源定位
> 论文是 affine integer quantization 与 quantization-aware training 的经典来源，重点目标是训练后执行整数推理，而不是把训练本身全程变成整数算术。

## 可调用证据

- 实值用 scale 与 zero-point 映射到有限整数格点；
- fake quantization 在训练 forward 中模拟 clip/round/dequantize，backward 常用近似梯度；
- activation range 校准、饱和与 per-layer/per-channel 选择决定误差；
- 论文在当时移动端视觉模型上报告精度—延迟—内存权衡。

## 边界

- straight-through estimator 不是 round 的真实导数；
- QAT 的训练计算通常仍含浮点 master parameters/gradients；
- CVPR 2018 的 int8 CNN 结果不能直接外推到 LLM 低比特训练。
