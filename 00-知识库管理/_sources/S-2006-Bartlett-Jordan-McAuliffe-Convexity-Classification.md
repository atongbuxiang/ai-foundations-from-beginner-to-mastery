---
type: source
status: active
area: [sources, learning-theory, classification-calibration, surrogate-loss]
source_type: paper
title: "Convexity, Classification, and Risk Bounds"
author: [Peter L. Bartlett, Michael I. Jordan, Jon D. McAuliffe]
year: 2006
url: "https://doi.org/10.1198/016214505000000907"
accessed: 2026-08-23
source_tier: A
license: "JASA article; retain citation and independent derivations"
venue: "Journal of the American Statistical Association 101(473), 138–156"
scope_role: primary
temporal_role: classical-foundation
related: ["[[逻辑回归、复合损失与概率分类]]", "[[支持向量机、最大间隔与核方法]]", "[[Bayes 决策、Bayes 预测器与 Bayes 风险]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Convexity, Classification, and Risk Bounds

> [!abstract] 来源定位
> Bartlett、Jordan 与 McAuliffe 严格研究 convex surrogate excess risk 怎样控制 0–1 excess risk，并以 classification calibration 刻画最弱的一致性条件。它防止本库把“logistic loss 是 convex”误写成“训练 loss 下降就自动获得分类 risk guarantee”。

## 元数据与纳入

- DOI：[JASA](https://doi.org/10.1198/016214505000000907)；
- 可读全文：[课程托管 PDF](https://sites.stat.washington.edu/courses/stat527/s14/readings/Bartlett_etal_JASA_2006.pdf)；
- 正式引用：Bartlett, P. L., Jordan, M. I. & McAuliffe, J. D. (2006), *JASA* 101, 138–156；
- 证据角色：conditional surrogate risk、classification calibration 与 excess-risk comparison；
- 本库 logistic probability estimation 的 strict properness 另由 [[S-2010-Reid-Williamson-Composite-Binary-Losses]] 承担。

## 本库调用的断言

1. convexity 是 computation property，不单独保证 statistical calibration；
2. classification-calibrated surrogate 才能从 surrogate regret 控制 0–1 regret；
3. logistic loss 是重要 calibrated convex surrogate；
4. comparison function、noise assumptions 与 function-class estimation error必须分别声明。

