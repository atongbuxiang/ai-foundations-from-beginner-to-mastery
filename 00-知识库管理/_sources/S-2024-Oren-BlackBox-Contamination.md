---
type: source
status: verified
area: [sources, language-models, contamination, hypothesis-testing]
source_type: paper
title: "Proving Test Set Contamination in Black-Box Language Models"
author: "Yonatan Oren et al."
year: 2024
url: "https://proceedings.iclr.cc/paper_files/paper/2024/hash/46e624c244cff669223d488defd4e835-Abstract-Conference.html"
accessed: 2026-08-26
source_tier: P1
license: "ICLR paper; independent summary"
scope_role: black-box-contamination-test
related: ["[[Contamination、Prompt Sensitivity、Robustness 与不确定性]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 黑箱测试集污染：Canonical Order 与精确假阳保证

> [!abstract] 来源定位
> 论文利用无污染零假设下 benchmark 示例排序的 exchangeability，比较 canonical order 与随机排列的 likelihood，从黑箱模型中给出带假阳控制的污染证据。本库采用零假设、检验统计量和 power/assumption 分账。

拒绝零假设是特定污染机制的统计证据，不定位训练文件，也不证明分数提升完全由记忆导致；不拒绝也可能只是检验 power 不足。
