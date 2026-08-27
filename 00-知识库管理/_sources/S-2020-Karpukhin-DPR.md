---
type: source
status: verified
area: [sources, information-retrieval, dense-retrieval]
source_type: paper
title: "Dense Passage Retrieval for Open-Domain Question Answering"
author: "Vladimir Karpukhin et al."
year: 2020
url: "https://aclanthology.org/2020.emnlp-main.550/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: dual-encoder-retrieval
related: ["[[BM25、Dense Retrieval、Hybrid 与 Score Fusion]]", "[[Retriever 训练、Negative Sampling 与 Query-Document 目标]]"]
created: 2026-08-26
updated: 2026-08-26
---

# DPR：双编码器、内积检索与负样本

> [!abstract] 来源定位
> DPR 分别编码 query 与 passage，以内积和对比目标训练，并比较随机、BM25 与 in-batch negatives。课程采用其可预计算文档向量的系统分解和 top-k passage accuracy。

论文中的 9%—19% top-20 优势绑定其数据集、语料与基线，不能外推为 dense 在所有领域优于 BM25。
