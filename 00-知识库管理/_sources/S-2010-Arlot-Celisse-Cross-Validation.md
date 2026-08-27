---
type: source
status: verified
area: [sources, learning-theory, cross-validation, model-selection]
source_type: survey-paper
title: "A survey of cross-validation procedures for model selection"
author: [Sylvain Arlot, Alain Celisse]
year: 2010
url: "https://doi.org/10.1214/09-SS054"
accessed: 2026-08-23
source_tier: A
license: "Statistics Surveys article; retain citation, independent explanations, and official DOI/PDF"
venue: "Statistics Surveys 4, 40–79"
scope_role: primary-survey
temporal_role: classical-foundation
related: ["[[正则化、交叉验证与模型选择]]", "[[训练集、验证集、测试集与自适应复用]]", "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]"]
created: 2026-08-23
updated: 2026-08-26
---

# A survey of cross-validation procedures for model selection

> [!abstract] 来源定位
> Arlot 与 Celisse 系统区分 CV 作为 risk estimator 与 model-selection procedure，并强调 prediction/estimation 与 identification 目标、training fraction、bias/variance 和 problem-dependent failure。它是本库避免“十折交叉验证永远正确”口号化的正式来源。

## 元数据与纳入

- 正式 DOI：[10.1214/09-SS054](https://doi.org/10.1214/09-SS054)；
- 官方全文：[Project Euclid PDF](https://projecteuclid.org/journals/statistics-surveys/volume-4/issue-none/A-survey-of-cross-validation-procedures-for-model-selection/10.1214/09-SS054.pdf)；
- 正式引用：Arlot, S. & Celisse, A. (2010), *Statistics Surveys* 4, 40–79；
- 证据角色：hold-out、leave-\(p\)-out、\(V\)-fold、risk estimation、selection、training-size bias 与 variance；
- 边界：nested CV、adaptive agents 与 grouped/time data 在正文中结合现代 evaluation protocol 独立审计。

## 本库调用的断言

1. CV 的基本对象是 statistical algorithm，而不只是一个固定 fitted model；
2. validation independence 避免 resubstitution optimism，但 fold estimates 彼此相关；
3. training-set fraction 改变 CV 所估计的 procedure risk；
4. model identification 与 best prediction 不是同一个 selection goal；
5. CV procedure 的选择依赖 problem structure，不存在无条件最优的 fold 数。
