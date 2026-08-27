---
type: source
status: active
area: [sources, uncertainty, entropy, mutual-information]
source_type: paper
title: "Quantifying Aleatoric and Epistemic Uncertainty in Machine Learning: Are Conditional Entropy and Mutual Information Appropriate Measures?"
author: [Lisa Wimmer, Yusuf Sale, Paul Hofman, Bernd Bischl, Eyke Hüllermeier]
year: 2023
url: "https://proceedings.mlr.press/v216/wimmer23a.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and critique conditions"
venue: "UAI 2023"
scope_role: primary
temporal_role: critical-audit
related: ["[[Aleatoric、Epistemic 与模型不确定性]]", "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Quantifying Aleatoric and Epistemic Uncertainty

> [!abstract] 来源定位
> 批判性检查用 expected conditional entropy 与 mutual information 量化 aleatoric/epistemic uncertainty 的常见做法。本库据此把熵分解定位为给定二阶分布/模型下的度量选择，而非普遍唯一的概念定义。

## 本库调用

1. predictive entropy 的代数分解不自动等于语义上唯一的 uncertainty 分解；
2. 度量应满足哪些单调性、极值与可解释性 desiderata；
3. 多分类分布与模型不一致会产生反直觉排序；
4. 单个 entropy/MI 数字不能替代 calibration、selective risk 与 shift test；
5. 报告必须说明 posterior/ensemble law 如何获得。
