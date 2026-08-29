---
type: source
status: active
area: [sources, neural-networks, word-embeddings, representation-learning]
source_type: paper
title: "Distributed Representations of Words and Phrases and their Compositionality"
author: "Tomas Mikolov; Ilya Sutskever; Kai Chen; Greg Corrado; Jeffrey Dean"
year: 2013
url: "https://proceedings.neurips.cc/paper/2013/hash/9aa42b31882ec039965f3c4923ce901b-Abstract.html"
venue: "NeurIPS 2013"
accessed: 2026-08-29
source_tier: A
license: "NeurIPS paper；本库仅保存独立摘要、短公式与链接"
scope_role: historical-core
temporal_role: foundational
related: ["[[Embedding 几何、相似度与各向异性]]", "[[Embedding Lookup、稀疏梯度与参数规模]]", "[[Sampled、Hierarchical 与 Adaptive Softmax]]"]
created: 2026-08-24
updated: 2026-08-29
---

# Mikolov et al.：Distributed Word Representations

> [!abstract] 来源定位
> 论文改进 Skip-gram，提出 frequent-word subsampling、negative sampling 与 phrase representations，并报告线性类比/组合现象。它承担经典词向量几何的历史实验入口；本库不把有限 benchmark 上的线性关系升级为所有语义都具有全局欧氏线性结构。

## 证据对象

- 训练目标是由中心词表示预测上下文，而不是直接监督“语义距离”；
- negative sampling 改变完整 softmax 的训练目标与计算；
- 论文在指定语料和 analogy 任务上观察到某些向量平移关系；
- phrase 作为独立 token 可表达不可由单词简单组合的固定短语。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| W2V-C1 | Skip-gram 学到可用于相似/类比任务的向量 | 经验 | 语料、目标、频率与评测依赖 | 原论文范围成立 |
| W2V-C2 | 任意语义关系都等于固定向量平移 | 普遍外推 | 多义、频率、tokenization 与任务 | 不成立 |
| W2V-C3 | negative sampling 等于精确 full softmax MLE | 目标混淆 | 采样目标不同 | 一般不等价 |
| W2V-C4 | 高 cosine 必然表示人类语义相似 | 解释外推 | geometry、frequency 与 benchmark 相关 | 不成立 |
