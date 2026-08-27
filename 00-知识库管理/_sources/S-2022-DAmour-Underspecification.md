---
type: source
status: verified
area: [sources, machine-learning, underspecification, robustness]
source_type: paper
title: "Underspecification Presents Challenges for Credibility in Modern Machine Learning"
author: "D'Amour et al."
year: 2022
url: "https://www.jmlr.org/papers/v23/20-1335.html"
accessed: 2026-08-26
source_tier: A
venue: JMLR
scope_role: primary-evidence
related: ["[[数据优化器调度交互、混杂与归因边界]]", "[[随机种子、配对比较、置信区间与序贯决策]]"]
created: 2026-08-26
updated: 2026-08-26
---

# D'Amour 等：Underspecification

> [!abstract] 来源定位
> 当训练目标和开发集允许许多同等可接受的模型时，不同 pipeline/seed 产生的预测器可能在部署相关行为上显著不同。

## 本卷调用

- 把 seed variance 解释为算法分布的一部分，而非一律视为可删除噪声；
- 除主 metric 外，测量 stress tests、subgroups、calibration 与 failure tails；
- checkpoint/seed selection 只在预先声明的可观测标准上进行。

## 边界

underspecification 说明等验证分数不能保证等行为，但不证明任意差异都具有实际重要性；需预注册 deployment estimand。
