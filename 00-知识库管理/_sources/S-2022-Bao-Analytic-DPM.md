---
type: source
status: verified
area: [sources, generative-models, diffusion, variance]
source_type: paper
title: "Analytic-DPM: an Analytic Estimate of the Optimal Reverse Variance in Diffusion Probabilistic Models"
author: "Fan Bao; Chongxuan Li; Jun Zhu; Bo Zhang"
year: 2022
url: "https://arxiv.org/abs/2201.06503"
venue: "ICLR 2022"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[反向均值、固定方差、学习方差与 Analytic-DPM]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Bao et al.：Analytic-DPM

> [!abstract] 来源定位
> 论文在指定 diffusion family 中把 optimal reverse variance 与 KL 写成 score 的解析形式，再用 pretrained score model 与 Monte Carlo 估计，提出 training-free inference 调整。课程把“解析形式”“score approximation”“Monte Carlo estimate”“clipping bounds”和最终实验分成五层。

论文报告的 20–80× speedup 属于其模型、步数和 evaluator 设置；“optimal”不指任意 covariance family、任意 mean error 或人类感知 metric。

