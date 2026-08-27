---
type: source
status: verified
area: [sources, generative-models, diffusion, numerical-ode]
source_type: paper
title: "DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps"
author: "Cheng Lu; Yuhao Zhou; Fan Bao; Jianfei Chen; Chongxuan Li; Jun Zhu"
year: 2022
url: "https://arxiv.org/abs/2206.00927"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
related: ["[[扩散 SDE、ODE Solver、步长与 NFE 总账]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Lu et al.：DPM-Solver

> [!abstract] 来源定位
> 原论文解析处理 diffusion ODE 的线性部分，把其余项写成指数加权积分，并构造专用高阶 solver。课程用它区分 black-box order 与 diffusion-structured order，并坚持以 NFE 而非“步数”统一成本。

收敛阶首先是对给定光滑 vector field 的数值结论；learned score error、端点奇异性、guidance 非线性和浮点误差需另记账。
