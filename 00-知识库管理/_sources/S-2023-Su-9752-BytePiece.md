---
type: source
status: verified
area: [sources, scientific-spaces, tokenization, bytepiece]
source_type: blog
title: "BytePiece：更纯粹、更高压缩率的 Tokenizer"
author: "苏剑林"
year: 2023
url: "https://spaces.ac.cn/archives/9752"
accessed: 2026-08-26
source_tier: P3
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、短公式与链接"
site_category: [自然语言处理]
scope_role: core-exposition
temporal_role: byte-tokenizer-hypothesis
related: ["[[Tokenizer 作为码本、分段路径与压缩接口]]", "[[Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]", "[[Tokenizer 评估、多语言公平、安全与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 科学空间：BytePiece

> [!abstract] 来源定位
> 文章把 tokenizer 分成基本单元、分词算法和训练算法，主张从 byte 出发可保证有限基本覆盖，并以 BNLM/Unigram 风格路径和剪枝构建 BytePiece。它是 LM-03/07/08 的中文问题入口，而不是“byte-based 必然公平或下游最优”的定理。

## 断言审计

| 断言 | 类型 | 课程处理 |
|---|---|---|
| 256 个 byte 基本单元可覆盖任意 byte stream | `I` | 在明确定义 byte token 映射时成立 |
| byte 统计更语言无关/更均匀 | `H/E` | 需按语料、encoding、语言与指标切片验证 |
| 文中测试下 BytePiece 压缩率更高 | `E` | 绑定语料、词表大小、normalization 与实现版本 |
| 压缩率更高意味着 LM 更好 | 不成立的外推 | 还需参数、序列成本、训练预算和下游实验 |

课程会复算路径概率和 bytes/token，但不复述整页代码或实验表。

