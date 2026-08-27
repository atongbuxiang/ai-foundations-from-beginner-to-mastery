---
type: source
status: verified
area: [sources, generative-models/autoregressive, density-estimation]
source_type: paper
title: "Neural Autoregressive Distribution Estimation"
author: [Benigno Uria, Marc-Alexandre Côté, Karol Gregor, Iain Murray, Hugo Larochelle]
year: 2016
url: "https://arxiv.org/abs/1605.02226"
accessed: 2026-08-25
source_tier: A
scope_role: core
temporal_role: classical
related: ["[[概率链式分解、顺序选择与自回归生成]]", "[[显式密度、隐式分布与可计算性三角]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Uria et al.：Neural Autoregressive Distribution Estimation

> [!abstract] 来源定位
> NADE 以概率乘法规则把联合分布写成可归一化条件概率的乘积，并用参数共享降低逐条件建模成本。它承担 tractable autoregressive density estimator 的正式来源；课程不把其特定网络或当年 benchmark 结论外推到所有现代架构。

## 核心贡献

- normalized conditional factors 的乘积自动 normalized；
- 对二值和实值数据提供 tractable density estimation；
- 参数共享使不同条件因子不是完全独立训练；
- order-agnostic 训练说明排序可作为模型设计变量，但不会让有限网络对所有排序自动等价。

## 课程调用与边界

| 调用 | 采用 | 不外推 |
|---|---|---|
| GEN-02 | exact density evaluation 与 ancestral sampling 接口 | 三角权衡是工程图，不是不可兼得定理 |
| GEN-04 | chain rule、ordering、shared conditional network | 任意排序有限容量性能相同 |
| GEN-08 | tractable likelihood 与 sequential sampling 的代价 | 2016 benchmark 代表当前前沿 |

