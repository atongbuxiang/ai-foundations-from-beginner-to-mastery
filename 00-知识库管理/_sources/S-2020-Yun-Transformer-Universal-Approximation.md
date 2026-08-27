---
type: source
status: draft
area: [sources, ai/transformers, ai/expressivity]
source_type: paper
title: "Are Transformers universal approximators of sequence-to-sequence functions?"
author: "Chulhee Yun et al."
year: 2020
url: "https://openreview.net/forum?id=ByxRM0Ntvr"
accessed: 2026-08-24
source_tier: A
license: "OpenReview paper; independent summary only"
scope_role: theory-boundary
temporal_role: theory
related: ["[[Attention 失效模式、反例与证据地图]]", "[[Self-Attention、Cross-Attention 与张量形状]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Transformer 的序列到序列通用逼近边界

> [!abstract] 来源定位
> 论文给出 Transformer 对连续序列到序列函数的通用逼近结果：无位置编码时针对 permutation-equivariant 函数类；加入适当位置编码后可覆盖紧致域上的一般连续序列到序列函数。课程只在原假设下引用，不把存在性定理解释成有限宽深训练保证。

## 假设账本

- 目标函数连续，输入限制在紧致域/论文规定范数空间；
- 网络深度、宽度与参数可随逼近精度构造；
- 无位置编码的函数类需满足置换等变结构；
- 加入位置编码改变对称性与可表达目标；
- 定理回答“存在参数”，不回答 SGD 能否找到、样本复杂度、鲁棒性或工程效率。

## 调用

- [[Self-Attention、Cross-Attention 与张量形状]]：张量映射与置换等变性；
- [[Attention 失效模式、反例与证据地图]]：表达存在性、可学习性和系统能力分层。
