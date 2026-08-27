---
type: source
status: draft
area: [sources, neural-networks, variational-dropout, local-reparameterization]
source_type: paper
title: "Variational Dropout and the Local Reparameterization Trick"
author: "Diederik P. Kingma; Tim Salimans; Max Welling"
year: 2015
url: "https://proceedings.neurips.cc/paper/2015/hash/bc7316929fe1545bf0b98d114ee3ecb8-Abstract.html"
venue: "NeurIPS 2015"
accessed: 2026-08-24
source_tier: A
license: "NeurIPS proceedings paper；本库仅保存独立摘要、必要公式与链接"
scope_role: variational-and-estimator
temporal_role: foundational
related: ["[[Dropout 的方差、共适应解释与 Bayesian 边界]]", "[[DropConnect、权重噪声与激活噪声]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Kingma、Salimans、Welling：Variational Dropout 与 Local Reparameterization

> [!abstract] 来源定位
> 论文把特定 Gaussian dropout objective 与变分推断联系起来，并把 global weight noise 转换为 datapoint-local preactivation noise，以降低 stochastic-gradient estimator 的方差。它承担 variational/estimator 层的原始来源；binary dropout、任意 prior、任意跨样本 joint law 与精确 Bayesian posterior 不由此自动成立。

## 方法边界

对线性层和合适的独立 Gaussian weight posterior，可解析得到每个样本的 preactivation 均值/方差，再采 local noise。对按样本求和的期望 loss，marginal 保持可给同一目标估计；global sample 与 local samples 的跨样本相关结构不同，梯度方差和分布式行为也不同。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| LRT-C1 | 特定 global Gaussian weight noise 可局部重参数化到 preactivation | 分布 | 线性层、独立结构与可算 moments | 成立 |
| LRT-C2 | local noise 可降低 minibatch gradient estimator variance | 估计 | 论文采样与独立条件 | 原范围成立 |
| LRT-C3 | local 与 global sampling 的完整 batch joint distribution 相同 | 联合分布外推 | 跨样本相关性不同 | 错误 |
| LRT-C4 | Variational Dropout 等于精确 posterior inference | 近似误读 | posterior family/prior/ELBO 受限 | 错误 |
