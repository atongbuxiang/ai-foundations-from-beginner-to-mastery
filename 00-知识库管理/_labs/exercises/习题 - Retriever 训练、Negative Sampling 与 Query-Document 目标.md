---
type: exercise
status: verified
area: [language-models, dense-retrieval]
topic: "[[Retriever 训练、Negative Sampling 与 Query-Document 目标]]"
solution: "[[解答 - Retriever 训练、Negative Sampling 与 Query-Document 目标]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Retriever 训练、Negative Sampling 与 Query-Document 目标

## A. 识别与复述

### LM45-A01
列出三种不等价的正例定义。

### LM45-A02
区分随机、BM25 hard 与 model-mined negatives。

### LM45-A03
什么是 stale negative index？

## B. 手算与构造

### LM45-B01
正例与两个负例 logits 为 $(2,1,0)$，$\tau=1$；计算正例 softmax 概率与损失。

### LM45-B02
按上一题概率计算三个 logit 的梯度。

### LM45-B03
构造 in-batch false negative。

## C. 推导与证明

### LM45-C01
推导 softmax 对比分数梯度。

### LM45-C02
解释温度减小为何放大梯度且增加错标敏感性。

### LM45-C03
写多正例目标并说明它仍不能解决未知正例。

## D. 边界、反例与纠错

### LM45-D01
反驳“越难的负样本越好”。

### LM45-D02
为何训练 loss 降低不推出部署 Recall@K 提升？

### LM45-D03
审计只报告 negative sampler 名称、不报告比例与刷新延迟的实验。

## E. AI 迁移

### LM45-E01
设计 mined negatives 的人工分层审计。

### LM45-E02
为对话 query 与扫描 PDF 部署域设计迁移切片。

### LM45-E03
设计 retrieval、generation、attribution 多目标报告。

独立完成后查看[[解答 - Retriever 训练、Negative Sampling 与 Query-Document 目标]]。
