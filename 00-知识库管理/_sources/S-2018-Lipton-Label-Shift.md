---
type: source
status: active
area: [sources, label-shift, distribution-shift]
source_type: paper
title: "Detecting and Correcting for Label Shift with Black Box Predictors"
author: [Zachary C. Lipton, Yu-Xiang Wang, Alexander J. Smola]
year: 2018
url: "https://proceedings.mlr.press/v80/lipton18a.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and invertibility conditions"
venue: "ICML 2018"
scope_role: primary
temporal_role: modern-method
related: ["[[Covariate、Label 与 Concept Shift]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Detecting and Correcting for Label Shift with Black Box Predictors

> [!abstract] 来源定位
> 在 $P_s(X\mid Y)=P_t(X\mid Y)$ 假设下，用黑盒预测器的混淆结构估计 target class priors 并重加权。本库调用其线性识别条件；不把 prediction-frequency change 无条件解释成 label shift。

## 本库调用

1. label shift 保持 class-conditionals；
2. target prediction frequencies、source confusion matrix 与 class weights 的线性关系；
3. confusion matrix 可逆/条件性是识别门槛；
4. classifier calibration 不是唯一要求，但 degeneracy 会破坏估计；
5. concept shift 下校正没有保证。
