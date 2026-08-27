---
type: source
status: verified
area: [sources, in-context-learning, linear-regression]
source_type: paper
title: "What Can Transformers Learn In-Context? A Case Study of Simple Function Classes"
author: "Shivam Garg et al."
year: 2022
url: "https://arxiv.org/abs/2208.01066"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: controlled-function-learning
related: ["[[ICL 的 Bayesian、线性回归与元优化解释]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Transformer 的上下文函数学习

> [!abstract] 来源定位
> 论文从头训练 Transformer，在 prompt 中给出函数样本，使其对未见线性函数达到接近最小二乘的预测，并扩展到若干受控函数类。课程采用可计算的线性回归 oracle、分布移位坐标和 baseline 比较。

“达到类似最小二乘的误差”不等于逐层严格实现最小二乘，也不自动外推自然语言任务和通用预训练模型。
