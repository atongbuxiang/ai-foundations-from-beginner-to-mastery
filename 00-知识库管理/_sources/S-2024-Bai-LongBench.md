---
type: source
status: draft
area: [sources, ai/long-context, evaluation]
source_type: paper
title: "LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding"
author: "Yushi Bai et al."
year: 2024
url: "https://aclanthology.org/2024.acl-long.172/"
accessed: 2026-08-24
source_tier: A
license: "ACL Anthology; independent summary only"
scope_role: benchmark
temporal_role: long-context-evaluation
related: ["[[位置分辨率、混叠与长度外推评测]]"]
created: 2026-08-24
updated: 2026-08-24
---

# LongBench：多任务长上下文评测

> [!abstract] 来源定位
> LongBench 组织中英双语、单/多文档问答、摘要、few-shot、synthetic 与代码等任务，提醒长上下文能力不能由单一 needle 或 PPL 代表。

## 课程采用

评测报告按任务、语言、长度、答案位置和 metric 分层；同时保留 tokenizer 后实际 token length、截断策略、prompt 与 decoding。Benchmark 分数是 E，不是 context window 的定义。

## 边界

公开静态任务存在数据污染、自动 metric 与长度分布限制；多任务平均会掩盖某类远程依赖失败。
