---
type: exercise
status: verified
area: [language-models, tokenization, wordpiece]
topic: "[[WordPiece、词表构建与最长匹配边界]]"
solution: "[[解答 - WordPiece、词表构建与最长匹配边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - WordPiece、词表构建与最长匹配边界

## A. 识别与复述

### LM05-A01
区分 WordPiece 的词表学习与 longest-match 编码。

### LM05-A02
`##` continuation prefix 表示什么，不表示什么？

### LM05-A03
为什么必须把现代实现细节与 2012 历史来源分账？

## B. 手算与构造

### LM05-B01
词表 `play, player, ##er, ##ing, [UNK]`，编码 `player` 与 `playing`。

### LM05-B02
词表 `a, ab, ##bc`，对 `abc` 执行 greedy，并给一条全局合法路径。

### LM05-B03
$p(a)=.4,p(b)=.5,p(ab)=.3$，计算 $p(ab)/(p(a)p(b))$ 与 log-score。

## C. 推导与证明

### LM05-C01
说明 longest-match 不等于最少 token 动态规划，并给充分反例结构。

### LM05-C02
分析 trie 编码的时间界，设输入长度 $n$、最大 piece 长度 $L$。

### LM05-C03
证明整词 `[UNK]` 策略使不同输入多对一，不能无损解码。

## D. 边界、反例与纠错

### LM05-D01
反驳“WordPiece 总按 $p(ab)/(p(a)p(b))$ 训练”。

### LM05-D02
反驳“词表包含所有 Unicode 字符就不会失败”。

### LM05-D03
同一词表，unknown 作用域不同会怎样改变 IDs 与模型信息？

## E. AI 迁移

### LM05-E01
审计一个 BERT tokenizer 配置需读取哪些 normalizer/pretokenizer/special 字段？

### LM05-E02
设计 greedy-dead-end 与超长 pre-token 单测。

### LM05-E03
比较 WordPiece 与 BPE 时怎样避免把模型、数据与 tokenizer 因果混在一起？

独立完成后查看[[解答 - WordPiece、词表构建与最长匹配边界]]。

