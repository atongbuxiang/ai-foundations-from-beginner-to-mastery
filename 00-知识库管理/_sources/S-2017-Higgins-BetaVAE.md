---
type: source
status: verified
area: [sources, generative-models/vae, representation-learning]
source_type: paper
title: "beta-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework"
author: [Irina Higgins, Loic Matthey, Arka Pal, Christopher Burgess, Xavier Glorot, Matthew Botvinick, Shakir Mohamed, Alexander Lerchner]
year: 2017
url: "https://openreview.net/forum?id=Sy2fzU9gl"
accessed: 2026-08-25
source_tier: A
scope_role: core
temporal_role: classical
related: ["[[Posterior Collapse、率失真与解码器容量]]", "[[VAE 的条件、聚类、解耦主张与证据地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Higgins et al.：β-VAE

> [!abstract] 来源定位
> β-VAE 在 reconstruction 与 prior-KL 之间引入权重 $\beta$，研究 capacity/independence pressure 与可解释因素。它承担方法定义和原始实验；$\beta>1$ 时目标通常不再是原模型的标准 ELBO，且无监督语义解耦不由 factorized prior 单独保证。

课程把 $\beta$ 写成 rate–distortion Lagrange weight，独立评估 reconstruction、rate、aggregate mismatch、total correlation、下游 usefulness 与随机 seed。

