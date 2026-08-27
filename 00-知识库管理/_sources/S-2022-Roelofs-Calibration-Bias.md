---
type: source
status: active
area: [sources, calibration, estimator-bias]
source_type: paper
title: "Mitigating Bias in Calibration Error Estimation"
author: [Rebecca Roelofs, Nicholas Cain, Jonathon Shlens, Michael C. Mozer]
year: 2022
url: "https://proceedings.mlr.press/v151/roelofs22a.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and estimator conditions"
venue: "AISTATS 2022"
scope_role: primary
temporal_role: estimator-audit
related: ["[[概率校准、Proper Scoring Rule 与可靠性图]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Mitigating Bias in Calibration Error Estimation

> [!abstract] 来源定位
> 分析 calibration error 估计中的有限样本偏差，并讨论 debiasing 与自适应分箱。本库调用其估计器审计视角；不把任何单个修正估计器写成无条件 ground truth。

## 本库调用

1. calibration error 是 population object，样本 ECE 是随机估计量；
2. 分箱内准确率与置信度差的绝对值会引入有限样本偏差；
3. binning scheme 与样本数应进入报告合同；
4. 比较模型时应固定评估器并报告不确定性；
5. calibration estimator 自身也需模拟或重复抽样验证。
