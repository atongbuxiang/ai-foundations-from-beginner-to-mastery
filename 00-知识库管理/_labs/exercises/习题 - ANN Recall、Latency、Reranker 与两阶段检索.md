---
type: exercise
status: verified
area: [language-models, ann, reranking]
topic: "[[ANN Recall、Latency、Reranker 与两阶段检索]]"
solution: "[[解答 - ANN Recall、Latency、Reranker 与两阶段检索]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - ANN Recall、Latency、Reranker 与两阶段检索

## A. 识别与复述

### LM44-A01
区分 ANN recall、task evidence recall 与 chunk oracle coverage。

### LM44-A02
解释 HNSW 分层导航的直觉。

### LM44-A03
区分 dual encoder、late interaction 与 cross-encoder。

## B. 手算与构造

### LM44-B01
exact top-5 为 $\{a,b,c,d,e\}$，ANN 为 $\{a,c,e,f,g\}$；计算 ANN recall@5。

### LM44-B02
候选 top-20 不含 gold，说明任意 reranker 的 gold Recall@5 上界。

### LM44-B03
编码、ANN、fetch、rerank、生成 p95 分别为 8、12、5、35、90 ms；计算端到端串行和并指出假设。

## C. 推导与证明

### LM44-C01
证明 reranked set 的 gold coverage 不超过 first-stage candidate coverage。

### LM44-C02
写出 ColBERT MaxSim 并解释为何文档 token 表示可预计算。

### LM44-C03
分解量化误差、遍历误差与 top-$K$ 截断误差。

## D. 边界、反例与纠错

### LM44-D01
构造 ANN recall 低但 task recall 不变的情况。

### LM44-D02
为何平均 latency 不足以描述在线系统？

### LM44-D03
审计不同硬件、不同 $K$ 的 reranker 速度比较。

## E. AI 迁移

### LM44-E01
设计 exact→quantized→ANN→rerank 逐项消融。

### LM44-E02
写 HNSW 参数 sweep 的质量—延迟—内存表。

### LM44-E03
设计新增、更新、删除后的 ANN 一致性测试。

独立完成后查看[[解答 - ANN Recall、Latency、Reranker 与两阶段检索]]。
