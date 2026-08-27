---
type: source
status: verified
area: [sources, generative-models, flow-matching, cnf]
source_type: paper
title: "Flow Matching for Generative Modeling"
author: "Yaron Lipman; Ricky T. Q. Chen; Heli Ben-Hamu; Maximilian Nickel; Matt Le"
year: 2023
url: "https://arxiv.org/abs/2210.02747"
venue: "ICLR 2023"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: foundational
related: ["[[连续性方程、概率路径与 Flow Matching]]", "[[Conditional Flow Matching、Coupling 与最优传输路径]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Lipman et al.：Flow Matching

> [!abstract] 来源定位
> 论文把 Flow Matching 定义为对 fixed conditional probability paths 的向量场做 simulation-free regression，从而训练 Continuous Normalizing Flow。Gaussian conditional paths 包含 diffusion path，OT displacement interpolation 是另一类重要选择。

## 核心调用

- marginal vector field 可由 conditional vector fields 的后验加权平均得到；
- conditional FM loss 与不可直接采样的 marginal FM loss 在 population level 共享梯度/最优点；
- 训练无需沿 learned ODE 做内层数值积分，但生成仍需解 ODE；
- path choice 改变 regression target、曲率、solver 难度与有限模型表现。

## 边界

论文中的效率与样本质量是给定模型、数据、solver 和协议下的实验结果，不是所有 OT-style path 必然优于 diffusion path 的定理。所谓 “simulation-free” 限定训练目标构造，不意味着 sampling-free 或 zero-NFE。
