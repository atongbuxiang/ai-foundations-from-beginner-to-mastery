---
type: source
status: verified
area: [sources, neural-networks/residual-stability, neural-ode]
source_type: paper
title: "Neural Ordinary Differential Equations"
author: "Ricky T. Q. Chen; Yulia Rubanova; Jesse Bettencourt; David Duvenaud"
year: 2018
url: "https://proceedings.neurips.cc/paper/2018/hash/69386f6bb1dfed68692a24c8686939b9-Abstract.html"
arxiv: "1806.07366"
venue: "NeurIPS 2018"
accessed: 2026-08-23
source_tier: A
license: "NeurIPS paper；本库仅保存独立摘要、必要公式与链接"
scope_role: bridge
temporal_role: foundational
related: ["[[ResNet 的 ODE 与离散动力系统视角]]", "[[流映射、Liouville 公式与连续正规化流]]", "[[Continuous Normalizing Flow、Liouville 与 FFJORD]]", "[[自动微分：前向、反向与高阶模式]]"]
created: 2026-08-23
updated: 2026-08-25
---

# Chen et al.：Neural ODE

> [!abstract] 来源定位
> 论文直接以神经网络参数化连续时间向量场，并让 ODE solver 计算输出。它承担 continuous-depth 模型、solver tolerance 与 adjoint 入口；本库严格区分“离散网络的精确反向传播”和“连续伴随方程再数值离散”。

## 模型合同

$$
\frac{dz(t)}{dt}=f_\theta(z(t),t),
\qquad
z(t_1)=\operatorname{ODESolve}(z(t_0),f_\theta,t_0,t_1).
$$

solver、容差、事件、最大步数与 dtype 都属于计算图语义，不是可忽略实现细节。

## 证据边界

- 连续深度不等于零离散误差；
- continuous adjoint 与 discrete adjoint 在有限容差下可能不同；
- 自适应步数提供输入依赖计算，但 latency、误差和梯度必须分别审计；
- exact ODE flow 的唯一性/可逆性性质不能自动赋给一般有限步 residual block。
