---
type: source
status: verified
area: [sources, unicode, normalization, tokenization]
source_type: standard
title: "Unicode Standard Annex #15: Unicode Normalization Forms"
author: "Unicode Consortium; editor Ken Whistler"
year: 2025
url: "https://unicode.org/reports/tr15/"
accessed: 2026-08-26
source_tier: P0
license: "Unicode normative reference；本库仅保存独立摘要、短例与链接"
scope_role: normative-definition
temporal_role: versioned-standard
related: ["[[Unicode、字节、码点、字素簇与规范化合同]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Unicode UAX #15：规范化形式

> [!abstract] 来源定位
> UAX #15 是 Unicode normalization 的规范性入口，定义 canonical/compatibility equivalence 与 NFC/NFD/NFKC/NFKD。课程以它决定“什么叫规范化”，而不以 tokenizer 文档或编程语言的便捷函数替代标准。

## 课程采用

| 对象 | 课程结论 | 边界 |
|---|---|---|
| NFC/NFD | canonical decomposition；NFC 再做 canonical composition | 二进制长度可变，但保持 canonical equivalence |
| NFKC/NFKD | compatibility decomposition；NFKC 再 composition | 可能折叠圈号、宽度、上标等有意义区别 |
| 版本 | normalization 绑定 Unicode 数据与 conformance test | 不能只记录函数名 |
| 拼接 | 两个已规范化串的拼接未必仍规范化 | 流式/边界处理需重新检查 |

规范性细节与勘误以[最新版 UAX #15](https://unicode.org/reports/tr15/)为准。

