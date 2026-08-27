---
type: source
status: active
area: [sources, learning-theory, misspecification, quasi-mle]
source_type: paper
title: "Maximum Likelihood Estimation of Misspecified Models"
author: [Halbert White]
year: 1982
url: "https://doi.org/10.2307/1912526"
accessed: 2026-08-23
source_tier: A
license: "Econometrica article; retain citation and independent derivations"
venue: "Econometrica 50(1), 1–25"
scope_role: primary
temporal_role: classical-foundation
related: ["[[模型可辨识性、选择与 Misspecification]]", "[[最大似然估计与 MAP]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Maximum Likelihood Estimation of Misspecified Models

> [!abstract] 来源定位
> White 分析 true law不属于所声明 parametric family时的 quasi-MLE：estimator趋向 expected log-likelihood/KL projection，并需要 sandwich而非 information-equality covariance。本库用它建立“预测可用不等于模型真实”的正式边界。

## 本库调用

1. misspecified MLE目标是 pseudo-true/KL-projection parameter；
2. parameter-of-interest consistency不由 QMLE convergence自动保证；
3. Hessian与score outer product一般不再相等；
4. naive likelihood-based inference在错设下可能无效；
5. in-distribution projection optimality不保证 distribution shift下可靠。
