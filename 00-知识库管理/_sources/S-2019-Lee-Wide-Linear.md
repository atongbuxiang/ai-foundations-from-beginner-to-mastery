---
type: source
status: active
area: [sources, wide-neural-networks, linearization]
source_type: paper
title: "Wide Neural Networks of Any Depth Evolve as Linear Models Under Gradient Descent"
author: [Jaehoon Lee, Lechao Xiao, Samuel S. Schoenholz, Yasaman Bahri, Roman Novak, Jascha Sohl-Dickstein, Jeffrey Pennington]
year: 2019
url: "https://proceedings.neurips.cc/paper/2019/hash/0d1a9651497a38d8b1c3871c84528bd4-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "NeurIPS proceedings; retain citation"
venue: "Advances in Neural Information Processing Systems 32"
scope_role: primary
temporal_role: modern-theory
related: ["[[NTK、Lazy Training 与 Kernel Regime]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Wide Neural Networks Evolve as Linear Models
> [!abstract] 来源定位
> 在适当宽网 scaling 和 gradient descent 条件下，建立原网络训练轨迹与初始化处一阶 Taylor 模型的接近性，并给出对应高斯预测描述。本库调用 finite-to-infinite linearization bridge 与实验诊断；不把任意大模型直接判为 linear regime。
## 本库调用
1. initialization linearization；
2. wide-limit training trajectory；
3. finite-width approximation；
4. parameterization/learning-rate 条件；
5. NTK baseline。

