---
type: source
status: draft
area: [sources, neural-networks, machine-translation, sampled-softmax, importance-sampling]
source_type: paper
title: "On Using Very Large Target Vocabulary for Neural Machine Translation"
author: "Sébastien Jean; Kyunghyun Cho; Roland Memisevic; Yoshua Bengio"
year: 2015
url: "https://aclanthology.org/P15-1001/"
doi: "https://doi.org/10.3115/v1/P15-1001"
venue: "ACL-IJCNLP 2015"
accessed: 2026-08-24
source_tier: A
license: "ACL Anthology paper；本库仅保存独立摘要、必要公式与链接"
scope_role: sampled-training-evidence
temporal_role: foundational
related: ["[[Sampled、Hierarchical 与 Adaptive Softmax]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Jean et al.：Very Large Target Vocabulary 与采样训练

> [!abstract] 来源定位
> 论文针对大词表 NMT 提出基于有偏 importance sampling 的近似训练，使每次更新只处理目标词表子集；推理可选择全词表或子集。它承担“训练采样不自动等于 exact full-softmax MLE”的原始实例，不能与 negative sampling 或 hierarchical model 混同。

## 证据边界

- 采样集合与 proposal/correction 决定估计目标和偏差；
- 训练近似与推理候选裁剪是两个独立选择；
- 在 full vocabulary 上报告 exact NLL 仍需全量或等价精确归一化；
- 原论文的速度/翻译结果绑定当时 NMT 架构、硬件和词表。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| JLV-C1 | 子集训练可降低每步输出计算 | 算法 | 样本数远小于 $V$ | 成立 |
| JLV-C2 | 论文算法是无偏 full-softmax gradient estimator | 估计 | 论文明确采用 biased approximation | 错误 |
| JLV-C3 | 训练采样后必须在推理也采同一子集 | 阶段混淆 | 推理可另选 full/subset | 错误 |
| JLV-C4 | sampled approximation 的 perplexity 可不经 full normalization 直接等同 exact perplexity | 评价混淆 | 需同一概率合同 | 错误 |
