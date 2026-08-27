---
type: source
status: verified
area: [sources, experimentation, variance, fine-tuning]
source_type: paper
title: "Fine-Tuning Pretrained Language Models: Weight Initializations, Data Orders, and Early Stopping"
author: "Dodge et al."
year: 2020
url: "https://arxiv.org/abs/2002.06305"
accessed: 2026-08-26
source_tier: A
scope_role: empirical-variance
related: ["[[随机种子、配对比较、置信区间与序贯决策]]", "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Dodge 等：Fine-tuning 方差与 Early Stopping

> [!abstract] 来源定位
> 论文通过大量 fine-tuning trials 研究 initialization、data order 和 early stopping 对下游结果的影响，说明“同一方法”本身是一种运行分布。

## 本卷调用

- 分离 model initialization seed、data-order seed 与其他随机源；
- 使用配对运行控制共享随机难度；
- 报告完整 trial 分布、failure denominator 和 early-stop rule；
- 不以最好 seed 替代预先声明的算法表现。

## 边界

具体方差大小依任务、模型和 fine-tuning recipe；该论文支持审计必要性，不给出普适 seed 数。
