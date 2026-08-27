---
type: exercise
status: draft
area: [generative-models, vae, variational-inference]
topic: "[[VAE 的 ELBO、变分后验与重参数化梯度]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - VAE 的 ELBO、变分后验与重参数化梯度]]"
created: 2026-08-25
updated: 2026-08-25
---

# 习题 - VAE 的 ELBO、变分后验与重参数化梯度

## A. 识别与复述

### GEN11-A01
写出 ELBO 的 joint-ratio 形式、reconstruction–KL 形式与 evidence decomposition。

### GEN11-A02
Jensen 推导需要什么 support 条件？何时取等？

### GEN11-A03
区分 score-function gradient 与 pathwise gradient 的适用条件。

## B. 手算与建模

### GEN11-B01
使用 GEN10-B01 的离散模型并取 $q(z=1\mid x=1)=0.5$，计算 ELBO、exact log evidence 与 gap。

### GEN11-B02
$z=\mu+\sigma\epsilon,f(z)=z^2$。在 $\mu=1,\sigma=2,\epsilon=-0.5$ 时求单样本 pathwise 梯度。

### GEN11-B03
给定两次 log likelihood 为 $-2,-4$，KL 为 $0.7$，计算 $L=2$ Monte Carlo ELBO 与 negative ELBO。

## C. 推导与证明

### GEN11-C01
从 Jensen 逐步推导 ELBO，并写清等号条件。

### GEN11-C02
从 posterior KL 推导 $\log p_\theta(x)=\mathcal L+\mathrm{KL}(q\|p_\theta(z\mid x))$。

### GEN11-C03
证明 $z=\mu+\sigma\epsilon$ 对 $f(z)=z^2$ 的 pathwise 梯度在期望下等于解析梯度。

## D. 边界、反例与纠错

### GEN11-D01
给出 $\mathbb E\log p(x\mid Z)\ne\log p(x\mid\mathbb EZ)$ 的数值反例。

### GEN11-D02
反驳“ELBO 上升必然意味着测试 likelihood 与样本质量都上升”。

### GEN11-D03
构造 proposal 漏掉 posterior support 导致 importance/ELBO 诊断失真的例子。

## E. AI 迁移

### GEN11-E01
从一段伪代码中列出 encoder、reparameterization、decoder、analytic KL 和 reduction 的最小审计字段。

### GEN11-E02
为离散 token latent 比较枚举、Gumbel relaxation 与 score-function 三种梯度方案。

### GEN11-E03
设计实验分别验证训练路径、likelihood 评价路径与无条件生成路径没有被混用。

## 解答入口

[[解答 - VAE 的 ELBO、变分后验与重参数化梯度]]

