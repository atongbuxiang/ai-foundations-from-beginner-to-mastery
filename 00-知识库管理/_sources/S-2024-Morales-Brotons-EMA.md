---
type: source
status: verified
area: [sources, optimization, averaging, ema]
source_type: paper
title: "Exponential Moving Average of Weights in Deep Learning: Dynamics and Benefits"
author: "Morales-Brotons, Vogels and Hendrikx"
year: 2024
url: "https://arxiv.org/abs/2411.18704"
accessed: 2026-08-26
source_tier: A
scope_role: systematic-empirical-study
related: ["[[参数 EMA、SWA 与 Checkpoint Averaging]]", "[[Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Morales-Brotons 等：权重 EMA 的动力学与收益

> [!abstract] 来源定位
> 论文系统研究权重 EMA 的训练动力学、调参、早期表现、噪声平滑与泛化/鲁棒/校准/迁移。课程采用其实证分层，EMA 的收益仍限定在实验协议内。

## 课程采用

$$
\bar\theta_t=\beta\bar\theta_{t-1}+(1-\beta)\theta_t.
$$

必须说明初始化与 bias correction、step-based $\beta$、update/sample/token 时钟、评估使用 raw 还是 EMA 权重，以及 BN/其他运行统计的处理。EMA 降低轨迹噪声不等于恢复 Bayesian posterior mean。
