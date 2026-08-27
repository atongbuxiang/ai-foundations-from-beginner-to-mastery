---
type: source
status: verified
area: [sources, ai/text-generation, generative-models/sampling]
source_type: paper
title: "The Curious Case of Neural Text Degeneration"
author: [Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, Yejin Choi]
year: 2019
url: "https://arxiv.org/abs/1904.09751"
accessed: 2026-08-25
source_tier: A
scope_role: core
temporal_role: classical
related: ["[[祖先采样、温度、截断与自回归解码分布]]", "[[S-2020-Su-7500-自回归停止与解码]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Holtzman et al.：Nucleus Sampling 与文本退化

> [!abstract] 来源定位
> 论文实证分析 likelihood-trained language model 在不同解码器下的退化，并提出按累计概率质量动态截断的 nucleus/top-$p$ sampling。它承担 top-$p$ 的原始方法与特定实验结论；“top-$p$ 对所有生成任务最佳”不成立。

## 定义

对前缀 $h$，令 $V_p(h)$ 为按 $p_\theta(v\mid h)$ 从高到低累加，质量首次达到阈值 $p$ 的最小 token 集合。解码核为

$$
q_p(v\mid h)=
\frac{p_\theta(v\mid h)\mathbf 1\{v\in V_p(h)\}}
{\sum_{w\in V_p(h)}p_\theta(w\mid h)}.
$$

它是一个前缀依赖的重新归一化分布，不是从原模型“原样采样”。

## 边界

- 候选集合大小随条件熵变化；
- 截断删除尾部质量并改变 sequence distribution；
- beam/greedy 最大化路径得分与从模型分布抽样是不同任务；
- 论文的人评与自动指标受模型、语料和超参数限制。

