---
type: source
status: draft
area: [sources, scientific-spaces, ai/transformers, ai/residual-routing]
source_type: blog
title: "Attention Residuals 回忆录"
author: 苏剑林
year: 2026
url: "https://spaces.ac.cn/archives/11664"
accessed: 2026-08-24
source_tier: C
license: "科学空间；仅保存独立摘要、短公式与链接"
scope_role: frontier-bridge
temporal_role: current-research
related: ["[[Transformer Block、残差、归一化与 FFN]]", "[[Transformer 表达、稳定性与证据边界]]", "[[S-2026-Chen-Attention-Residuals]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Attention Residuals 回忆录

> [!abstract] 来源定位
> 文章从 Pre/Post-Norm、Hyper-Connections 与 mHC 的演化背景，回顾 AttnRes 从“让层选择历史表示”到 Block AttnRes、缓存式流水通信和两阶段计算的设计过程。课程采用其问题意识与设计取舍；模型效果、规模曲线和系统开销回查原论文与代码。

## 课程采用

- 固定 residual sum 可被看作深度方向的固定聚合；
- full depth attention 会引入 $O(L^2)$ 层对与历史激活存储问题；
- block summary 是降低 memory/communication 的结构折中；
- 设计回忆说明方案演化，不等于每个机制解释已被严格隔离证明；
- 2026 年材料仍处快速演化期，调用时记录版本、模型、训练 token 与实现。

## 与正式来源分工

[[S-2026-Chen-Attention-Residuals]]承担方法、实验与系统声明；本卡只承担中文设计脉络。后续工作对低秩 depth keys 等扩展不并入原方法结论。
