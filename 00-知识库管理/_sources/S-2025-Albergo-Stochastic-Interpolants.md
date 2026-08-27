---
type: source
status: verified
area: [sources, generative-models, stochastic-interpolants, flows, diffusions]
source_type: paper
title: "Stochastic Interpolants: A Unifying Framework for Flows and Diffusions"
author: "Michael Albergo; Nicholas M. Boffi; Eric Vanden-Eijnden"
year: 2025
url: "https://www.jmlr.org/papers/v26/23-1605.html"
venue: "Journal of Machine Learning Research 26(209):1–80"
accessed: 2026-08-25
source_tier: A
license: "JMLR 页面；本库仅保存独立摘要、必要公式与链接"
scope_role: unifying
temporal_role: active-research
related: ["[[Diffusion、Flow、速度参数化与统一证据地图]]", "[[连续性方程、概率路径与 Flow Matching]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Albergo et al.：Stochastic Interpolants

> [!abstract] 来源定位
> 论文以带附加 latent 的 stochastic interpolant 在有限时间连接任意两端密度，并证明其密度既满足 transport equation，也满足一族带可调 diffusion 的 forward/backward Fokker–Planck equations。这为 flow 与 diffusion 提供了明确但有条件的统一框架。

## 课程调用

- 同一 interpolant density path 可对应 deterministic probability flow，也可对应不同噪声强度的 SDE；
- velocity/score 可由平方回归目标表征；
- 调节 diffusion 并不意味着 path law 相同，只是密度演化被配平；
- likelihood control 对 stochastic 与 deterministic dynamics 的条件不同。

本卷只把它用作 GEN-56 的现代统一坐标系，不以“统一”抹平 FM、score diffusion、Rectified Flow 在路径、目标、coupling 和 finite solver 上的差异。
