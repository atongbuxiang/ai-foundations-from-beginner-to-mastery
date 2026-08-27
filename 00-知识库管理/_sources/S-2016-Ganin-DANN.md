---
type: source
status: active
area: [sources, domain-adaptation, adversarial-representation]
source_type: paper
title: "Domain-Adversarial Training of Neural Networks"
author: [Yaroslav Ganin, Evgeniya Ustinova, Hana Ajakan, Pascal Germain, Hugo Larochelle, François Laviolette, Mario Marchand, Victor Lempitsky]
year: 2016
url: "https://jmlr.org/papers/v17/15-239.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and optimization conditions"
venue: "JMLR 17"
scope_role: primary
temporal_role: modern-method
related: ["[[Domain Adaptation 与 Domain Generalization Bound]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Domain-Adversarial Training of Neural Networks

> [!abstract] 来源定位
> 通过 gradient reversal 同时优化 source label prediction 与 domain confusion，学习经验上的 domain-invariant features。本库调用其 saddle objective 与协议；domain confusion 只控制所选 discriminator family，不证明 label sufficiency 或 causality。

## 本库调用

1. feature extractor、label head、domain head 三角色；
2. source labeled + target unlabeled protocol；
3. gradient reversal 的 min–max 方向；
4. domain classifier capacity 与 optimization 影响 discrepancy proxy；
5. invariance 和 target accuracy 必须分别评估。
