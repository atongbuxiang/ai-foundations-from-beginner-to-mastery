---
type: source
status: active
area: [sources, learning-theory, adaboost, online-learning]
source_type: paper
title: "A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting"
author: [Yoav Freund, Robert E. Schapire]
year: 1997
url: "https://doi.org/10.1006/jcss.1997.1504"
accessed: 2026-08-23
source_tier: A
license: "Journal of Computer and System Sciences article; retain citation and independent derivations"
venue: "JCSS 55(1), 119–139"
scope_role: primary
temporal_role: classical-foundation
related: ["[[Bagging、Random Forest 与 Boosting]]", "[[在线学习、Boosting 与序列预测 MOC]]"]
created: 2026-08-23
updated: 2026-08-23
---

# A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting

> [!abstract] 来源定位
> Freund 与 Schapire 从 repeated decision/weight update 构造 AdaBoost，把 weak learner、example weights、weighted error 与 additive vote 连接起来。它是本库 AdaBoost 更新、指数损失与后续 online-learning 接口的原始来源。

## 元数据与纳入

- 正式 DOI：[Elsevier](https://doi.org/10.1006/jcss.1997.1504)；
- 正式引用：Freund, Y. & Schapire, R. E. (1997), *JCSS* 55(1), 119–139；
- 证据角色：decision-theoretic online update、weak-to-strong boosting 与 weighted voting；
- 边界：margin explanation、noise robustness、probability calibration 与 gradient-boosting general loss 不由同一基础定理承担。

## 本库调用的断言

1. AdaBoost 逐轮提高当前误分类 examples 的 relative weight；
2. base-classifier coefficient由 weighted error 决定；
3. final classifier是 additive weighted vote；
4. weak-learning condition、training error bound 与 deployment risk 必须分层。
