---
type: exercise
status: draft
area: [learning-theory/calibration, proper-scoring-rules, reliability]
topic: "[[概率校准、Proper Scoring Rule 与可靠性图]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[概率校准、Proper Scoring Rule 与可靠性图]]"]
related: ["[[解答 - 概率校准、Proper Scoring Rule 与可靠性图]]", "[[Aleatoric、Epistemic 与模型不确定性]]"]
solution: "[[解答 - 概率校准、Proper Scoring Rule 与可靠性图]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 概率校准、Proper Scoring Rule 与可靠性图

> [!abstract] 训练目标
> 从条件频率定义出发，能推导 proper loss、Brier 分解与成本阈值，审计可靠性图/ECE/temperature scaling，并把概率质量限制到正确的数据与 shift 量词。

## A. 识别与复述

### LT-CAL-A01

分别写出 binary、strong multiclass、classwise 与 top-label calibration；说明已知的蕴含方向。

### LT-CAL-A02

区分 accuracy、discrimination、calibration、sharpness/resolution 与 decision utility；各给一个典型评价量。

### LT-CAL-A03

定义 proper 与 strictly proper loss。为什么“用严格 proper loss 训练”不等于有限样本模型已经校准？

## B. 手算与局部推导

### LT-CAL-B01

真实二分类概率为 $p=0.8$，比较报告 $q=0.8$ 与 $q=0.6$ 的 expected log loss 和 binary Brier loss，计算两种 regret。

### LT-CAL-B02

两个 equal-mass bins：第一 bin 有 50 个样本、平均 confidence 0.2、accuracy 0.1；第二 bin 有 50 个样本、confidence 0.8、accuracy 0.9。计算 $L_1$ ECE；说明把两 bin 合并会发生什么。

### LT-CAL-B03

假阳性成本为 2，假阴性成本为 8。推导 Bayes decision threshold，并判断 $q=0.15,0.25$ 时的最优行动。

## C. 证明与反例

### LT-CAL-C01

证明 multiclass log loss regret 等于 $D_{\mathrm{KL}}(p\Vert q)$，Brier regret 等于 $\|p-q\|_2^2$。

### LT-CAL-C02

构造一个 top-label calibrated 但不是 classwise/strong calibrated 的三分类预测器；逐项验证。

### LT-CAL-C03

从条件期望正交性推导 binary Brier 的 reliability–resolution–uncertainty 分解，并解释常数 base-rate predictor 的三项。

## D. 审计与诊断

### LT-CAL-D01

一篇论文只报“ECE=1.7%”。列出至少八项必须补充的 estimator/protocol 信息。

### LT-CAL-D02

团队在 test set 上从 20 个 temperatures、5 个 checkpoints 与 4 种 binning 中选最小 ECE。指出估计污染，并画出正确的 train–calibration–selection–locked-test 数据流。

### LT-CAL-D03

模型在 source 上 top-label calibrated，部署后 class prevalence 与医院构成改变。设计 calibration drift 监控，说明哪些 source 结论不能外推。

## E. 研究与迁移

### LT-CAL-E01

为 LLM 的“答案正确概率”定义 event、confidence extractor、calibration unit、proper score、reliability plot 与 abstention utility；说明 token probability 为什么不足。

### LT-CAL-E02

为高风险二分类器设计同时报告 NLL、Brier、classwise/group reliability、risk–coverage 和 cost curve 的实验；规定数据隔离与不确定性。

### LT-CAL-E03

写一份 probability-quality claim card：允许的最强结论、必要证据、shift 限制，以及必须拒绝的三类过度声明。
