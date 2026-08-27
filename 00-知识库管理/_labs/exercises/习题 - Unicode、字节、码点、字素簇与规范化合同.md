---
type: exercise
status: verified
area: [language-models, unicode, text]
topic: "[[Unicode、字节、码点、字素簇与规范化合同]]"
solution: "[[解答 - Unicode、字节、码点、字素簇与规范化合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Unicode、字节、码点、字素簇与规范化合同

## A. 识别与复述

### LM02-A01
区分 byte、code point、code unit、grapheme cluster 和 glyph。

### LM02-A02
解释 NFC/NFD 与 NFKC/NFKD 的两条轴。

### LM02-A03
为什么 UTF-8 decode 的 error policy 属于数据合同？

## B. 手算与构造

### LM02-B01
写出预组合 `é` 与分解 `e+◌́` 的码点序列，并预测 NFC/NFD 结果。

### LM02-B02
已知 `中` 的码点为 U+4E2D、UTF-8 为 `E4 B8 AD`。分别给 bytes/code points/graphemes 数。

### LM02-B03
构造含 `①`、全角字母和上标数字的例子，说明 NFKC 可能丢什么信息。

## C. 推导与证明

### LM02-C01
说明规范化幂等 $N(N(x))=N(x)$ 为什么是流水线测试的重要不变量。

### LM02-C02
证明 replacement-character error policy 一般不是 byte-injective，因而不能 byte round-trip。

### LM02-C03
说明 grapheme fertility 与 code-point fertility 可能给同一 tokenizer 不同排名。

## D. 边界、反例与纠错

### LM02-D01
反驳“视觉相同就应规范化为同一字符串”，给 confusable 反例。

### LM02-D02
反驳“所有已 NFC 字符串拼接后仍是 NFC”。

### LM02-D03
一套评估只用 Python `len` 报 tokens/character。指出跨语言与跨编程语言复现问题。

## E. AI 迁移

### LM02-E01
设计 Unicode tokenizer conformance/property test 输入族。

### LM02-E02
分析 zero-width、bidi control、homoglyph 对 prompt 日志与模型输入的双重风险。

### LM02-E03
为训练/服务写 normalization manifest，并说明升级 Unicode 版本时怎样回归测试。

独立完成后查看[[解答 - Unicode、字节、码点、字素簇与规范化合同]]。

