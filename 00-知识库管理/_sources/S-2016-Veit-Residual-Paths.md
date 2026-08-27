---
type: source
status: draft
area: [sources, neural-networks, residual-networks, effective-paths]
source_type: paper
title: "Residual Networks Behave Like Ensembles of Relatively Shallow Networks"
author: "Andreas Veit; Michael Wilber; Serge Belongie"
year: 2016
url: "https://proceedings.neurips.cc/paper_files/paper/2016/hash/37bc2f75bf1bcfe8450a1a41c200364c-Abstract.html"
venue: "NeurIPS 2016"
accessed: 2026-08-23
source_tier: A
license: "NeurIPS paper；本库仅保存独立摘要、必要数字与链接"
scope_role: core
temporal_role: foundational
related: ["[[深度、有效路径与稳定性证据地图]]", "[[残差块 Jacobian 与梯度直通]]", "[[Highway、Dense Connection 与 Skip 结构比较]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Veit、Wilber、Belongie：Residual Paths

> [!abstract] 来源定位
> 论文用 residual block 的路径展开、删除/重排实验与梯度路径长度分析，提出“相对浅路径的 ensemble-like 行为”解释。它是有效路径视角的经典经验来源；本库保留“like”与实验条件，不把共享状态、共享参数、相互作用路径说成独立模型集成。

## 证据对象

- 代数上，线性化残差乘积可展开为选择或跳过 branch 的有序项；
- 实验上，论文考察删除单个 block、交换 block 以及限制反向路径长度；
- 在论文的 ResNet-110 分析中，梯度的主要贡献集中在比名义深度短得多的路径区间，论文报告的代表区间为 10—34。

这些结果绑定当时架构、训练数据、路径采样与度量。它们不能直接外推为所有现代残差网络、Transformer 或训练阶段的固定分布。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| VP-C1 | 线性 residual product 有不同 branch 数目的路径项 | 代数 | 有序矩阵乘积 | 精确 |
| VP-C2 | 所有路径都是独立训练的浅层网络 | 结构外推 | 参数、状态和输出聚合高度耦合 | 错误 |
| VP-C3 | 论文删除实验支持 ensemble-like 鲁棒性解释 | 经验 | 指定 ResNet 与协议 | 有条件支持 |
| VP-C4 | 有效路径长度是架构唯一常数 | 动态外推 | 参数、数据、损失、训练时间均会改变贡献 | 错误 |

