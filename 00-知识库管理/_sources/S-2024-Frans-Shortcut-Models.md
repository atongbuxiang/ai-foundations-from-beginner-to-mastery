---
type: source
status: verified
area: [sources, generative-models, flow-matching, shortcut]
source_type: paper
title: "One Step Diffusion via Shortcut Models"
author: "Kevin Frans; Danijar Hafner; Sergey Levine; Pieter Abbeel"
year: 2024
url: "https://arxiv.org/abs/2410.12557"
accessed: 2026-08-25
source_tier: A
scope_role: frontier
related: ["[[扩散蒸馏、一致性模型与 Shortcut]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Frans et al.：Shortcut Models

> [!abstract] 来源定位
> 原论文以单网络、单训练阶段学习 time-and-step-conditioned update，训练不同步数预算并支持一步/多步推断。它承担 Shortcut 的一级算法和实验来源。

课程把 dyadic self-consistency 看作有限步 map 的训练约束，而不是连续 ODE 的自动存在唯一性或 exact semigroup 证明。
