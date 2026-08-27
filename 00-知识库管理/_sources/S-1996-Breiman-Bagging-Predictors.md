---
type: source
status: active
area: [sources, learning-theory, bagging, ensembles]
source_type: paper
title: "Bagging Predictors"
author: [Leo Breiman]
year: 1996
url: "https://doi.org/10.1007/BF00058655"
accessed: 2026-08-23
source_tier: A
license: "Machine Learning journal article; author-hosted PDF available, retain citation"
venue: "Machine Learning 24(2), 123–140"
scope_role: primary
temporal_role: classical-foundation
related: ["[[Bagging、Random Forest 与 Boosting]]", "[[决策树、分裂准则与剪枝]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Bagging Predictors

> [!abstract] 来源定位
> Breiman 以 bootstrap replicates 生成多个 training sets，并对由同一 learning method 得到的 predictors 做回归平均或分类投票。论文强调 base procedure 的 instability 是 bagging 获益的重要条件。

## 元数据与纳入

- 正式 DOI：[Springer](https://doi.org/10.1007/BF00058655)；
- 作者托管：[Berkeley PDF](https://www.stat.berkeley.edu/~breiman/bagging.pdf)；
- 正式引用：Breiman, L. (1996), *Machine Learning* 24(2), 123–140；
- 证据角色：bootstrap aggregation、regression average/class plurality 与 instability；
- 边界：bagging 不保证每个 base learner 或每个 distribution 都改善，OOB evaluation 另需数据结构与复用审计。

## 本库调用的断言

1. bagging 对 bootstrap-trained predictors 做 conditional Monte Carlo averaging；
2. unstable predictors 更可能从 aggregation 获益；
3. regression averaging 与 classification voting不是同一代数损失分解；
4. bootstrap Monte Carlo randomness 消失不等于 sampling/generalization error 消失。
