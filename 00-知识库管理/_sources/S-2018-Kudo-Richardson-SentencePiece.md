---
type: source
status: verified
area: [sources, tokenization, sentencepiece]
source_type: paper
title: "SentencePiece: A Simple and Language Independent Subword Tokenizer and Detokenizer"
author: "Taku Kudo, John Richardson"
year: 2018
url: "https://arxiv.org/abs/1808.06226"
accessed: 2026-08-26
source_tier: P1
license: "论文与 Apache-2.0 实现；本库保存独立摘要与链接"
scope_role: implementation-foundation
temporal_role: raw-sentence-tokenization
related: ["[[Tokenizer 作为码本、分段路径与压缩接口]]", "[[Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Kudo–Richardson：SentencePiece

> [!abstract] 来源定位
> SentencePiece 展示了直接从 raw sentences 训练和确定性 detokenization 的工程路线，并提供 BPE/Unigram 等实现。课程用它说明“算法”和“文本接口/实现库”是两层对象。

## 关键边界

- “language independent”指不依赖特定语言分词器的接口目标，不等于在所有语言上 token 成本公平；
- 以 meta symbol 表示空格有助于可逆 detokenization，但 normalization 配置仍可能改变原始字符串；
- SentencePiece 是工具/模型格式，不等于只有一种 segmentation objective；
- 真实复现需保存 model proto、normalizer、special ids、byte fallback、vocabulary 与库版本。

