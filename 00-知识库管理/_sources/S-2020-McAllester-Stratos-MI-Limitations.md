---
type: source
status: active
area: [sources, mutual-information, estimation-limits]
source_type: paper
title: "Formal Limitations on the Measurement of Mutual Information"
author: [David McAllester, Karl Stratos]
year: 2020
url: "https://proceedings.mlr.press/v108/mcallester20a.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "AISTATS 2020"
scope_role: primary
temporal_role: modern-theory
related: ["[[对比学习、InfoNCE 与密度比]]", "[[互信息与依赖性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Formal Limitations on the Measurement of Mutual Information

> [!abstract] 来源定位
> 证明 distribution-free high-confidence MI lower bound 从 N 个样本得到时一般不能超过 order log N。本库用它约束“从有限 batch 准确测得 hundreds of bits”的宣称。

## 本库调用

1. high-dimensional MI measurement 有普遍 sample barrier；
2. lower-bound optimization 与 accurate MI measurement 必须分开；
3. log-N ceiling 不是单一 critic 缺陷；
4. 更强结论需要 distribution、support 或 parametric assumptions；
5. empirical downstream correlation 不证明 MI 解释；
