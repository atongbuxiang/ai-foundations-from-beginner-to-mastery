---
type: exercise
status: verified
area: [language-models, rag, data-contracts]
topic: "[[Chunk、Metadata、Embedding 与 Index 合同]]"
solution: "[[解答 - Chunk、Metadata、Embedding 与 Index 合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Chunk、Metadata、Embedding 与 Index 合同

## A. 识别与复述

### LM42-A01
为什么检索对象不是原始文档本身？

### LM42-A02
列出 chunk 必须携带的六类最小字段。

### LM42-A03
区分 pre-filter 与 post-filter。

## B. 手算与构造

### LM42-B01
$N=1000,L=256,O=64$ 时计算滑窗 chunk 数。

### LM42-B02
单位向量内积为 $0.8$；计算平方欧氏距离。

### LM42-B03
构造 child 检索、parent 阅读、span 引用的三层映射。

## C. 推导与证明

### LM42-C01
推导 $\|q-v\|^2=2-2q^\top v$ 的适用条件。

### LM42-C02
说明 overlap 增加为何不保证独立证据 coverage 等比例增加。

### LM42-C03
证明 chunk oracle coverage 低时，仅调 retriever 无法突破该上界。

## D. 边界、反例与纠错

### LM42-D01
反驳“cosine 与 dot product 总是等价排序”。

### LM42-D02
审计更换 encoder 却复用旧索引。

### LM42-D03
为何只删关系库记录、不删 vector replica 不算完成删除？

## E. AI 迁移

### LM42-E01
为 PDF ingestion 写可逆数据血缘 manifest。

### LM42-E02
设计跨边界 gold span 的 chunker 回归测试。

### LM42-E03
设计 ACL、时间与 tenant 元数据过滤审计。

独立完成后查看[[解答 - Chunk、Metadata、Embedding 与 Index 合同]]。
