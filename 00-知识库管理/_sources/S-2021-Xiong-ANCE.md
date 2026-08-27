---
type: source
status: verified
area: [sources, information-retrieval, dense-retrieval]
source_type: paper
title: "Approximate Nearest Neighbor Negative Contrastive Learning for Dense Text Retrieval"
author: "Lee Xiong et al."
year: 2021
url: "https://openreview.net/forum?id=zeFrfgyZln"
accessed: 2026-08-26
source_tier: P1
license: "ICLR paper; independent summary"
scope_role: hard-negative-training
related: ["[[Retriever 训练、Negative Sampling 与 Query-Document 目标]]"]
created: 2026-08-26
updated: 2026-08-26
---

# ANCE：从全语料挖掘困难负样本

> [!abstract] 来源定位
> ANCE 用异步更新的 ANN 索引从全语料寻找当前模型难区分的负样本，讨论局部 in-batch negatives 的梯度问题。课程采用其 negative distribution 与索引陈旧性合同。

更难的负样本可能包含漏标正例；若不审计 false negatives，训练信号会惩罚真正相关文档。
