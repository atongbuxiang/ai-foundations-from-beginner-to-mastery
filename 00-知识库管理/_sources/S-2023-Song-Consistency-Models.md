---
type: source
status: verified
area: [sources, generative-models, consistency-models]
source_type: paper
title: "Consistency Models"
author: "Yang Song; Prafulla Dhariwal; Mark Chen; Ilya Sutskever"
year: 2023
url: "https://arxiv.org/abs/2303.01469"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
related: ["[[扩散蒸馏、一致性模型与 Shortcut]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Song et al.：Consistency Models

> [!abstract] 来源定位
> 原论文定义沿同一 probability-flow ODE trajectory 输出一致的模型，支持一步生成、多步改善和 zero-shot editing；既可蒸馏预训练 diffusion，也可独立训练。

课程把 boundary condition、trajectory consistency、teacher/EMA 程序和 sampling algorithm 分开。训练对上的相邻时间一致性不等于全域 exact flow map。
