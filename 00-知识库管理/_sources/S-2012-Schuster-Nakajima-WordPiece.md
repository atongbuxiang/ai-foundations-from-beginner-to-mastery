---
type: source
status: verified
area: [sources, tokenization, wordpiece, speech]
source_type: paper
title: "Japanese and Korean Voice Search"
author: "Mike Schuster, Kaisuke Nakajima"
year: 2012
url: "https://research.google/pubs/japanese-and-korean-voice-search/"
doi: "10.1109/ICASSP.2012.6289079"
accessed: 2026-08-26
source_tier: P1
license: "IEEE paper metadata；本库保存独立摘要与链接"
scope_role: historical-origin
temporal_role: wordpiece-origin
related: ["[[WordPiece、词表构建与最长匹配边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Schuster–Nakajima：WordPiece 的早期来源

> [!abstract] 来源定位
> 该语音搜索工作是 WordPiece 的早期正式来源。课程用它追踪历史对象，但不把现代库中所有名为 WordPiece 的词表训练器、continuation prefix 和 unknown 行为归于一份完全统一的算法规范。

## 课程保留

- WordPiece 以子词缓解大词表与开放词问题；
- 现代编码常采用带词首/续接约束的 longest-match-first；
- 词表学习评分在二手资料和实现间有差异，必须引用具体实现与版本；
- “BPE 按频数、WordPiece 按似然增益”只能作为指定算法的比较，不能不带实现来源地概括全部系统。

