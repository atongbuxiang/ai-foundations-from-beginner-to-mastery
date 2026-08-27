---
type: exercise
status: draft
area: [learning-theory/posterior-predictive, ensembles, approximate-bayes]
topic: "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
related: ["[[解答 - Bayesian Posterior Predictive、Ensemble 与近似边界]]", "[[Conformal Prediction 与有限样本 Coverage]]"]
solution: "[[解答 - Bayesian Posterior Predictive、Ensemble 与近似边界]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - Bayesian Posterior Predictive、Ensemble 与近似边界

> [!abstract] 训练目标
> 能从 posterior predictive 积分到 mixture moments 与 Monte Carlo error，区分 MC dropout、SWAG、deep ensemble 的理论身份，并对相关性、错设、shift 与 compute 做完整审计。

## A. 识别与复述

### LT-BPP-A01

区分 parameter posterior、function distribution、posterior predictive 与 algorithm-induced ensemble；写出它们之间的映射。

### LT-BPP-A02

比较 exact posterior sampling、variational inference、MC dropout、SWAG、deep ensemble 与 bootstrap ensemble 的成员生成及主要 approximation boundary。

### LT-BPP-A03

为什么 parameter mean plug-in、平均 logits 与平均 probabilities 通常是三个不同预测器？

## B. 手算与局部推导

### LT-BPP-B01

三个等权 Gaussian members 的 $(\mu_m,\sigma_m^2)$ 为 $(0,1),(2,1),(4,4)$。计算 mixture mean、within、between 和 total variance。

### LT-BPP-B02

两个二分类成员 logits 为 $(\log9,0)$ 与 $(0,\log4)$。分别计算概率平均和 logit 平均后 softmax 的 $P(Y=1)$，验证二者不同。

### LT-BPP-B03

某 predictive quantity 的成员方差为 0.04。分别计算 $M=4,16$ 个 iid members 的 MC standard error；若 $M=16$ 且两两相关 $\rho=0.2$，计算平均方差和近似 $M_{\rm eff}$。

## C. 证明与反例

### LT-BPP-C01

用 Jensen 不等式证明 mixture 的逐样本 NLL 不超过成员 NLL 的平均；为什么不推出它优于最强成员？

### LT-BPP-C02

构造非线性模型，使 $E[f_\Theta(x)]\ne f_{E\Theta}(x)$；再构造 posterior mean parameter 位于两个 modes 之间且预测很差的例子。

### LT-BPP-C03

写出 MC error + posterior approximation + model misspecification 的误差分账，并证明增加 samples 只直接控制第一项。

## D. 审计与诊断

### LT-BPP-D01

论文称“10 次 test-time dropout 是 Bayesian posterior”。列出 dropout training、prior/regularization、mask、BatchNorm、samples 与 calibration 方面缺失的证据。

### LT-BPP-D02

设计 single model、MC dropout、SWAG 与 deep ensemble 的 compute-fair comparison：对齐哪些预算，报告哪些 strongest-member、diversity 与 uncertainty 指标？

### LT-BPP-D03

模型在 clean data 上 NLL 好，但随 shift severity 增强迅速过度自信。设计 accuracy/NLL/Brier/ECE/risk–coverage 曲线与 shift provenance 审计。

## E. 研究与迁移

### LT-BPP-E01

区分 LLM 的 weight ensemble、prompt ensemble、decoder sampling 与 self-consistency；为每种对象给出可允许和不可允许的 Bayesian 解释。

### LT-BPP-E02

为 scientific ML 分解 observation noise、parameter posterior、numerical discretization、surrogate error 与 PDE model-form error；说明 ensemble 能覆盖哪些、不能覆盖哪些。

### LT-BPP-E03

写一份 predictive-ensemble claim card：成员生成、概率组合、相关性、MC error、近似、shift、calibration、compute 与结论边界。
