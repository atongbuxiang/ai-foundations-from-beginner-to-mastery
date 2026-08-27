---
type: source
status: draft
area: [sources, neural-networks, contextual-embeddings, anisotropy]
source_type: paper
title: "How Contextual are Contextualized Word Representations?"
author: "Kawin Ethayarajh"
year: 2019
url: "https://aclanthology.org/D19-1006/"
doi: "https://doi.org/10.18653/v1/D19-1006"
venue: "EMNLP-IJCNLP 2019"
accessed: 2026-08-24
source_tier: A
license: "ACL Anthology paper（CC BY 4.0）；本库仅保存独立摘要、必要数字与链接"
scope_role: core
temporal_role: foundational-analysis
related: ["[[Embedding 几何、相似度与各向异性]]", "[[表示学习的任务、表示与下游风险]]", "[[表示坍缩、非坍缩与可辨识边界]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Ethayarajh：Contextual Embedding Geometry

> [!abstract] 来源定位
> 论文比较 ELMo、BERT 与 GPT-2 的 contextual representations，研究各层的 anisotropy、同一词跨上下文 self-similarity 与 static embedding 可解释方差。它承担特定模型/语料上的经验几何证据；本库把“各向异性”拆成均值、谱、有效秩和随机方向基线，不将单一 cosine 统计视为普遍定义。

## 原论文边界

- 论文报告所研究模型各层的 contextual representations 并非 isotropic；
- 同一词跨上下文的 self-similarity 在较高层降低；
- 在所研究设置中，static embedding 对 contextual variance 的平均解释比例低于 5%；
- 这些数字绑定模型版本、层、语料、采样与度量，不是所有 embedding 系统的常数。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| ETH-C1 | 所测 contextual spaces 呈 anisotropic | 经验 | ELMo/BERT/GPT-2 与论文协议 | 原论文范围成立 |
| ETH-C2 | mean cosine 足以定义所有 anisotropy | 定义外推 | centering、谱、局部簇可能不同 | 不成立 |
| ETH-C3 | 去掉 top PC 必然改善任意任务 | 方法外推 | 任务、拟合数据与分布偏移依赖 | 不成立 |
| ETH-C4 | token table row 与 contextual state 可直接混测 | 对象混淆 | 一个是参数，一个是输入依赖表示 | 错误 |

