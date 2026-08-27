---
type: exercise
status: verified
area: [language-models, multi-hop-retrieval]
topic: "[[Multi-hop、Iterative、Graph Retrieval 与 Tool Interface]]"
solution: "[[解答 - Multi-hop、Iterative、Graph Retrieval 与 Tool Interface]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Multi-hop、Iterative、Graph Retrieval 与 Tool Interface

## A. 识别与复述

### LM47-A01
为何多次检索不必然构成多跳检索？

### LM47-A02
列出检索状态机的五个要素。

### LM47-A03
区分 decompose-first、交错检索与图遍历。

## B. 手算与构造

### LM47-B01
两跳命中率为 $0.8,0.7$，在独立假设下算 joint recall。

### LM47-B02
给出实体 A→公司 B→国家 C 的两跳状态日志。

### LM47-B03
预算 3 次调用，第一次无新增证据、第二次重复同一 ID；写合理 stop/rollback。

## C. 推导与证明

### LM47-C01
写状态 $s_t$、动作 $a_t$、观察 $o_t$ 与转移 $F$。

### LM47-C02
解释为何第二跳依赖第一跳时不能把真实 joint recall 简单写成 $r_1r_2$。

### LM47-C03
证明 oracle first-hop 与 oracle all-evidence 诊断的层次不同。

## D. 边界、反例与纠错

### LM47-D01
反驳“可读 CoT 就是忠实 evidence chain”。

### LM47-D02
构造 query drift 或 confirmation loop。

### LM47-D03
为何 reflection token 不能当人工真值？

## E. AI 迁移

### LM47-E01
设计带 provenance 的工具调用 schema。

### LM47-E02
设计 retrieve/no-retrieve gate 的 precision/recall 审计。

### LM47-E03
设计多跳系统的 call/token/latency 与 joint evidence 报告。

独立完成后查看[[解答 - Multi-hop、Iterative、Graph Retrieval 与 Tool Interface]]。
