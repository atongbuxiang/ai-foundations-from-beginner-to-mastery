---
type: source
status: verified
source_type: paper
source_tier: A
title: "Addressing Representation Collapse in Vector Quantized Models with One Linear Layer"
author: "Yongxin Zhu et al."
year: 2024
url: "https://arxiv.org/abs/2411.02038"
accessed: 2026-08-25
area: [sources, ai/generative-models, optimization]
related: ["[[Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Zhu et al.：SimVQ

> [!abstract] 原始证据
> SimVQ 用共享可学习线性基底重参数化 code vectors，使梯度更新作用于 codebook 所张成的整体空间。论文在图像、音频和多种架构中报告 code utilization 与重构改善。

## 边界

- $QW$ 可在函数层合并，但 factorization 改变优化路径；“表达等价”与“训练等价”必须分开。
- 改善是经验结论；冻结/训练 $Q$、优化器、初始化与维度都属于方法合同。
