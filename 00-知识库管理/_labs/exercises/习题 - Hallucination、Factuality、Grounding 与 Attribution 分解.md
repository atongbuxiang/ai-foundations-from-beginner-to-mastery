---
type: exercise
status: verified
area: [language-models, evaluation, factuality]
topic: "[[Hallucination、Factuality、Grounding 与 Attribution 分解]]"
solution: "[[解答 - Hallucination、Factuality、Grounding 与 Attribution 分解]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Hallucination、Factuality、Grounding 与 Attribution 分解

## A. 识别与复述

### LM61-A01
区分 truth、task correctness、grounding、citation correctness 与 attribution completeness。

### LM61-A02
解释 atomic claim、时间切片与来源权威为什么必须先定义。

### LM61-A03
区分 intrinsic 与 extrinsic hallucination，并说明该分类依赖 task contract。

## B. 手算与构造

### LM61-B01
回答含 8 个 atomic claims，其中 6 个为真。计算 atomic factual precision。

### LM61-B02
系统给出 5 条 citation，其中 4 条真正支持对应 claim；10 个需引用 claims 中有 6 个获得充分支持。分别计算 citation precision 与 claim coverage。

### LM61-B03
三条 claims 权重为 $(1,3,2)$，正确指示为 $(1,0,1)$。计算 unweighted 与 weighted factual precision。

## C. 推导与证明

### LM61-C01
用集合与指示变量写出 citation precision 和 attribution completeness，说明二者分母为何不同。

### LM61-C02
证明“每条 citation 都正确”不能推出“回答的所有事实 claims 都有支持”。

### LM61-C03
把自动 factuality evaluator 写成 retrieval→segmentation→entailment 管线，并分解可能的假阴性来源。

## D. 边界、反例与纠错

### LM61-D01
各构造 true-but-ungrounded 与 grounded-but-false 的例子。

### LM61-D02
反驳“有 URL 的回答就不是幻觉”。

### LM61-D03
解释知识随时间变化时，静态 reference 可能把当前真命题判错的问题。

## E. AI 迁移

### LM61-E01
为医疗 RAG 设计 claim ledger 与证据 span 数据结构。

### LM61-E02
设计来源冲突时的权威、时间与弃权规则。

### LM61-E03
为长回答设计 claim-weighted 人工审计抽样，避免只检查容易事实。

独立完成后查看[[解答 - Hallucination、Factuality、Grounding 与 Attribution 分解]]。
