---
type: source
status: verified
area: [sources, peft, quantization, qlora]
source_type: paper
title: "QLoRA: Efficient Finetuning of Quantized LLMs"
author: "Tim Dettmers et al."
year: 2023
url: "https://arxiv.org/abs/2305.14314"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: qlora-definition
temporal_role: foundational-method
related: ["[[QLoRA、量化基座与适配显存总账]]", "[[LoRA 的低秩更新、初始化、缩放与合并]]"]
created: 2026-08-26
updated: 2026-08-26
---

# QLoRA

> [!abstract] 来源定位
> QLoRA 让梯度穿过冻结的 4-bit quantized base，更新 LoRA adapters，并提出 NF4、double quantization 与 paged optimizers。课程据此拆开存储 dtype、计算 dtype、量化 metadata、adapter/optimizer、activation 与峰值临时内存。

“4-bit”不等于总训练显存为全量微调的四分之一，也不等于权重在 4-bit 中被更新；质量与显存主张绑定 kernel、group size、compute dtype、rank、sequence length 和硬件。

