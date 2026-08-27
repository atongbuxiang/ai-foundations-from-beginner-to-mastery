---
type: source
status: verified
area: [sources, generative-models/vae, variational-inference]
source_type: paper
title: "Auto-Encoding Variational Bayes"
author: [Diederik P. Kingma, Max Welling]
year: 2013
url: "https://arxiv.org/abs/1312.6114"
accessed: 2026-08-25
source_tier: A
scope_role: core
temporal_role: classical
related: ["[[VAE 的 ELBO、变分后验与重参数化梯度]]", "[[Gaussian VAE 的闭式 KL、解码似然与尺度合同]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Kingma 与 Welling：Auto-Encoding Variational Bayes

> [!abstract] 来源定位
> AEVB 定义了面向连续 per-datapoint latent 的可扩展 stochastic variational learning：用 recognition model amortize posterior inference，并通过 reparameterized ELBO estimator 使用标准随机梯度。它承担 VAE 方法定义与历史优先证据；现代架构、collapse 诊断和图像质量不由原文单独代表。

## 核心调用

$$
\mathcal L(x)=E_{q_\phi(z\mid x)}\log p_\theta(x\mid z)
-D_{KL}(q_\phi(z\mid x)\Vert p(z)),
$$

以及 $z=g_\phi(x,\varepsilon)$ 的 pathwise estimator。课程保留微分—期望交换、Monte Carlo 方差、likelihood scale 与 amortization gap 条件。

