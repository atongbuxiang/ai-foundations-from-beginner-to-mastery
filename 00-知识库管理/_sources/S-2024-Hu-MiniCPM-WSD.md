---
type: source
status: verified
area: [sources, optimization, learning-rate, wsd, language-modeling]
source_type: paper
title: "MiniCPM: Unveiling the Potential of Small Language Models with Scalable Training Strategies"
author: "Hu et al."
year: 2024
url: "https://arxiv.org/abs/2404.06395"
accessed: 2026-08-26
source_tier: A
scope_role: original-method-and-evidence
related: ["[[Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]", "[[训练时域、Restart、Schedule-Free 与末端学习率]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Hu 等：MiniCPM 与 Warmup–Stable–Decay

> [!abstract] 来源定位
> MiniCPM 把预训练学习率拆成 warmup、较长 stable 和末段 decay 三阶段，用 stable 主干支持持续训练与从不同 token horizon 分叉做 cooldown。课程采用 WSD 的时域合同与分支实验思想，不把特定 decay 比例写成普适常数。

## 课程采用

- 分别记录 warmup 终点 $T_w$、stable 终点 $T_s$、总 horizon $T$；
- stable checkpoint 可以作为多个预算的共同祖先，但不同 cooldown 分支仍是不同实验；
- decay 函数、最低 LR、token/step 口径和数据混合变化必须显式记录。

## 边界

WSD 的连续训练便利性不等于 horizon-free 的收敛定理，也不保证所有 optimizer/noise regime 都从 cooldown 获益。
