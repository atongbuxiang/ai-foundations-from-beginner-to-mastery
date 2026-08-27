---
type: source
status: verified
area: [sources, ai/scaling-laws, optimization, architecture, data]
source_type: blog
title: "解构 Scaling Law：优化、架构、数据的三重奏"
author: 苏剑林
year: 2026
url: "https://spaces.ac.cn/archives/11833"
accessed: 2026-08-26
source_tier: C
license: "科学空间；仅保存独立摘要、短公式与链接"
scope_role: synthesis-hypothesis
temporal_role: active-research
related: ["[[经验 Scaling Law、幂律拟合与不可约项]]", "[[Broken Scaling、涌现表象与优化架构数据分解]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 解构 Scaling Law：优化、架构、数据的三重奏

> [!abstract] 来源定位
> 文章把理想测试损失分为数据 gap、优化 gap、架构 gap 与理想地板，并为学习率、batch、steps、参数量、深宽、数据量和重复训练提出幂律假说。它是课程的中文综合视角与假说生成器，不承担普遍 Scaling Law 定理。

## 可调用骨架

文章考虑

$$
L(\mathcal E\mid\mathcal D,\mathcal A,\mathcal O)
=F_{\rm data}+F_{\rm opt}+F_{\rm arch}+L_{\rm ideal}.
$$

并以单调性与经验规律猜测各 gap 对训练时域、架构尺度和数据变量的依赖，再通过约束优化推导候选最优关系。

## 课程保留

- scaling 结果可由 optimizer、architecture、data 三类因素及交互共同改变；
- exponent 可能更接近任务/数据难度，coefficient 可能更受工程进展影响——作为待检验假说；
- multi-epoch、embedding parameter counting、width/depth 与 sequence length 都可能改变有限窗口；
- 文章明确承认多数公式是启发式假设而非定理。

## 边界

- 各 gap 非负需要“更优对象的定义、分布与训练目标一致”等条件；
- 数据、架构、优化并不天然可加分离，交互项可能显著；
- 单调性不能推出幂律，接近经典指数也不能构成独立验证；
- 2026-07-29 发布内容按博客 exposition/hypothesis 使用。
