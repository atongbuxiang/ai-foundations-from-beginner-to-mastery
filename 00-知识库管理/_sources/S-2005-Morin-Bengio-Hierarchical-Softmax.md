---
type: source
status: active
area: [sources, neural-networks, language-modeling, hierarchical-softmax]
source_type: paper
title: "Hierarchical Probabilistic Neural Network Language Model"
author: "Frederic Morin; Yoshua Bengio"
year: 2005
url: "https://proceedings.mlr.press/r5/morin05a.html"
venue: "AISTATS 2005"
accessed: 2026-08-29
source_tier: A
license: "PMLR paper；本库仅保存独立摘要、必要公式与链接"
scope_role: historical-core
temporal_role: foundational
related: ["[[Sampled、Hierarchical 与 Adaptive Softmax]]"]
created: 2026-08-24
updated: 2026-08-29
---

# Morin、Bengio：Hierarchical Probabilistic Language Model

> [!abstract] 来源定位
> 论文用二叉层次分解替代平坦全词表归一化，并以 WordNet 先验构造 hierarchy，在其语言模型设置中报告显著加速。它承担 hierarchical probability factorization 的经典来源；现代 GPU kernel、树构造与经验速度必须重新测量。

## 概率合同

每个词是树的一片叶。词概率等于从根到该叶路径上局部二元决策概率的乘积。只要每个内部节点的左右条件概率和为 1、叶恰好覆盖词表，所有叶概率自动归一化。平衡树路径长为 $O(\log V)$，但不平衡树、语义/频率聚类和硬件并行度会改变实际成本。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| HS-C1 | 合法概率树给出对所有叶精确归一化的模型 | 概率 | 完整树与合法局部 Bernoulli | 精确 |
| HS-C2 | 平衡二叉树单词路径为 $O(\log V)$ | 复杂度 | 树近似平衡 | 成立 |
| HS-C3 | hierarchical softmax 等于原 flat-softmax 函数族的无误差加速 | 参数化外推 | 改变 factorization 与共享结构 | 错误 |
| HS-C4 | 更少标量节点必然在 GPU 上更快 | 系统外推 | batching、分支与 kernel 利用率相关 | 不成立 |
