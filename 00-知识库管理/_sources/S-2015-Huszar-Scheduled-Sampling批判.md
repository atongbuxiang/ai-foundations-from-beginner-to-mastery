---
type: source
status: verified
area: [sources, generative-models/autoregressive, statistical-estimation]
source_type: paper
title: "How (not) to Train your Generative Model: Scheduled Sampling, Likelihood, Adversary?"
author: Ferenc Huszár
year: 2015
url: "https://arxiv.org/abs/1511.05101"
accessed: 2026-08-25
source_tier: A
scope_role: counterpoint
temporal_role: classical
related: ["[[Teacher Forcing、暴露偏差与生成时分布漂移]]", "[[S-2020-Su-7259-Exposure-Bias]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Huszár：Scheduled Sampling 的一致性批判

> [!abstract] 来源定位
> 论文以短序列反例分析 Scheduled Sampling：训练时把部分真实前缀替换为模型样本，会改变被最小化的总体目标；在某些极限下，最优解趋向忽略变量依赖的边缘乘积，而非真实联合分布。课程用它反驳“训练—推理输入更相似，所以估计一定更正确”的直觉跳跃。

## 两步反例的结构

真实数据为 $P(x_1,x_2)$，模型为 $Q(x_1)Q(x_2\mid x_1)$。若第二步有时使用从 $Q(x_1)$ 产生的前缀，却仍以真实 $x_2$ 为 target，那么训练 pair 的联合分布不再总是 $P(x_1,x_2)$；极端替换会把 prefix 与 target 解耦，推动 $Q(x_2\mid x_1)$ 学向 $P(x_2)$。

## 课程判断

- 该反例说明 Scheduled Sampling 不是一般的一致 MLE；
- 它不证明 Scheduled Sampling 在所有有限任务上更差；
- Teacher Forcing 下的正确 MLE 在可实现、无限数据、全局优化条件下仍以真实联合分布为最优；
- 感知质量、任务指标与 likelihood 的错配是另一问题，不能借“Exposure Bias”一词混为一谈。

