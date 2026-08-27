---
type: exercise
status: verified
area: [language-models, tokenization, bpe]
topic: "[[BPE、合并规则与确定性编码解码]]"
solution: "[[解答 - BPE、合并规则与确定性编码解码]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - BPE、合并规则与确定性编码解码

## A. 识别与复述

### LM04-A01
为什么 BPE 模型必须保存 ordered merges 而非仅词表？

### LM04-A02
列出 pretokenizer、初始 alphabet、word boundary、frequency weight、tie 与 overlap 六项合同。

### LM04-A03
区分 subword BPE、byte-level BPE 与原始 byte-pair compression。

## B. 手算与构造

### LM04-B01
语料 `aa×2, ab×1`，初始按字符。算 pair counts，执行一次 merge 并写新语料。

### LM04-B02
merges rank 0 `(b,c)`、rank 1 `(a,b)`，编码 `abc`；交换 ranks 再编码。

### LM04-B03
对 `aaaa` 合并 `(a,a)`，按左到右不重叠替换；给新序列并算一次出现数。

## C. 推导与证明

### LM04-C01
证明每次 merge 至少不会增加训练语料的符号总数；何时严格减少？

### LM04-C02
说明同频 pair 的不同选择为何可通过改变下一轮计数导致最终词表分叉。

### LM04-C03
写加权 pair count 公式，并证明把 word types 当等权与按 token frequency 一般不同。

## D. 边界、反例与纠错

### LM04-D01
反驳“最终 vocab 相同，编码就相同”。

### LM04-D02
反驳“byte-level BPE 自动保留原始文本”。

### LM04-D03
一个并行 trainer 只固定 seed。指出仍可能非确定的计数/并列路径。

## E. AI 迁移

### LM04-E01
为 BPE tokenizer 写五个必须通过的单元测试。

### LM04-E02
比较 regex pretokenizer 允许/禁止跨空格 merge 对代码和自然语言的影响。

### LM04-E03
审计“词表从 32k 增到 64k，token 数下降 15%，所以训练快 15%”。

独立完成后查看[[解答 - BPE、合并规则与确定性编码解码]]。

