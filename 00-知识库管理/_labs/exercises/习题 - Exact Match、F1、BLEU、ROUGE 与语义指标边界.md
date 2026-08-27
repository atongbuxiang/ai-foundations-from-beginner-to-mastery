---
type: exercise
status: verified
area: [language-models, evaluation, metrics]
topic: "[[Exact Match、F1、BLEU、ROUGE 与语义指标边界]]"
solution: "[[解答 - Exact Match、F1、BLEU、ROUGE 与语义指标边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Exact Match、F1、BLEU、ROUGE 与语义指标边界

## A. 识别与复述

### LM58-A01
解释 normalization、tokenization 与 reference set 为什么是指标定义的一部分。

### LM58-A02
区分 token F1、BLEU modified precision、ROUGE-L 与 contextual similarity 的匹配单位。

### LM58-A03
说明 corpus BLEU 为什么不能一般地由 sentence BLEU 的算术平均得到。

## B. 手算与构造

### LM58-B01
reference tokens 为 $(a,a,b,c)$，candidate 为 $(a,b,b,d)$。按多重集合计算 precision、recall 与 F1。

### LM58-B02
candidate 长度 $c=6$、reference 有效长度 $r=8$。计算 BLEU brevity penalty。

### LM58-B03
求序列 $(a,b,c,d,e)$ 与 $(b,c,x,e)$ 的 LCS 长度，并计算以 LCS 为匹配数的 precision、recall 和 $F_1$。

## C. 推导与证明

### LM58-C01
证明 token F1 可写为 $2|C\cap R|/(|C|+|R|)$，其中交集按多重集合取最小计数。

### LM58-C02
从“过短候选不应只靠高 precision 获益”的目标解释 BLEU 中 $BP=\exp(1-r/c)$（当 $c<r$）的方向与边界。

### LM58-C03
构造一个语义等价但 EM 为零的候选，并说明这不能反推所有语义指标都一定判对。

## D. 边界、反例与纠错

### LM58-D01
构造 token F1 很高但事实含义相反的答案。

### LM58-D02
反驳“BERTScore 高就说明回答事实正确”。

### LM58-D03
说明用 test references 反复选择 normalization 或 metric 后只报最优结果的选择偏差。

## E. AI 迁移

### LM58-E01
为抽取式 QA 设计 normalization 单元测试。

### LM58-E02
为摘要系统设计由 lexical、semantic、factual 和人工指标组成的诊断向量。

### LM58-E03
设计一个 paired bootstrap，用来比较两个系统的 corpus-level 指标差异。

独立完成后查看[[解答 - Exact Match、F1、BLEU、ROUGE 与语义指标边界]]。
