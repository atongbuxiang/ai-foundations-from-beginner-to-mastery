---
type: source
status: verified
area: [sources, ai-training, fp8]
source_type: paper
title: "FP8 Formats for Deep Learning"
author: "Paulius Micikevicius et al."
year: 2022
url: "https://arxiv.org/abs/2209.05433"
accessed: 2026-08-26
source_tier: A
license: "arXiv paper；知识库仅保存独立摘要、格式比较与链接"
scope_role: format-evidence
temporal_role: active-standardization
related: ["[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]", "[[Loss Scaling、Master Weight 与低精度梯度累积]]"]
created: 2026-08-26
updated: 2026-08-26
---

# FP8 Formats for Deep Learning

> [!abstract] 来源定位
> 论文提出 E4M3 与 E5M2 两类 FP8 编码，并以不同 range/precision 角色支持训练和推理。它是本卷讨论 FP8 不可只写“8 bit float”的主要原始来源。

## 可调用证据

- E4M3 以较多 fraction bits换较小 range，E5M2 以更多 exponent bits换更大 range；
- 两种编码对 Inf/NaN 的保留方式不完全相同；
- 实际训练依赖 per-tensor/history scaling、较高精度 accumulation 和按张量选择格式；
- 论文在 CNN、RNN、Transformer 与最高 175B 语言模型设置中报告与 16-bit baseline 接近的结果。

## 边界

- 论文中的格式/scale recipe 不等于任意硬件当前 FP8 实现；
- 相同 bit-width 不等于相同编码、舍入、饱和或 kernel；
- 经验匹配不证明每个张量都可安全降到 FP8。
