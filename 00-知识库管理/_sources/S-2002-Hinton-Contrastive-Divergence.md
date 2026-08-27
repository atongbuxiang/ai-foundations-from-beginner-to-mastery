---
type: source
status: verified
area: [sources, generative-models, energy-based-models, mcmc]
source_type: paper
title: "Training Products of Experts by Minimizing Contrastive Divergence"
author: "Geoffrey E. Hinton"
year: 2002
url: "https://www.cs.utoronto.ca/~hinton/absps/tr00-004.html"
venue: "Neural Computation 14(8)"
accessed: 2026-08-25
source_tier: A
license: "作者公开页面；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: foundational
related: ["[[最大似然的正相负相、对比散度与噪声对比估计]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Hinton：Contrastive Divergence

> [!abstract] 来源定位
> CD 用从数据初始化的短链分布替代难采样的模型分布，降低每次更新成本。课程把它写成带 sampler-dependent bias 的梯度 surrogate，而不把 CD-$k$ 当成 exact MLE。

## 三层不能混同

$$
\nabla KL(p_*\|p_\theta),
\qquad
KL(p_*\|p_\theta)-KL(p_k\|p_\theta),
\qquad
E_{p_*}\nabla E_\theta-E_{p_k}\nabla E_\theta.
$$

更新时若忽略 $p_k$ 对 $\theta$ 的依赖，最后一式通常不是上方差值的完整梯度。$k\to\infty$、链遍历并充分混合时才期待模型相逼近；persistent CD 改变初始化/偏差结构，但也不自动消除误差。

