---
type: source
status: active
area: [sources, learning-theory, pac-bayes]
source_type: paper
title: "Some PAC-Bayesian Theorems"
author: [David A. McAllester]
year: 1999
url: "https://doi.org/10.1023/A:1007618624809"
accessed: 2026-08-23
source_tier: A
license: "Springer article; retain citation and independent derivations"
venue: "Machine Learning 37(3), 355–363"
scope_role: primary
temporal_role: classical-foundation
related: ["[[PAC-Bayes Bound 的测度变换主线]]", "[[PAC-Bayes 先验、后验与数据依赖边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Some PAC-Bayesian Theorems

> [!abstract] 来源定位
> McAllester 的早期 PAC-Bayes 论文把任意先验测度、训练后选择的随机化预测分布与高概率泛化保证连接起来。它为“用 posterior 相对 prior 的 KL，而不是仅用整个 hypothesis class 的最坏容量”提供了经典起点。

## 元数据与纳入

- 正式记录与 DOI：[Springer DOI](https://doi.org/10.1023/A:1007618624809)；
- 正式引用：McAllester, D. A. (1999), *Machine Learning* 37, 355–363；
- 证据角色：PAC-Bayesian guarantee 的历史与概念骨架；
- 本库的 Bernoulli-KL 常数与完整推导主要按 [[S-2002-Seeger-PAC-Bayesian-Generalization]] 校准。

## 本库调用的断言

1. PAC-Bayes 允许 hypothesis space 与 prior 是一般测度对象；
2. probability statement 对训练样本成立，而 conclusion 可同时覆盖一族 data-dependent posteriors；
3. complexity 由 posterior 相对 prior 的 KL 与 confidence term 构成；
4. prior 是学习前归纳偏置，不是训练后把中心移到答案附近的免费旋钮；
5. posterior 是为证书选择的随机化预测分布，不要求等于 Bayesian posterior。

## 版权与常数边界

不复制原文证明或图。正文从测度变换、二项型矩界与联合凸性独立推导；不同 PAC-Bayes theorem 的常数、loss 条件和 inverse-kl 形式不可互换。

