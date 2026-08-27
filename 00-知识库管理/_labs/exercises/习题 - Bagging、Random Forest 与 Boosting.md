---
type: exercise
status: draft
area: [learning-theory/ensembles, random-forests, boosting]
topic: "[[Bagging、Random Forest 与 Boosting]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[决策树、分裂准则与剪枝]]", "[[偏差—方差—噪声分解]]"]
related: ["[[解答 - Bagging、Random Forest 与 Boosting]]", "[[在线学习、Boosting 与序列预测 MOC]]"]
solution: "[[解答 - Bagging、Random Forest 与 Boosting]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - Bagging、Random Forest 与 Boosting

> [!abstract] 训练目标
> 能区分 bootstrap/feature/sequence randomness，推导 ensemble variance、OOB比例、AdaBoost与 functional gradient更新，并设计不复用 OOB/validation的 AI ensemble protocol。

## A. 识别与复述

### LT-ENS-A01

区分 ideal bagged predictor、finite-\(B\) bagging、infinite random forest与 repeated-dataset expectation；增加 \(B\) 分别改变什么？

### LT-ENS-A02

比较 bagging、random forest、AdaBoost与 gradient boosting的 member generation、并行性、aggregation与直接 objective。

### LT-ENS-A03

解释 OOB prediction为何避免 direct resubstitution，但不是可无限复用的 independent test set。

## B. 手算与数值判断

### LT-ENS-B01

bootstrap sample size \(n=100\)。计算某 observation未被抽中的精确概率 \((99/100)^{100}\) 的近似值、被至少抽中概率，并与 \(e^{-1}\) limit比较。

### LT-ENS-B02

base predictions各有 variance \(v=16\)，pairwise correlation \(\rho=0.2\)，成员数 \(B=25\)。求 ensemble variance及 \(B\to\infty\) floor。

### LT-ENS-B03

AdaBoost某轮 weighted error \(\varepsilon=0.2\)。求 \(\alpha\) 与 \(Z=2\sqrt{\varepsilon(1-\varepsilon)}\)；正确/错误样本未归一化 weights分别乘多少？

## C. 推导与证明

### LT-ENS-C01

用 law of total variance分解 data variance与 conditional bootstrap Monte Carlo variance；再证明 finite-\(B\) conditional variance按 \(1/B\) 下降。

### LT-ENS-C02

推导 exchangeable members的
$$
v[\rho+(1-\rho)/B]
$$
variance公式，并解释 correlation floor。

### LT-ENS-C03

从 AdaBoost stage objective推导 \(\alpha_m\)、weight update与 training exponential loss乘积；再说明 0–1 training error为何受它上界。

## D. 边界、反例与纠错

### LT-ENS-D01

反驳“bootstrap产生更多独立训练信息”。从 empirical distribution与 unique observation比例说明。

### LT-ENS-D02

反驳“random forest树数趋于无穷，所以 generalization error趋于零”。指出极限对象、bias、dataset uncertainty、shift与 selection。

### LT-ENS-D03

反驳“bagging只降 variance、boosting只降 bias”。给出至少四个会同时改变 bias/variance/target的机制。

## E. AI 迁移

### LT-ENS-E01

为同一用户有多条记录且带时间顺序的 random forest设计 OOB/outer evaluation。为什么普通 row bootstrap/OOB可能泄漏？

### LT-ENS-E02

设计 gradient-boosted reward model protocol：loss、pair sampling、depth、shrinkage、early stopping、calibration、prompt-group split与 policy-shift验收。

### LT-ENS-E03

为 forest/boosting生产系统写一份 ensemble报告，至少包含 randomness、tree count convergence、correlation、OOB reuse、proper scores、importance stability、latency与 shift。
