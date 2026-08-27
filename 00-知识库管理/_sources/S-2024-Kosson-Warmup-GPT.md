---
type: source
status: verified
area: [sources, optimization, warmup, language-modeling]
source_type: paper
title: "Analyzing and Reducing the Need for Learning Rate Warmup in GPT Training"
author: "Kosson, Messmer and Jaggi"
year: 2024
url: "https://arxiv.org/abs/2410.23922"
accessed: 2026-08-26
source_tier: A
scope_role: optimizer-update-study
related: ["[[Warmup、早期曲率与优化器状态建立]]", "[[学习率、局部损失变化与相对更新尺度]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Kosson 等：GPT Warmup 与早期更新尺度

> [!abstract] 来源定位
> 论文从 AdamW/Lion 的早期更新过大出发，同时检查参数二范数、方向角、表示变化与 critical batch，并通过显式归一化更新来减少 warmup。它为“更新尺度机制”提供直接实验，不证明其他机制无效。

## 课程采用

- 把 $\Delta W_t=\eta_t U_t$ 分解为方向、标量 LR 与参数/表示相对尺度；
- 记录早期角更新和表示扰动，而非只画全局 gradient norm；
- 把减少或消除 warmup 限定在论文所测试的小型 GPT、优化器变体和预算内。
