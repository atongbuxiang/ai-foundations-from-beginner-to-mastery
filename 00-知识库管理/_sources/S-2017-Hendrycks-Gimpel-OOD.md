---
type: source
status: active
area: [sources, ood-detection, confidence]
source_type: paper
title: "A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks"
author: [Dan Hendrycks, Kevin Gimpel]
year: 2017
url: "https://openreview.net/forum?id=Hkg4TI9xl"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and benchmark conditions"
venue: "ICLR 2017"
scope_role: primary
temporal_role: foundational-baseline
related: ["[[OOD、鲁棒性与因果不变性的边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# A Baseline for Detecting Misclassified and OOD Examples

> [!abstract] 来源定位
> 用 maximum softmax probability 建立误分类/OOD detection 的简单基线。本库调用其 score-ranking protocol；softmax confidence 不是 density、causal distance 或任意 out-distribution 下的统一 detector。

## 本库调用

1. detection score 与 classifier prediction 分层；
2. in/out benchmark pair 明确定义；
3. AUROC/AUPR 与 threshold metrics；
4. misclassification detection 与 OOD detection 不同；
5. baseline failure 不能由单一平均曲线概括。
