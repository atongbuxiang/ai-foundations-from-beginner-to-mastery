---
type: source
status: active
area: [sources, neural-networks, language-modeling, weight-tying, loss-design]
source_type: paper
title: "Tying Word Vectors and Word Classifiers: A Loss Framework for Language Modeling"
author: "Hakan Inan; Khashayar Khosravi; Richard Socher"
year: 2017
url: "https://arxiv.org/abs/1611.01462"
openreview: "https://openreview.net/forum?id=r1aPbsFle"
venue: "ICLR 2017"
accessed: 2026-08-29
source_tier: A
license: "author preprint/OpenReview paper；本库仅保存独立摘要、必要公式与链接"
scope_role: supporting-core
temporal_role: foundational
related: ["[[输入—输出权重共享与 Weight Tying]]", "[[Label Smoothing、置信度与目标偏置]]"]
created: 2026-08-24
updated: 2026-08-29
---

# Inan、Khosravi、Socher：Tying Word Vectors and Classifiers

> [!abstract] 来源定位
> 论文从语言模型 loss framework 与输入/输出共享语义空间出发导出 weight tying，并结合 embedding-similarity target distribution 做实验。它与 Press–Wolf 同期构成 tying 的经典来源；本库只调用共享矩阵与参数效率结论，不把论文的附加 loss 或 RNN 实验等同于现代所有 LLM 训练合同。

## 证据分工

- 理论框架把 output classifier rows 与 word vectors 联系起来；
- 实用方案重用 input embedding 作为 output classification matrix；
- 论文另有基于 embedding similarity 的 target/loss 修改，不能与“仅 tying”混成一个消融；
- 实验结论绑定 Penn Treebank、当时模型与优化协议。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| IKS-C1 | tying 可由共享输入/输出语义空间的框架导出 | 理论/建模 | 论文假设 | 有条件成立 |
| IKS-C2 | tying 与 similarity-based soft target 是同一操作 | 实验对象混淆 | 两者可分别消融 | 错误 |
| IKS-C3 | 参数减少精确等于一个 $V\times d$ 矩阵 | 计数 | 直接 tying 且维度相同 | 条件下精确 |
| IKS-C4 | 共享后 input gradient 仍只更新出现 token 行 | 梯度误读 | output VJP 通常对所有类稠密 | 错误 |
