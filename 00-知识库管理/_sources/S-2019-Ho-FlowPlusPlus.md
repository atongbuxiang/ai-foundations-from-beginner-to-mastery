---
type: source
status: verified
area: [sources, generative-models, normalizing-flows, dequantization]
source_type: paper
title: "Flow++: Improving Flow-Based Generative Models with Variational Dequantization and Architecture Design"
author: "Jonathan Ho; Xi Chen; Aravind Srinivas; Yan Duan; Pieter Abbeel"
year: 2019
url: "https://arxiv.org/abs/1902.00275"
venue: "ICML 2019"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[Flow 的 Support、Dequantization、TARFLOW 与证据地图]]", "[[Neural Spline Flow 与单调可逆变换]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Ho et al.：Flow++

> [!abstract] 来源定位
> Flow++说明离散图像不能直接拿 continuous density 当 pmf，提出 variational dequantization，并改进 coupling transform 与 conditioning architecture。课程用 Jensen 推导离散 log-mass lower bound，区分 uniform dequantization 与 learned $q(u\mid x)$。

Continuous bits/dim 高低依赖 quantization、noise support、logit transform/Jacobian 和 variational bound；跨论文若预处理不同，likelihood 不可直接比较。

