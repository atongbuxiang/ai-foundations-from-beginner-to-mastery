---
type: source
status: verified
area: [sources, generative-models/vae, importance-sampling]
source_type: paper
title: "Importance Weighted Autoencoders"
author: [Yuri Burda, Roger Grosse, Ruslan Salakhutdinov]
year: 2015
url: "https://arxiv.org/abs/1509.00519"
accessed: 2026-08-25
source_tier: A
scope_role: core
temporal_role: classical
related: ["[[IWAE、重要性权重与推断缺口]]", "[[S-2021-Su-8791-VAE估计样本概率密度]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Burda、Grosse 与 Salakhutdinov：IWAE

> [!abstract] 来源定位
> IWAE 以 $K$ 个 importance weights 的 log-average 构造比单样本 ELBO 更紧的 log-evidence lower bound。它承担 bound 定义与原始经验；后续关于 inference-network gradient SNR、DReG 和评价 bias 需独立来源。

$$
\mathcal L_K(x)=E\left[\log\frac1K\sum_{k=1}^K
\frac{p_\theta(x,z_k)}{q_\phi(z_k\mid x)}\right]\le\log p_\theta(x).
$$

对同一 proposal，$\mathcal L_1\le\mathcal L_K$（标准 iid setting）且在相应矩条件下趋于 log evidence。更紧 bound 不保证有限样本 gradient 对 $\phi$ 更好，也不证明后验 family 真实包含 multimodal posterior。

