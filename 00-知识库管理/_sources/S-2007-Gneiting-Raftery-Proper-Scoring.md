---
type: source
status: verified
area: [sources, calibration, proper-scoring-rules]
source_type: paper
title: "Strictly Proper Scoring Rules, Prediction, and Estimation"
author: [Tilmann Gneiting, Adrian E. Raftery]
year: 2007
url: "https://doi.org/10.1198/016214506000001437"
accessed: 2026-08-23
source_tier: A
license: "Scholarly source; retain citation and quotation limits"
venue: "Journal of the American Statistical Association"
scope_role: primary
temporal_role: foundational
related: ["[[概率校准、Proper Scoring Rule 与可靠性图]]"]
created: 2026-08-23
updated: 2026-08-26
---

# Strictly Proper Scoring Rules, Prediction, and Estimation

> [!abstract] 来源定位
> 系统化 proper/strictly proper scoring rule、entropy、divergence 与预测分布估计之间的关系。本库用它证明“诚实报告真实条件分布”是总体风险最优性质；不把有限样本分数或单一分箱图等同于完整校准。

## 本库调用

1. proper 与 strictly proper 的定义及方向约定；
2. 期望 score 的 regret 可写为非负 divergence；
3. log score 与 Brier score 的总体最优性；
4. sharpness、calibration 与 forecast evaluation 的分工；
5. scoring rule 的选择仍编码用户关心的预测分布性质。
