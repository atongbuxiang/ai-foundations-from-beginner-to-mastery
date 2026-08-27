---
type: source
status: verified
area: [sources, generative-models/vae, information-theory]
source_type: paper
title: "InfoVAE: Information Maximizing Variational Autoencoders"
author: [Shengjia Zhao, Jiaming Song, Stefano Ermon]
year: 2017
url: "https://arxiv.org/abs/1706.02262"
accessed: 2026-08-25
source_tier: A
scope_role: supporting
temporal_role: classical
related: ["[[Posterior Collapse、率失真与解码器容量]]", "[[VAE 的条件、聚类、解耦主张与证据地图]]", "[[S-2018-Su-6088-VAE最小化先验与最大化互信息]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Zhao、Song 与 Ermon：InfoVAE

> [!abstract] 来源定位
> InfoVAE 重新加权 mutual-information 与 aggregate-posterior matching 项，缓解 latent 被忽略并统一若干 autoencoder objectives。课程用它区分 per-example KL、$I_q(X;Z)$ 与 $D(q(z)\Vert p(z))$；新 objective 不应含混地称为原始 ELBO。

关键恒等式：

$$
E_{p_*(x)}D_{KL}(q(z\mid x)\Vert p(z))
=I_q(X;Z)+D_{KL}(q(z)\Vert p(z)).
$$

MMD/adversarial aggregate matching 的 estimator、kernel/critic 与 finite-batch bias 需另行审计。

