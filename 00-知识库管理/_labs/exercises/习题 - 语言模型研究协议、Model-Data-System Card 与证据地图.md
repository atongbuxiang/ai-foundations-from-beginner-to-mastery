---
type: exercise
status: verified
area: [language-models, research-protocol, documentation, evidence]
topic: "[[语言模型研究协议、Model-Data-System Card 与证据地图]]"
solution: "[[解答 - 语言模型研究协议、Model-Data-System Card 与证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 语言模型研究协议、Model-Data-System Card 与证据地图

## A. 识别与复述

### LM72-A01
区分 description、evidence index 与 governance interface。

### LM72-A02
分别说明 Model、Data、System Card 的核心对象。

### LM72-A03
解释 PROV 中 Entity、Activity、Agent，并各给一个语言模型例子。

## B. 手算与构造

### LM72-B01
把“新模型更好更安全”改写为包含对象、比较、总体、指标/阈值、不确定性和版本的可证伪 claim。

### LM72-B02
给出 claim→estimate→scores→raw traces→bundle/data 的五行证据表字段。

### LM72-B03
一个 card 有 20 个必填证据字段，16 个有 artifact link，其中 2 个链接失效。分别计算表面完成率与有效链接完成率。

## C. 推导与证明

### LM72-C01
说明 Card 字段完整为何不是系统安全的充分条件。

### LM72-C02
解释新 template 为什么可以使旧 claim 失效，即使 weights 未变。

### LM72-C03
证明只保留支持证据会产生 publication/selection bias。

## D. 边界、反例与纠错

### LM72-D01
反驳“厂商 System Card 是官方文件，所以等于独立复现”。

### LM72-D02
构造 Model Card 正确但 System Card 结论错误的场景。

### LM72-D03
Card 更新时覆盖旧版本而不留历史，会破坏哪些审计能力？

## E. AI 迁移

### LM72-E01
为一个 RAG agent 写三卡最小目录。

### LM72-E02
把 Govern–Map–Measure–Manage 映射到一次发布流程。

### LM72-E03
设计一个 claim ledger 条目，含支持、反对、未知、owner、expiry 与 invalidation trigger。

独立完成后查看[[解答 - 语言模型研究协议、Model-Data-System Card 与证据地图]]。
