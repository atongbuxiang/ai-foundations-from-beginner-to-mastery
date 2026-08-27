---
type: source
status: verified
area: [sources, information-geometry, curvature, optimization]
source_type: paper
title: "New Insights and Perspectives on the Natural Gradient Method"
author: [James Martens]
year: 2020
url: "https://www.jmlr.org/papers/v21/17-678.html"
venue: "JMLR 21(146):1–76"
accessed: 2026-08-26
source_tier: A
license: "CC BY 4.0；本库保存独立摘要和必要公式"
scope_role: foundational-review
temporal_role: reference
related: ["[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]", "[[自然梯度、KL 局部几何与坐标不变性]]", "[[GGN、经验 Fisher 与曲率近似陷阱]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Martens：Natural Gradient 的二阶视角

> [!abstract] 来源定位
> 系统区分 Hessian、GGN、Fisher 与 empirical Fisher，并分析 natural gradient 的二阶解释、trust-region/Tikhonov 设计和近似参数化不变性。它是 TRN-17、20、21 的正式主桥。

## 课程采用

- 对负对数似然，true Fisher 对模型自身 $y\sim p_\theta(y\mid x)$ 取期望；empirical Fisher 使用数据标签，两者一般不同；
- 输出分布为以网络输出作 natural parameter 的指数族等重要条件下，Fisher 可与 GGN 相等；
- GGN 是 PSD 的 Hessian 近似，Hessian 本身可不定；
- exact natural gradient 具有适当重参数化性质，ordinary Hessian/Newton 并不共享完全相同的性质；
- damping 与 trust region 不是无关的工程补丁，而是局部模型可信度合同。

## 不作的外推

不把“Fisher 可替代 Hessian”写成矩阵恒等式；不把 empirical Fisher 或 Adam 的平方梯度直接称为 Fisher；不把 infinitesimal invariance 写成有限 LR、近似 solve 下的 bitwise trajectory invariance。
