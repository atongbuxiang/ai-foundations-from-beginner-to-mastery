---
type: exercise
status: verified
area: [language-models, pretraining-data, deduplication]
topic: "[[精确去重、MinHash、LSH 与近重复检测]]"
solution: "[[解答 - 精确去重、MinHash、LSH 与近重复检测]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 精确去重、MinHash、LSH 与近重复检测

## A. 识别与复述

### LM19-A01
区分 byte exact、canonical exact、substring 与 near duplicate。

### LM19-A02
区分 Jaccard resemblance 与 containment 的分母。

### LM19-A03
MinHash、LSH、exact verification 与 clustering 各做什么？

## B. 手算与构造

### LM19-B01
$A=\{a,b,c,d\},B=\{b,c,e\}$，算 Jaccard 与双向 containment。

### LM19-B02
$s=0.8,b=10,r=4$，算 LSH candidate probability。

### LM19-B03
构造 $A\sim B,B\sim C,A\not\sim C$ 的 shingle 集，说明 connected component 链式合并。

## C. 推导与证明

### LM19-C01
证明 $P[h_{min}(A)=h_{min}(B)]=J(A,B)$。

### LM19-C02
推导 $\hat J$ 的期望与方差（独立哈希理想化）。

### LM19-C03
推导 $1-(1-s^r)^b$ 并分析 $b,r$ 对 recall/load 的方向。

## D. 边界、反例与纠错

### LM19-D01
给短文完整包含于长文但 Jaccard 很低的反例。

### LM19-D02
反驳“未发生 LSH bucket collision 就证明不重复”。

### LM19-D03
说明留最早/最长/最高质代表会怎样改变数据分布。

## E. AI 迁移

### LM19-E01
设计 MinHash 小宇宙枚举 oracle。

### LM19-E02
为真实 corpus 设计 recall—candidate load—false delete frontier。

### LM19-E03
审计只写“MinHash threshold 0.8”而无 shingle/signature/bands 的报告。

独立完成后查看[[解答 - 精确去重、MinHash、LSH 与近重复检测]]。

