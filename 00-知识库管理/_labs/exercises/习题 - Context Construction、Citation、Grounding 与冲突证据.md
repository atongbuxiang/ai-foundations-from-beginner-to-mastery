---
type: exercise
status: verified
area: [language-models, rag, citations]
topic: "[[Context Construction、Citation、Grounding 与冲突证据]]"
solution: "[[解答 - Context Construction、Citation、Grounding 与冲突证据]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Context Construction、Citation、Grounding 与冲突证据

## A. 识别与复述

### LM46-A01
区分 relevance、support、factuality、attribution 与 faithfulness。

### LM46-A02
为何 retrieved set 不等于最终 context？

### LM46-A03
区分 citation correctness 与 completeness。

## B. 手算与构造

### LM46-B01
3 个需验证 claims 中，2 个有支持；共 4 条引用中 3 条正确。计算 completeness 与 correctness。

### LM46-B02
预算 300 tokens，三段长度/效用为 $(180,8),(140,7),(100,4)$；在可加假设下选最优集合。

### LM46-B03
构造“事实为真但当前引用不支持”的例子。

## C. 推导与证明

### LM46-C01
写含冗余惩罚与 coverage 奖励的上下文选择目标。

### LM46-C02
证明每句都有引用不推出 citation correctness 为 1。

### LM46-C03
说明 gold + distractor 与 gold-only 对照识别什么。

## D. 边界、反例与纠错

### LM46-D01
为何低熵 context 不等于真实来源？

### LM46-D02
审计只引用页面、不定位 span 的系统。

### LM46-D03
两个来源冲突时为何不能简单多数投票？

## E. AI 迁移

### LM46-E01
设计 claim→citation→span 数据结构。

### LM46-E02
设计 prompt injection 文档的防护与回归测试。

### LM46-E03
为时效冲突来源写透明回答模板。

独立完成后查看[[解答 - Context Construction、Citation、Grounding 与冲突证据]]。
