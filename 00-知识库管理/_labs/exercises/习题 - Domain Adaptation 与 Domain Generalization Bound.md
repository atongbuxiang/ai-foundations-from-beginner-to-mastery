---
type: exercise
status: draft
area: [learning-theory/domain-adaptation, domain-generalization]
topic: "[[Domain Adaptation 与 Domain Generalization Bound]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Domain Adaptation 与 Domain Generalization Bound]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Domain Adaptation 与 Domain Generalization Bound
## A. 识别与复述
### LT-DA-A01
区分 unsupervised/semi-supervised DA、DG 与 test-time adaptation。
### LT-DA-A02
定义 $d_{\mathcal H\Delta\mathcal H}$ 与 $\lambda_{\mathcal H}$。
### LT-DA-A03
domain classifier error、proxy distance 与 target risk 有何不同？
## B. 手算与局部推导
### LT-DA-B01
若 $R_s=.10,d=.30,\lambda=.15$，计算经典 bound。
### LT-DA-B02
domain error $\epsilon=.1,.5$ 时计算 proxy A-distance。
### LT-DA-B03
写 DANN 三个模块和梯度方向。
## C. 证明与反例
### LT-DA-C01
用 disagreement triangle 完整证明 target-risk 三项 bound。
### LT-DA-C02
构造 input marginals 相同、label rules 相反的 source/target。
### LT-DA-C03
证明常数表示 domain invariant，但可使 label error 接近 base-rate error。
## D. 审计与诊断
### LT-DA-D01
DANN domain accuracy 50%、target accuracy 差。给出 $\lambda$、capacity、collapse 等诊断。
### LT-DA-D02
审计用 target validation 选 DG checkpoint 的泄漏。
### LT-DA-D03
设计 ERM/DANN/DG 的 architecture、pretraining、search 与 domain-balanced 公平比较。
## E. 研究与迁移
### LT-DA-E01
为多医院任务设计 source-domain、unseen target 与 worst-domain protocol。
### LT-DA-E02
分析 pseudo-label conditional alignment 的确认偏差。
### LT-DA-E03
写 adaptation/generalization claim card，明确不可观测 $\lambda$ 与 target-blind selection。
