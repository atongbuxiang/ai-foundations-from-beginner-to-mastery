---
type: source
status: verified
area: [sources, language-models, privacy, memorization]
source_type: paper
title: "The Secret Sharer: Evaluating and Testing Unintended Memorization in Neural Networks"
author: "Nicholas Carlini et al."
year: 2019
url: "https://www.usenix.org/conference/usenixsecurity19/presentation/carlini"
accessed: 2026-08-26
source_tier: P1
license: "USENIX paper; independent summary"
scope_role: canary-exposure-foundation
related: ["[[Memorization、Exposure、Canary 与训练数据抽取]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Secret Sharer：Canary 与 Exposure

> [!abstract] 来源定位
> 论文用人工插入、可控稀有度的 canary 测试非预期逐字记忆，并以候选空间中的 rank 定义 exposure。它给出受控测量工具，不等于证明真实敏感训练样本都可由任意攻击者提取。

课程保留 canary 分布、插入次数、候选空间、攻击可见信息和查询预算；只使用合成字符串，不把真实凭据写入实验。
