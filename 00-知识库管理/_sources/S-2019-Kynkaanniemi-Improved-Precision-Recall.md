---
type: source
status: verified
area: [sources, generative-models, evaluation, precision-recall]
source_type: paper
title: "Improved Precision and Recall Metric for Assessing Generative Models"
author: "Tuomas Kynkäänniemi; Tero Karras; Samuli Laine; Jaakko Lehtinen; Timo Aila"
year: 2019
url: "https://arxiv.org/abs/1904.06991"
accessed: 2026-08-25
source_tier: A
scope_role: bridge
related: ["[[Likelihood、FID、KID、Precision–Recall 与人类评估]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Kynkäänniemi et al.：Improved Precision and Recall

> [!abstract] 来源定位
> 论文在预训练特征空间用 kNN 半径构造 real/generated manifold approximation，分别估计 fidelity 与 coverage。结果依赖 encoder、$k$、样本数、距离和预处理，不能只报“precision/recall”而省略方法名。
