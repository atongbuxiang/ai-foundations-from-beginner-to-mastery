---
type: exercise
status: verified
area: [language-models, tokenization, evaluation]
topic: "[[Tokenizer 评估、多语言公平、安全与证据地图]]"
solution: "[[解答 - Tokenizer 评估、多语言公平、安全与证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Tokenizer 评估、多语言公平、安全与证据地图

## A. 识别与复述

### LM08-A01
区分 bytes/token、tokens/code point、tokens/grapheme 与 word fertility。

### LM08-A02
列出可逆、压缩、词表、计算、质量、安全六类指标。

### LM08-A03
为什么“language independent”不是公平性结论？

## B. 手算与构造

### LM08-B01
组 A 有 900 文档、fertility 1；组 B 有 100 文档、fertility 4。算总体均值与等组均值。

### LM08-B02
文档 bytes 为 1000，A/B token 数 400/500，算 bytes/token。若 total NLL(nats) 为 800/760，算两者 BPB。

### LM08-B03
给一组 paired 文档长度差，说明为何以文档而非 token 做 bootstrap。

## C. 推导与证明

### LM08-C01
推导总体 fertility 是组均值的 mixture-weighted average，并说明 Simpson 型隐藏。

### LM08-C02
说明固定 token steps 与固定 raw corpus 比较的 estimand 不同。

### LM08-C03
构造两个 tokenizer 的 Pareto 比较：一个压缩好但安全差，一个相反，说明无单标量最优。

## D. 边界、反例与纠错

### LM08-D01
反驳“bytes/token 高，所以模型更准”。

### LM08-D02
反驳“总体平均公平，所以每种语言公平”。

### LM08-D03
一个 benchmark 只测 clean text。列出至少四类未覆盖 tokenizer 攻击面。

## E. AI 迁移

### LM08-E01
写一个 tokenizer A/B 预注册比较协议。

### LM08-E02
为 API 计价与延迟设计语言切片风险指标。

### LM08-E03
审计 BytePiece 压缩率主张：哪些属于事实、实验、假说与越界外推？

独立完成后查看[[解答 - Tokenizer 评估、多语言公平、安全与证据地图]]。

