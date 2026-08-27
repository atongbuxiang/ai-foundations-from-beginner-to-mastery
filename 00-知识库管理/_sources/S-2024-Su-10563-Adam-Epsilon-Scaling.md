---
type: source
status: verified
area: [sources, optimization, adam, scaling]
source_type: blog
title: "Adam的epsilon如何影响学习率的Scaling Law？"
author: 苏剑林
year: 2024
url: "https://spaces.ac.cn/archives/10563"
accessed: 2026-08-26
source_tier: C
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
scope_role: chinese-derivation-entry
temporal_role: research-exposition
related: ["[[Adam 的 Epsilon、数值稳定与实现分歧]]", "[[Adam 的尺度不变性、Sign 近似与 Update RMS]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 苏剑林：Adam epsilon 与 Scaling

> [!abstract] 来源定位
> 文章把 Adam direction 近似为 soft-sign，并研究 epsilon、batch noise 与局部二阶 loss decrease 的关系。它是“epsilon 不只是防除零”的中文推导入口；不是对完整 Adam 状态、所有 epsilon placement 或深网全局训练的定理。

## 采用的核心对象

文章以

$$
\operatorname{softsign}(x;\epsilon)
=\frac{x}{\sqrt{x^2+\epsilon^2}}
$$

作为 sign 与线性 gradient 之间的插值：$|x|\gg\epsilon$ 时接近 sign，$|x|\ll\epsilon$ 时近似 $x/\epsilon$。随后在 Gaussian batch-noise、坐标独立、局部 Hessian 正定与平均场近似下，估计最佳局部步长随 batch 的变化，并提出 epsilon 增大时更接近 SGD-like regime、某类 Surge 条件更难成立。

## 假设账

| 环节 | 性质 | 课程处理 |
|---|---|---|
| 完整 Adam → soft-sign | 模型化近似 | 忽略 $m_t,v_t$ 的不同时标与历史相关 |
| soft-sign → clip | 计算近似 | 保留饱和/线性区，精度需数值反查 |
| batch gradient 为 Gaussian | 分布假设 | 只作局部/大样本入口 |
| 坐标协方差对角 | 结构假设 | 深网相关梯度中一般不精确 |
| Hessian 正定与二阶截断 | 局部近似 | 不覆盖非凸、时变高阶项 |
| 坐标比值换成统一 $\kappa$ | 平均场 | 标为 `A/H`，不得升级为 identity |

## 课程补严

根号内 $\epsilon^2$ 的 soft-sign 与常见框架 $\sqrt v+\epsilon$ 不是同一个公式；课程在 [[Adam 的 Epsilon、数值稳定与实现分歧]] 中把 exact implementation、数值 floor 和解释模型三层分开，再用逐点曲线检验近似区间。
