---
type: source
status: draft
area: [sources, ai/attention, ai/interpretability]
source_type: paper
title: "Attention is not Explanation"
author: "Sarthak Jain, Byron C. Wallace"
year: 2019
url: "https://aclanthology.org/N19-1357/"
accessed: 2026-08-24
source_tier: A
license: "ACL Anthology paper; independent summary only"
scope_role: boundary
temporal_role: interpretability
related: ["[[Attention 失效模式、反例与证据地图]]", "[[内容寻址、Query、Key 与 Value]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Attention is not Explanation：权重与忠实解释的边界

> [!abstract] 来源定位
> 论文在所研究的 NLP 模型与任务中比较 attention 权重、梯度相关性和可产生近似预测的替代权重，质疑把可视化权重直接当作忠实解释。课程采用它提出验证义务，不把标题扩大为“attention 在任何情况下都没有解释价值”。

## 采用的审计问题

1. “解释”指描述内部读取、预测敏感性、反事实充分性，还是人类语义合理性？
2. 固定其他变量改变权重，输出是否按宣称变化？
3. 是否存在显著不同却产生近似输出的替代权重？
4. value、后续 MLP、residual 和多层组合是否使单层权重失去因果充分性？

## 边界

- 权重作为模型内部状态是事实；作为忠实因果归因则需额外证据；
- 某些任务中的负结果不能证明所有架构、层、头、解释目标都失败；
- 可视化可用于提出假说和调试，但不能单独裁决因果机制。
