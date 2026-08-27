---
type: source
status: active
area: [sources, uncertainty, heteroscedasticity, bayesian-deep-learning]
source_type: paper
title: "What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?"
author: [Alex Kendall, Yarin Gal]
year: 2017
url: "https://proceedings.neurips.cc/paper_files/paper/2017/hash/2650d6089a6d640c5e85b2b88265dc2b-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and model conditions"
venue: "NeurIPS 2017"
scope_role: primary
temporal_role: modern-method
related: ["[[Aleatoric、Epistemic 与模型不确定性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?

> [!abstract] 来源定位
> 在视觉任务中结合输入依赖的 observation-noise model 与近似 Bayesian parameter uncertainty。本库调用 heteroscedastic likelihood 和实验接口；不把论文中的工程分解提升为模型无关、唯一或完全可辨识的真值分解。

## 本库调用

1. regression 中预测均值与输入依赖方差；
2. Gaussian NLL 对残差与 log-variance 的权衡；
3. parameter samples 对 predictive spread 的贡献；
4. dense prediction 中按像素/任务建模 uncertainty；
5. 似然错设、校准与 OOD 仍需独立评估。
