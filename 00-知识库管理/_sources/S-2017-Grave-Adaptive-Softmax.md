---
type: source
status: draft
area: [sources, neural-networks, language-modeling, adaptive-softmax]
source_type: paper
title: "Efficient Softmax Approximation for GPUs"
author: "Édouard Grave; Armand Joulin; Moustapha Cissé; David Grangier; Hervé Jégou"
year: 2017
url: "https://proceedings.mlr.press/v70/grave17a.html"
venue: "ICML 2017"
accessed: 2026-08-24
source_tier: A
license: "PMLR paper；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[Sampled、Hierarchical 与 Adaptive Softmax]]", "[[Embedding 初始化、缩放、分解与量化接口]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Grave et al.：Adaptive Softmax

> [!abstract] 来源定位
> 论文利用词频不平衡把高频词留在 head、低频词分入 clusters，并为 tail 使用较低维表示，以最小化期望计算时间且适配 GPU 矩阵运算。它承担 adaptive softmax 的原始方法合同；“近 full-softmax accuracy”和速度倍数是论文实验结果，不是硬件无关定理。

## 方法边界

频繁词只需 head probability；稀有词 probability 是 head 中 cluster probability 与 cluster 内 conditional probability 的乘积。训练只展开目标所在 tail cluster；完整 log-probability 输出仍需遍历所有 clusters。词频排序、cutoffs、tail dimensions 与 kernel shape 共同决定收益。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| AS-C1 | 频率分组可降低期望而非最坏计算 | 复杂度 | label distribution 长尾 | 成立 |
| AS-C2 | tail 低维可进一步减少参数与计算 | 参数化 | 维度随 cluster 降低 | 成立 |
| AS-C3 | adaptive softmax 与 flat softmax 具有完全同一函数类 | 结构外推 | hierarchy/dimension 改变模型 | 错误 |
| AS-C4 | 任意均匀标签分布都获得同样收益 | 分布外推 | 方法利用不平衡频率 | 不成立 |
