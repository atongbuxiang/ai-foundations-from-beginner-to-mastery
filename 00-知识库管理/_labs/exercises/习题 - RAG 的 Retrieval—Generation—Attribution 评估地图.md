---
type: exercise
status: verified
area: [language-models, rag, evaluation]
topic: "[[RAG 的 Retrieval—Generation—Attribution 评估地图]]"
solution: "[[解答 - RAG 的 Retrieval—Generation—Attribution 评估地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - RAG 的 Retrieval—Generation—Attribution 评估地图

## A. 识别与复述

### LM48-A01
区分 $R,G,A$ 三个事件。

### LM48-A02
列出八层故障树。

### LM48-A03
为何边缘平均数不能决定联合成功率？

## B. 手算与构造

### LM48-B01
相关集合 2 个，top-5 命中 1 个；计算 Recall@5 与 Precision@5。

### LM48-B02
三个查询首个相关排名为 1、2、无命中；按无命中 RR=0 算 MRR。

### LM48-B03
relevance 为 $(3,2,0)$；计算 $DCG@3$。

## C. 推导与证明

### LM48-C01
构造三组数据具有相同 $P(R),P(G),P(A)$ 但不同联合率。

### LM48-C02
说明 query-level paired bootstrap 为何要保留样本内所有 stage。

### LM48-C03
推导 exact-oracle、gold-context、gold-layout 的诊断顺序。

## D. 边界、反例与纠错

### LM48-D01
为何答案字符串出现在 passage 不等于完整支持？

### LM48-D02
审计只报最终 EM、且系统 B 使用更大 $K$ 的比较。

### LM48-D03
为何自动 judge 必须有人工审计子集？

## E. AI 迁移

### LM48-E01
设计 answerable/unanswerable 风险—覆盖率评估。

### LM48-E02
设计时间、冲突、注入、ACL 四类压力测试。

### LM48-E03
写同预算 A/B 的质量、成本、配对区间报告模板。

独立完成后查看[[解答 - RAG 的 Retrieval—Generation—Attribution 评估地图]]。
