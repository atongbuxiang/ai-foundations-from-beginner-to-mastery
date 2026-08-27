---
type: exercise
status: draft
area: [generative-models, vae, importance-sampling]
topic: "[[IWAE、重要性权重与推断缺口]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - IWAE、重要性权重与推断缺口]]"
created: 2026-08-25
updated: 2026-08-25
---

# 习题 - IWAE、重要性权重与推断缺口

## A. 识别与复述

### GEN13-A01
定义 importance weight、无偏 density estimator 与 IWAE bound。

### GEN13-A02
为什么 density estimator 无偏不推出 log estimator 无偏？

### GEN13-A03
定义 model、family、amortization、optimization/MC 四类 gap。

## B. 手算与建模

### GEN13-B01
weights 为 $(.1,.4,.7,.8)$，求 $\widehat p_4$、log estimate 与 ESS。

### GEN13-B02
离散 $q=(.5,.5)$、joint masses $(.15,.35)$，求 exact evidence、两种 weight 与 $K=1$ ELBO。

### GEN13-B03
某 estimator 的 weight mean 为 $.2$、variance 为 $.01$。用 delta method 估计 $K=100$ 的 log bias。

## C. 推导与证明

### GEN13-C01
证明 $\widehat p_K$ 无偏且 $\mathcal L_K\le\log p(x)$。

### GEN13-C02
证明 exact posterior proposal 使所有 importance weights 为 $p(x)$。

### GEN13-C03
推导 normalized importance estimator，并说明它为何一般有限样本有偏但一致。

## D. 边界、反例与纠错

### GEN13-D01
构造单次 $\log\widehat p_{K+1}<\log\widehat p_K$ 的样本序列。

### GEN13-D02
反驳“增大 K 使 bound 更紧，所以同预算训练一定更好”。

### GEN13-D03
给出 ESS 较高但 proposal 仍漏掉一个 posterior mode 的反例。

## E. AI 迁移

### GEN13-E01
设计 VAE test likelihood 报告协议，包含 K、重复、稳定计算、ESS 与置信区间。

### GEN13-E02
设计 fixed-$\theta$ 的局部 variational refinement 以估计 amortization gap。

### GEN13-E03
对一个论文“更好的 encoder 改善生成模型”的声明设计 family、optimization 与 parameter-budget 对照。

## 解答入口

[[解答 - IWAE、重要性权重与推断缺口]]

