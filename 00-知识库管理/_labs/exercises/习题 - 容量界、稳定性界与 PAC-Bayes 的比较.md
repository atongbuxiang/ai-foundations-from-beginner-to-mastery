---
type: exercise
status: draft
area: [learning-theory/generalization-certificates, comparison]
topic: "[[容量界、稳定性界与 PAC-Bayes 的比较]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[算法稳定性与替换一个样本]]", "[[样本压缩方案与泛化]]", "[[PAC-Bayes Bound 的测度变换主线]]", "[[互信息与信息论泛化界]]"]
related: ["[[解答 - 容量界、稳定性界与 PAC-Bayes 的比较]]", "[[神经网络容量与 Norm-Based Bound]]"]
solution: "[[解答 - 容量界、稳定性界与 PAC-Bayes 的比较]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 容量界、稳定性界与 PAC-Bayes 的比较

> [!abstract] 训练目标
> 能在共同对象合同下比较容量、稳定性、压缩、PAC-Bayes 与 mutual information，完成证书选型、置信预算与失败模式审计。

## A. 识别与复述

### LT-CERT-A01

为五类 bounds 各写出 complexity object、典型量词与直接保证类型。

### LT-CERT-A02

解释 logical validity、nonvacuity、tightness 与 explanatory adequacy 的区别。

### LT-CERT-A03

为什么比较两个 numerical bounds 前必须统一 sample unit、loss、output predictor、randomness 与 confidence？

## B. 手算与数值判断

### LT-CERT-B01

\(|\mathcal H|=1024\)。分别写出 finite-class \(\log|\mathcal H|\)、uniform-prior point-posterior KL、10-bit output 的 MI upper bound；说明数值相同为何 guarantee 不同。

### LT-CERT-B02

有四个预声明 certificates，总失败预算 \(\delta=0.04\)。等分预算后每个 \(\delta_j\) 是多少？若某 bound 的 confidence term 是 \(\log(1/\delta_j)\)，相对单独使用 \(\delta=0.04\) 多付多少 nats？

### LT-CERT-B03

某 stable algorithm 有 \(\widehat R_S=0.35\)、expected gap bound \(0.01\)。能推出怎样的 expected population risk statement？为什么不能说 risk 小于 \(0.01\)？

## C. 推导与证明

### LT-CERT-C01

证明
$$
\mathbb E_S\operatorname{KL}(P_{W\mid S}\|P)
=I(S;W)+\operatorname{KL}(P_W\|P).
$$

### LT-CERT-C02

证明：若 \(J\) 个 certificate events 的 failure budgets 满足 \(\sum_j\delta_j\le\delta\)，则可以合法 post-hoc 取最小 \(B_j(S,\delta_j)\)。

### LT-CERT-C03

对可数 \(\mathcal H\) 与 prior \(P(h)\)，从 PAC-Bayes point posterior 推出 weighted description penalty \(\log(1/P(h))\)，并比较 weighted union bound。

## D. 边界、反例与纠错

### LT-CERT-D01

给出 stable but high-risk algorithm；说明 generalization gap certificate 与 learning guarantee 的差别。

### LT-CERT-D02

给出 low-MI-on-average but worst-case-unstable algorithm 的构造思路；说明 average dependence 与 adjacency sensitivity 不可互换。

### LT-CERT-D03

反驳：“VC bound vacuous，所以 VC theory 被深度学习证伪。”要求区分 theorem validity、chosen class 与 explanatory scope。

## E. AI 迁移

### LT-CERT-E01

为以下四个系统选首选 certificate 并说明备选：regularized logistic regression、quantized tree、stochastic neural ensemble、adaptive hyperparameter agent。

### LT-CERT-E02

设计一个 multi-certificate benchmark report，至少包含十个共同字段和置信预算规则。

### LT-CERT-E03

对一个 overparameterized deterministic transformer，提出容量、稳定性、压缩、PAC-Bayes、MI 五条可证伪研究问题；不得只写“计算一个 bound”。

