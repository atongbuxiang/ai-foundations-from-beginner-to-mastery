---
type: exercise
status: draft
area: [learning-theory/conformal-prediction, coverage, exchangeability]
topic: "[[Conformal Prediction 与有限样本 Coverage]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Conformal Prediction 与有限样本 Coverage]]"]
related: ["[[解答 - Conformal Prediction 与有限样本 Coverage]]", "[[Covariate、Label 与 Concept Shift]]"]
solution: "[[解答 - Conformal Prediction 与有限样本 Coverage]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - Conformal Prediction 与有限样本 Coverage

> [!abstract] 训练目标
> 能从 untouched calibration scores 与 exchangeable rank 推出有限样本 marginal coverage，正确构造 regression/classification sets，并审计 conditional claim、reuse、dependence、shift 与 efficiency。

## A. 识别与复述

### LT-CFM-A01

定义 nonconformity score、calibration quantile、prediction set 与 coverage event；说明 score quality 和 rank validity 的分工。

### LT-CFM-A02

区分 marginal、pointwise conditional、group/class-conditional 与 simultaneous coverage；各写出概率量词。

### LT-CFM-A03

exchangeability 与 i.i.d. 有何关系？列出时间、患者、多视图与反馈系统中可能破坏 exchangeability 的单位错误。

## B. 手算与局部推导

### LT-CFM-B01

给定 $m=9,\alpha=0.2$ 和 scores
$$
(0.1,0.2,0.2,0.4,0.5,0.7,0.8,1.0,1.6),
$$
求正确索引和 threshold；若 point prediction 为 3.2，写 prediction interval。

### LT-CFM-B02

给定 $m=4,\alpha=0.1$，求 $k$ 并解释为什么 threshold 为 $+\infty$；这说明小 calibration set 有什么分辨率限制？

### LT-CFM-B03

CQR 在某点给初始区间 $[4,7]$，calibration conformal quantile 为 $0.8$；写最终区间。再对标签 $y=3.5,5,8.2$ 计算 nonconformity score。

## C. 证明与反例

### LT-CFM-C01

在无 ties 情形用 exchangeable rank 完整证明 split-conformal marginal coverage；再说明保守 ties 处理为什么不降低 coverage。

### LT-CFM-C02

构造两个群组：总体 90% coverage，但小群组只有 50% coverage；验证总体数字并说明为何不违反 marginal theorem。

### LT-CFM-C03

解释用 calibration labels 试 100 个 scores 后挑最短集合为什么破坏基础证明；给出额外 tuning split 的修复数据流。

## D. 审计与诊断

### LT-CFM-D01

医疗数据中每位患者有多次检查。设计 patient-level train/calibration/test split、bootstrap unit、group coverage 与 interval-length 报告。

### LT-CFM-D02

某方法 coverage 99.9% 但分类集合平均含 99/100 类。评价该方法，并设计 coverage–efficiency、empty/full-set 与 subgroup 指标。

### LT-CFM-D03

审计一个声称“distribution-free under any deployment shift”的 conformal 系统：指出 rank proof 断裂处，并区分 covariate、label、concept 与 temporal shift。

## E. 研究与迁移

### LT-CFM-E01

为 20 类分类器设计 simple score 与 APS 两种 conformal sets；规定 ties、randomization、calibration size、set-size 与 classwise coverage。

### LT-CFM-E02

为时间序列预测区分 one-step marginal interval 与 whole-trajectory simultaneous tube；提出依赖结构、rolling calibration 和 safety 层的额外要求。

### LT-CFM-E03

写一份 conformal claim card：exchangeable unit、split、score、quantile convention、coverage 量词、efficiency、shift/reuse 限制和允许的最强结论。
