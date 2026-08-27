---
type: source
status: verified
area: [sources, unicode, segmentation, tokenization]
source_type: standard
title: "Unicode Standard Annex #29: Unicode Text Segmentation"
author: "Unicode Consortium"
year: 2025
url: "https://unicode.org/reports/tr29/"
accessed: 2026-08-26
source_tier: P0
license: "Unicode normative reference；本库仅保存独立摘要与链接"
scope_role: normative-definition
temporal_role: versioned-standard
related: ["[[Unicode、字节、码点、字素簇与规范化合同]]", "[[Tokenizer 评估、多语言公平、安全与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Unicode UAX #29：文本分段

> [!abstract] 来源定位
> UAX #29 给出 grapheme cluster、word 与 sentence 的默认边界规则。课程用 extended grapheme cluster 近似“用户感知字符”的可计算单位；它不是语言学词、tokenizer piece 或渲染 glyph 的同义词。

## 证据边界

- 字素簇可包含多个码点，例如 combining mark 或 ZWJ emoji 序列；
- 默认 word boundary 不是所有语言的形态学分词器；
- 规则与属性数据绑定 Unicode 版本，CLDR 还可提供 tailoring；
- tokenizer 可以跨、沿或忽略这些边界，必须单独声明。

实现验收应使用[最新版 UAX #29](https://unicode.org/reports/tr29/)及相应测试数据，而不是只用少量 emoji 手测。

