---
type: source
status: verified
area: [sources, generative-models, gan, optimization]
source_type: paper
title: "GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium"
author: "Martin Heusel et al."
year: 2017
url: "https://arxiv.org/abs/1706.08500"
venue: "NeurIPS 2017"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: dynamics-and-evaluation
temporal_role: foundational
related: ["[[Minimax 动力学、旋转、阻尼与局部收敛]]", "[[GAN 稳定化方法、受控比较与证据地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Heusel et al.：TTUR

> [!abstract] 来源定位
> 论文在 stochastic approximation 假设下分析生成器与判别器不同学习率时间尺度，并引入 FID。课程引用它解释 two-time-scale 不是“多训几步 critic”的口号；必须检查步长序列、噪声、局部稳定与实现 optimizer 是否满足理论。

## 断言审计

| 断言 | 类型 | 条件/边界 | 课程判断 |
|---|---|---|---|
| 分离学习率可形成快慢时间尺度 | stochastic approximation | 步长与稳定假设 | 有条件成立 |
| 任意 Adam 超参数均继承收敛 | 外推 | 理论近似/假设有限 | 不采用 |
| FID 比单一画廊更系统 | 评价方法 | encoder、样本量与实现依赖 | 有限采用 |
| TTUR 使任意 GAN 达到全局 Nash | 普遍外推 | 非凸非凹 | 错误 |

