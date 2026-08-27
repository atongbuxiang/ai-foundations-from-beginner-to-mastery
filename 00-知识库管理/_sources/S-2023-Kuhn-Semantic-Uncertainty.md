---
type: source
status: verified
area: [sources, language-models, uncertainty, semantic-equivalence]
source_type: paper
title: "Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation"
author: "Lorenz Kuhn, Yarin Gal, Sebastian Farquhar"
year: 2023
url: "https://arxiv.org/abs/2302.09664"
accessed: 2026-08-26
source_tier: P1
license: "ICLR paper; independent summary"
scope_role: semantic-uncertainty
related: ["[[Proper Scoring、Calibration、ECE 与 Selective Generation]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Semantic Uncertainty：从字符串样本聚合到意义事件

> [!abstract] 来源定位
> 开放生成中不同字符串可表达同一答案。论文按语义等价类聚合采样响应的概率质量并计算 semantic entropy。本库采用“先定义事件再谈概率”的原则，同时审计 entailment/cluster 模型、采样预算与有限样本误差。

Semantic entropy 是一种估计器而非事实正确性的证明；等价类划分错误、遗漏低概率意义或 API 无 logprob 都会改变结论。
