---
type: exercise
status: draft
area: [learning-theory/masked-prediction, teacher-student, self-supervision]
topic: "[[遮蔽预测、Teacher–Student 与自监督目标]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[遮蔽预测、Teacher–Student 与自监督目标]]"]
related: ["[[解答 - 遮蔽预测、Teacher–Student 与自监督目标]]", "[[Linear Probe、Fine-Tuning 与迁移评估]]"]
solution: "[[解答 - 遮蔽预测、Teacher–Student 与自监督目标]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 遮蔽预测、Teacher–Student 与自监督目标

> [!abstract] 训练目标
> 能写 corruption–target 合同，推导 log/square loss 的 conditional estimand，比较 MLM/MAE/Mean Teacher/BYOL/DINO，并审计 target drift、leakage、confirmation 与 pretext–downstream gap。

## A. 识别与复述

### LT-TGT-A01

写出 clean $X$、mask $M$、corrupted input $\widetilde X$、target $T$、student $q_\theta$ 与 pretext population risk。哪些变量必须注明 stop-gradient？

### LT-TGT-A02

比较 raw token、pixel、latent、discrete code、cluster assignment 与 teacher distribution 六类 targets 的 loss geometry 与主要失败。

### LT-TGT-A03

区分 Mean Teacher、BYOL 与 DINO 的 teacher target、parameter update、temperature/centering 及 labeled-loss 使用方式。

## B. 手算与局部推导

### LT-TGT-B01

从 cross-entropy = entropy + KL 推导 masked discrete target 的最优预测是 $P(T\mid V)$。若 model class 受限，剩余 gap 怎样解释？

### LT-TGT-B02

推导平方损失下 $a^*(V)=E[T\mid V]$。若 $T\mid V$ 以 $1/2$ 概率取 $-1,+1$，求最优预测与最小风险，并解释“模糊重建”。

### LT-TGT-B03

$\xi_{t+1}=0.9\xi_t+0.1\theta_{t+1}$，$\xi_0=0$，$\theta_1=1,\theta_2=2,\theta_3=4$。计算 $\xi_1,\xi_2,\xi_3$，并写成历史权重和。

## C. 证明与反例

### LT-TGT-C01

证明 only-masked token loss 的 population estimand 依赖 mask law $Q(M\mid X)$；构造 content-dependent masking 使其过度加权稀有 token。

### LT-TGT-C02

构造一个 decoder 足够强、encoder 表示近乎常数但 reconstruction loss 仍较低的 toy data；说明 decoder capacity 为什么必须进入 MAE audit。

### LT-TGT-C03

构造 teacher 与 student 共同预测错误 pseudo-label 且 consistency loss 为 0 的例子；列出能打破 self-confirmation 的独立信号。

## D. 审计与诊断

### LT-TGT-D01

审计一个 BERT-style MLM：mask rate、80/10/10 replacement、loss positions、tokenizer、special-token mismatch、data split 和 evaluation 分别需记录什么？

### LT-TGT-D02

比较图像 MAE 在 mask ratio 25%、75%、95% 下的 visible compute、conditional ambiguity、local shortcut 与 downstream expectation。设计公平 ablation。

### LT-TGT-D03

DINO 训练出现所有样本都预测同一 prototype。分别从 teacher temperature、centering、EMA lag、multi-crop、batch statistics 与 implementation order 诊断。

## E. 研究与迁移

### LT-TGT-E01

为多变量时间序列设计 masked self-supervision；明确不得使用的未来信息、mask pattern、target distribution、missingness mechanism 与 downstream forecasting protocol。

### LT-TGT-E02

设计 token target、pixel target 与 teacher-latent target 的三路对照研究。如何在相同 encoder compute 下隔离 target geometry，而不让 decoder 参数量成为混杂？

### LT-TGT-E03

给出一份自监督事故报告模板，覆盖 target leakage、teacher drift、collapse、pretext–downstream disagreement、checkpoint selection 与 rollback evidence。

