---
type: source
status: active
area: [sources, natural-distribution-shift, robustness]
source_type: paper
title: "Measuring Robustness to Natural Distribution Shifts in Image Classification"
author: [Rohan Taori, Achal Dave, Vaishaal Shankar, Nicholas Carlini, Benjamin Recht, Ludwig Schmidt]
year: 2020
url: "https://proceedings.neurips.cc/paper/2020/hash/d8330f857a17c53d217014ee776bfd50-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and benchmark conditions"
venue: "NeurIPS 2020"
scope_role: primary
temporal_role: benchmark-audit
related: ["[[OOD、鲁棒性与因果不变性的边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Measuring Robustness to Natural Distribution Shifts

> [!abstract] 来源定位
> 比较 ImageNet 分布内性能与多种自然变化下的 effective robustness，强调基线趋势和额外增益分账。本库调用其“绝对 OOD accuracy 与超出 ID trend 的 robustness 不同”视角。

## 本库调用

1. natural-shift benchmarks 与 source accuracy 配对；
2. raw accuracy gain 可由更强 ID model 解释；
3. effective robustness 依赖基线拟合与 benchmark；
4. synthetic robustness 不自动迁移到 natural shifts；
5. 单一视觉任务不能支持通用因果稳定性。
