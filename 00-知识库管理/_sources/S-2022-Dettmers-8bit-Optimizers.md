---
type: source
status: verified
area: [sources, ai-training, optimizer-state, quantization]
source_type: paper
title: "8-bit Optimizers via Block-wise Quantization"
author: "Tim Dettmers, Mike Lewis, Sam Shleifer, Luke Zettlemoyer"
year: 2022
url: "https://arxiv.org/abs/2110.02861"
accessed: 2026-08-26
source_tier: A
license: "arXiv / ICLR paper；知识库仅保存独立摘要与链接"
scope_role: optimizer-state-compression
temporal_role: active-method
related: ["[[训练量化、优化器状态压缩与 QAT]]", "[[ZeRO、FSDP、激活重计算与 Offload]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 8-bit Optimizers via Block-wise Quantization

> [!abstract] 来源定位
> 论文把量化对象从权重/激活扩展到有状态优化器的统计量，并用 block-wise dynamic quantization 处理跨张量异常值与尺度不均。

## 可调用证据

- Adam 类状态常占每参数两个 FP32 数，是内存账的重要部分；
- per-tensor 单一 scale 会被异常值支配，block-wise scale 改善局部利用率；
- 论文还组合动态非线性量化和稳定 embedding 处理特定故障；
- 在论文列明的语言、视觉与翻译任务上报告接近 32-bit optimizer 的结果。

## 边界

- “8-bit optimizer”不是把更新计算的所有对象都改成 int8；
- 方法效果绑定 block size、映射、解量化与异常值策略；
- 内存下降不自动等于 wall-time 加速，quantize/dequantize kernel 与带宽需实测。
