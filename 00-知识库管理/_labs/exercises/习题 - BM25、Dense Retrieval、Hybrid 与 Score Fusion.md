---
type: exercise
status: verified
area: [language-models, information-retrieval]
topic: "[[BM25、Dense Retrieval、Hybrid 与 Score Fusion]]"
solution: "[[解答 - BM25、Dense Retrieval、Hybrid 与 Score Fusion]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - BM25、Dense Retrieval、Hybrid 与 Score Fusion

## A. 识别与复述

### LM43-A01
BM25 的 IDF、词频饱和与长度校正分别解决什么？

### LM43-A02
双编码器为何能预计算文档向量？

### LM43-A03
RRF 解决了什么，又丢失了什么？

## B. 手算与构造

### LM43-B01
$k_1=1.5,b=0.75,|d|=\operatorname{avgdl},f=3,\operatorname{IDF}=2$；计算单词项 BM25 贡献。

### LM43-B02
$q=(1,2),d_1=(2,0),d_2=(0,2)$；按内积排序。

### LM43-B03
$k_0=60$；A 排名 $(1,10)$，B 排名 $(3,3)$，计算 RRF 并排序。

## C. 推导与证明

### LM43-C01
求 BM25 词频因子在 $f\to\infty$ 的极限。

### LM43-C02
证明候选 union 的 gold coverage 是后续融合的上界。

### LM43-C03
说明 raw BM25 与 cosine 直接加权为何含量纲问题。

## D. 边界、反例与纠错

### LM43-D01
构造 BM25 胜 dense 的罕见编号查询。

### LM43-D02
构造 dense 胜 BM25 的语义改写查询。

### LM43-D03
审计用测试集选择 fusion 权重的实验。

## E. AI 迁移

### LM43-E01
设计 lexical-only、dense-only、union oracle、RRF 四路评估。

### LM43-E02
为中英混合技术语料设计 analyzer 与 embedding 切片。

### LM43-E03
写 hybrid 检索的分数、名次、tie 与候选深度 manifest。

独立完成后查看[[解答 - BM25、Dense Retrieval、Hybrid 与 Score Fusion]]。
