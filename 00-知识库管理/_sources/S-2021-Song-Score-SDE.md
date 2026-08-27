---
type: source
status: verified
area: [sources, generative-models, score-based-models, sde]
source_type: paper
title: "Score-Based Generative Modeling through Stochastic Differential Equations"
author: "Yang Song; Jascha Sohl-Dickstein; Diederik P. Kingma; Abhishek Kumar; Stefano Ermon; Ben Poole"
year: 2021
url: "https://arxiv.org/abs/2011.13456"
venue: "ICLR 2021"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: foundational
related: ["[[Predictor–Corrector 与 Score-based 生成程序]]", "[[SDE、概率流 ODE 与 Flow Matching MOC]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Song et al.：Score-based SDE

> [!abstract] 来源定位
> 论文统一多噪声 score 模型与 diffusion probabilistic models，给出 reverse-time SDE、probability-flow ODE 与 predictor–corrector sampler。本卷只调用 PC 的误差分工；严格反向时间定理和 ODE likelihood 留到 50.7。

## 课程采用与限制

- predictor 数值推进 reverse SDE 的时间演化；
- corrector 在固定噪声层使用 score-based MCMC 调整当前 marginal；
- corrector 不是对未知真实误差的投影，有限步也不保证到达平稳；
- 同 marginal 的 exact theorem 不自动传到 learned score 与 discretized solver；
- 比较 sampler 时必须 compute-match：score evaluations、corrector steps、tolerance 与 wall time。

