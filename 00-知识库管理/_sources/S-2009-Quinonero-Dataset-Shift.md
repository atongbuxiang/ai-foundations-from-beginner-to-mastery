---
type: source
status: verified
area: [sources, dataset-shift, taxonomy]
source_type: book
title: "Dataset Shift in Machine Learning"
author: [Joaquín Quiñonero-Candela, Masashi Sugiyama, Anton Schwaighofer, Neil D. Lawrence]
year: 2009
url: "https://mitpress.mit.edu/9780262170055/dataset-shift-in-machine-learning/"
accessed: 2026-08-26
source_tier: A
license: "Scholarly book; retain citation and quotation limits"
venue: "MIT Press"
scope_role: synthesis
temporal_role: foundational
related: ["[[Covariate、Label 与 Concept Shift]]", "[[重要性加权与 Covariate Shift 校正]]"]
created: 2026-08-23
updated: 2026-08-26
---

# Dataset Shift in Machine Learning

> [!abstract] 来源定位
> 系统整理 train/test 分布不一致、sample selection、covariate shift 与相应校正。本库调用 joint-law factorization 与 shift taxonomy；不把未观测 target labels 下不可检验的条件稳定性当作已验证事实。

## 本库调用

1. source/target joint laws 分层；
2. covariate、prior/label 与 concept change 的区别；
3. sample-selection mechanism 与 support overlap；
4. diagnosis、correction、evaluation 必须分开；
5. shift types 可重叠，taxonomy 不是互斥标签器。
