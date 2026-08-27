---
type: source
status: verified
area: [sources, generative-models, evaluation, kid, mmd]
source_type: paper
title: "Demystifying MMD GANs"
author: "Mikołaj Bińkowski; Danica J. Sutherland; Michael Arbel; Arthur Gretton"
year: 2018
url: "https://arxiv.org/abs/1801.01401"
venue: "ICLR 2018"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
related: ["[[Likelihood、FID、KID、Precision–Recall 与人类评估]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Bińkowski et al.：KID

> [!abstract] 来源定位
> 论文提出 Kernel Inception Distance，即在固定 Inception 特征与 polynomial kernel 上的 MMD，并可用 U-statistic 得到无偏 $\mathrm{MMD}^2$ estimator。无偏不等于低方差，也不消除特征与 kernel 选择偏差。
