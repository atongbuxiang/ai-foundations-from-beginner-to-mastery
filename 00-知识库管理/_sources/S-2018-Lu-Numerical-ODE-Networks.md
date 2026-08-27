---
type: source
status: draft
area: [sources, neural-networks/residual-stability, neural-ode]
source_type: paper
title: "Beyond Finite Layer Neural Networks: Bridging Deep Architectures and Numerical Differential Equations"
author: "Yiping Lu; Aoxiao Zhong; Quanzheng Li; Bin Dong"
year: 2018
url: "https://proceedings.mlr.press/v80/lu18d.html"
venue: "ICML 2018"
accessed: 2026-08-23
source_tier: A
license: "PMLR open-access paper；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[ResNet 的 ODE 与离散动力系统视角]]", "[[Euler、Runge-Kutta 与离散化误差]]", "[[残差缩放、Lipschitz 界与深度稳定性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Lu et al.：深网与数值微分方程

> [!abstract] 来源定位
> 论文系统连接深层架构与 ODE 数值离散，并据多步法设计网络。它承担 ResNet–Euler 类比的原始研究来源；一致性、收敛阶与稳定域仍由数值分析条件补严。

## 核心对应

显式 Euler

$$
x_{k+1}=x_k+h f(x_k,t_k)
$$

与带显式 step scale 的 residual block 同形。不同架构可对应不同离散模板，但“公式同形”不自动证明某个已训练有限深网络收敛到固定 ODE。

## 断言表

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| ODE-C1 | ResNet 可解释为 Euler-like update | 结构类比 | state shape、时间索引和 branch scale需定义 | 成立 |
| ODE-C2 | 任意 ResNet 都是某个固定 ODE 的收敛离散 | 极限命题 | 需 $h\to0$、一致参数族、正则与稳定性 | 不能无条件采用 |
| ODE-C3 | 数值方法知识可指导架构设计 | 方法论 | 离散模板与学习目标仍需实验 | 有价值但非性能定理 |
| ODE-C4 | 高阶离散名字必然带来更高任务精度 | 经验外推 | approximation、optimization、compute 均改变 | 不成立 |
