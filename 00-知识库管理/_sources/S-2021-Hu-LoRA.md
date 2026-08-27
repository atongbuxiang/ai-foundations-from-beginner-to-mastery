---
type: source
status: verified
area: [sources, peft, lora, low-rank]
source_type: paper
title: "LoRA: Low-Rank Adaptation of Large Language Models"
author: "Edward J. Hu et al."
year: 2021
url: "https://arxiv.org/abs/2106.09685"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: lora-definition
temporal_role: foundational-method
related: ["[[LoRA 的低秩更新、初始化、缩放与合并]]", "[[QLoRA、量化基座与适配显存总账]]"]
created: 2026-08-26
updated: 2026-08-26
---

# LoRA

> [!abstract] 来源定位
> LoRA 冻结预训练权重，并以低秩因子参数化选定线性层的增量。课程从矩阵形状、秩上界、参数量、初始化、缩放、梯度与 merge equivalence 重建方法，同时把原论文的模型/任务结果限制在其实验协议内。

低秩的是参数增量而非整个模型或函数；trainable parameter 少不等于激活、临时反量化、optimizer、通信和 wall time 按同倍数减少。

