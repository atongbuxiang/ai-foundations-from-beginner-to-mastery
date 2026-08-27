---
type: source
status: verified
area: [sources, curvature, fisher-information, optimization]
source_type: paper
title: "Limitations of the Empirical Fisher Approximation for Natural Gradient Descent"
author: [Frederik Kunstner, Philipp Hennig, Lukas Balles]
year: 2019
url: "https://proceedings.neurips.cc/paper/2019/hash/46a558d97954d0692411c861cf78ef79-Abstract.html"
venue: "NeurIPS 2019"
accessed: 2026-08-26
source_tier: A
scope_role: primary-critical
temporal_role: reference
related: ["[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]", "[[GGN、经验 Fisher 与曲率近似陷阱]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Kunstner–Hennig–Balles：Empirical Fisher 的限制

> [!abstract] 来源定位
> 论文用定义、简单模型与数值例子反驳“empirical Fisher 普遍近似 Fisher/Hessian”。课程用它建立 data-label outer product 与 model-sampled score covariance 的硬分界。

## 课程采用

对单样本随机梯度 $g$，empirical Fisher 对应 non-central second moment，可分解为

$$
\mathbb E[gg^T]=\operatorname{Cov}(g)+\mathbb E[g]\mathbb E[g]^T.
$$

这可支持 gradient-noise adaptation 解释，却不是一般 curvature 身份。只有模型正确指定、估计一致、接近合适最优点且数据相对容量充分等强条件下，EF 才可能接近 Fisher/Hessian；远离最优点时方向和尺度都可严重失真。
