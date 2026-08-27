---
type: exercise
status: verified
area: [language-models, rag]
topic: "[[参数记忆、外部记忆与 RAG 潜变量分解]]"
solution: "[[解答 - 参数记忆、外部记忆与 RAG 潜变量分解]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 参数记忆、外部记忆与 RAG 潜变量分解

## A. 识别与复述

### LM41-A01
区分参数记忆、上下文记忆与外部记忆。

### LM41-A02
解释 latent document $z$ 在 RAG 分解中的含义。

### LM41-A03
区分 RAG-Sequence、RAG-Token 与简单 context 拼接。

## B. 手算与构造

### LM41-B01
两文档权重为 $0.7,0.3$，给正确答案的条件概率为 $0.8,0.2$；计算边缘正确概率。

### LM41-B02
全语料权重为 $(0.5,0.3,0.2)$，top-2 截断后重新归一化；计算新权重。

### LM41-B03
构造一个“答案正确但检索错误”的最小案例。

## C. 推导与证明

### LM41-C01
从联合分布推导 $p(y\mid x,\mathcal C)=\sum_zp(z\mid x,\mathcal C)p(y\mid x,z)$。

### LM41-C02
推导给定目标答案后的文档责任度 $q(z\mid x,y^\star)$。

### LM41-C03
证明 top-$K$ 内重新归一化一般不等于全语料后验。

## D. 边界、反例与纠错

### LM41-D01
反驳“接入向量数据库就已经完成 RAG”。

### LM41-D02
为何 gold context 下仍答错不能归因于 retriever？

### LM41-D03
审计只更新原文、不重建向量与缓存的系统。

## E. AI 迁移

### LM41-E01
为一项时效问答写 corpus→retrieval→context→generation 事件账。

### LM41-E02
设计 closed-book、normal RAG 与 gold-context 三组对照。

### LM41-E03
写出带 snapshot、删除传播和缓存失效的外部记忆更新合同。

独立完成后查看[[解答 - 参数记忆、外部记忆与 RAG 潜变量分解]]。
