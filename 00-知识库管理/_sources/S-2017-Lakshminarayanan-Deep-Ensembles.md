---
type: source
status: active
area: [sources, deep-ensembles, uncertainty, posterior-predictive]
source_type: paper
title: "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles"
author: [Balaji Lakshminarayanan, Alexander Pritzel, Charles Blundell]
year: 2017
url: "https://proceedings.neurips.cc/paper_files/paper/2017/hash/9ef2ed4b7fd2c810847ffa5fa85bce38-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and empirical conditions"
venue: "NeurIPS 2017"
scope_role: primary
temporal_role: modern-method
related: ["[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles

> [!abstract] 来源定位
> 用独立初始化、数据顺序和适当 scoring rule 训练多个网络，再平均预测分布以改善 predictive uncertainty 的经验基线。本库调用其方法合同；明确指出 ensemble members 一般不是某个已定义 posterior 的独立样本。

## 本库调用

1. 独立训练成员与概率空间平均；
2. regression mixture 的 within/between variance；
3. adversarial training 等扩展只按论文设定解释；
4. 成员相关性限制有效样本数；
5. ensemble diversity、Bayesian epistemic uncertainty 与 OOD detection 不应画等号。
