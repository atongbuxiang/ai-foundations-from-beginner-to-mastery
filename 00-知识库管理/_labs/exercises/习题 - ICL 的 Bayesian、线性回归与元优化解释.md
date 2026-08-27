---
type: exercise
status: verified
area: [language-models, in-context-learning, theory]
topic: "[[ICL 的 Bayesian、线性回归与元优化解释]]"
solution: "[[解答 - ICL 的 Bayesian、线性回归与元优化解释]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - ICL 的 Bayesian、线性回归与元优化解释

## A. 识别与复述

### LM35-A01
区分行为等价、表示等价与机制等价。

### LM35-A02
Bayesian、estimator 与 optimizer 三种解释分别位于什么抽象层？

### LM35-A03
为什么存在一个 Transformer 权重构造不等于训练必然找到它？

## B. 手算与构造

### LM35-B01
潜任务 $y=x+1$ 与 $y=x-1$ 先验各 1/2，观测 $(2,3)$；在无噪声和错误率 0.1 两种情形算后验。

### LM35-B02
对 $(1,2),(2,4)$ 的一维无截距回归计算 OLS，并预测 $x_*=3$。

### LM35-B03
从 $w_0=0$ 对平方损失做一步 GD，写出 query 预测的 kernel-sum 形式。

## C. 推导与证明

### LM35-C01
推导 latent-task posterior predictive。

### LM35-C02
推导 ridge estimator，并说明 $\lambda=0$ 时还需什么条件。

### LM35-C03
说明 Gaussian Bayesian linear model 的 posterior mean、ridge 与迭代优化可在不同层同时成立。

## D. 边界、反例与纠错

### LM35-D01
构造“某一点输出等于 OLS，但整体函数不是 OLS”的反例。

### LM35-D02
反驳“每层都等于一步梯度下降”。

### LM35-D03
审计一篇把线性 attention toy theorem 外推聊天模型的论证。

## E. AI 迁移

### LM35-E01
设计 prior shift、noise 与 condition number 的判别实验。

### LM35-E02
为一篇 ICL 理论论文填写模型族、任务类、训练分布、误差与量词清单。

### LM35-E03
设计行为、隐藏状态与因果干预三级证据链。

独立完成后查看[[解答 - ICL 的 Bayesian、线性回归与元优化解释]]。
