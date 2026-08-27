---
type: source
status: active
area: [sources, contrastive-learning, false-negatives, negative-sampling]
source_type: paper
title: "Debiased Contrastive Learning"
author: [Ching-Yao Chuang, Joshua Robinson, Yen-Chen Lin, Antonio Torralba, Stefanie Jegelka]
year: 2020
url: "https://papers.nips.cc/paper/2020/hash/63c3ddcc7b23daa1e42dc41f9a44a873-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "NeurIPS 2020"
scope_role: primary
temporal_role: modern-method
related: ["[[正负样本、Batch 依赖与梯度估计]]", "[[对比学习、InfoNCE 与密度比]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Debiased Contrastive Learning

> [!abstract] 来源定位
> 指出 unlabeled marginal negatives 可包含 same-semantic-class false negatives，并在 class-prior assumptions 下构造 debiasing objective。本库用它说明 negative 不是天然真负例，correction 也依赖额外模型。

## 本库调用

1. marginal negative 可混合 true negatives 与 same-class collisions；
2. collision probability 随 latent class prior 与 batch 构成变化；
3. false negatives 改变 objective target 而非只增加 noise；
4. debiasing 需要 class-prior 或 latent-class 假设；
5. group、time duplicates 与 near positives 要在 sampler 层审计；
