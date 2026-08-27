---
type: source
status: verified
area: [sources, information-geometry, optimization]
source_type: paper
title: "Natural Gradient Works Efficiently in Learning"
author: [Shun-ichi Amari]
year: 1998
url: "https://doi.org/10.1162/089976698300017746"
venue: "Neural Computation 10(2):251–276"
accessed: 2026-08-26
source_tier: A
scope_role: primary
temporal_role: foundational
related: ["[[自然梯度、KL 局部几何与坐标不变性]]", "[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Amari：Natural Gradient

> [!abstract] 来源定位
> Natural gradient 的经典信息几何来源：ordinary coordinate gradient 依赖参数坐标，Fisher metric 下的 gradient 表示分布流形中的最速方向。论文还分析特定 online-learning 渐近效率；课程不把该结论外推到所有有限步深网训练。

## 课程采用

由局部 KL 约束

$$
\tfrac12\Delta\theta^T F(\theta)\Delta\theta\le\varepsilon
$$

与一阶 loss model 推出方向 $-F^\dagger g$ 及归一化尺度。坐标不变性需讨论同一分布族的光滑可逆重参数化、exact metric/solve 与 infinitesimal step；finite discretization、damping 和近似 Fisher 会削弱它。
