---
type: exercise
status: draft
area: [learning-theory/contrastive-learning, infonce, mutual-information]
topic: "[[对比学习、InfoNCE 与密度比]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[对比学习、InfoNCE 与密度比]]"]
related: ["[[解答 - 对比学习、InfoNCE 与密度比]]", "[[正负样本、Batch 依赖与梯度估计]]"]
solution: "[[解答 - 对比学习、InfoNCE 与密度比]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 对比学习、InfoNCE 与密度比

> [!abstract] 训练目标
> 能从candidate-index experiment推导Bayes density ratio、InfoNCE cross-entropy与MI lower bound，区分NCE/InfoNCE，并审计log-K ceiling、critic gaps和negative-law shift。

## A. 识别与复述

### LT-NCE-A01

完整写出K-candidate experiment与population InfoNCE loss。

### LT-NCE-A02

区分original NCE、InfoNCE、negative sampling与contrastive divergence的experiment和estimand。

### LT-NCE-A03

列出candidate risk、ratio identification、MI bound、finite estimate与downstream utility五层claim。

## B. 手算与数值判断

### LT-NCE-B01

给三个candidate logits$(2,1,0)$且第一项为positive，计算softmax probability、loss与$\log3-L$。

### LT-NCE-B02

若$K=256$，InfoNCE lower bound最高多少nats与bits？若要certify 20 nats，K至少多大？

### LT-NCE-B03

令$X=Y$为uniform binary。计算true MI；解释$K=2$ ceiling与negative collision。

## C. 推导与证明

### LT-NCE-C01

从candidate likelihood推导$P(I=i\mid x,y_{1:K})\propto p(y_i\mid x)/p_Y(y_i)$。

### LT-NCE-C02

证明cross-entropy给$\log K-L\le I(I;X,Y_{1:K})$，再说明到$I(X;Y)$需要哪一步。

### LT-NCE-C03

证明invertible $f,g$ 下MI不变，并解释为何这阻止MI单独刻画disentanglement。

## D. 边界、反例与纠错

### LT-NCE-D01

反驳“InfoNCE loss是无偏MI estimator”，列出至少四个gap。

### LT-NCE-D02

negative改从hard proposal $q(y\mid x)$抽样后，optimal ratio是什么？为什么不能继续机械引用MI ratio？

### LT-NCE-D03

构造高view MI但downstream task无用的identity/augmentation-seed shortcut。

## E. AI 迁移

### LT-NCE-E01

为image–text contrastive pretraining写positive/negative law、critic、temperature、batch与outer retrieval协议。

### LT-NCE-E02

设计受控Gaussian实验比较true MI、InfoNCE bound、critic capacity、K与finite-sample bias。

### LT-NCE-E03

写一份MI claim audit：support、units、nats/bits、ceiling、confidence、adaptive reuse与downstream evidence。

