---
type: source
status: verified
area: [sources, tokenization, bpe, nlp]
source_type: paper
title: "Neural Machine Translation of Rare Words with Subword Units"
author: "Rico Sennrich, Barry Haddow, Alexandra Birch"
year: 2016
url: "https://arxiv.org/abs/1508.07909"
accessed: 2026-08-26
source_tier: P1
license: "论文；本库仅保存独立摘要、教学例与链接"
scope_role: foundational
temporal_role: subword-bpe
related: ["[[BPE、合并规则与确定性编码解码]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Sennrich 等：子词 BPE 与稀有词建模

> [!abstract] 来源定位
> 该工作把 BPE 型合并用于开放词表神经机器翻译，使稀有词可由子词序列表示。课程采用其“从基本符号反复合并频繁 pair”的算法骨架；现代 byte-level BPE、正则预切分和框架文件格式必须另行定义。

## 课程合同

训练得到的是有序 merge 列表，而不只是最终 token 集。编码时按 rank 反复应用可用 merge；初始符号、词尾/空格标记、是否跨词边界、pair 计数和并列规则都会改变结果。

原论文的机器翻译实验是特定任务证据 `E`，不能证明 BPE 在所有语言、模型和预算下优于 WordPiece 或 Unigram。

