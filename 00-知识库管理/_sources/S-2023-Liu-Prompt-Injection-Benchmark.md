---
type: source
status: verified
area: [sources, language-models, security, prompt-injection, benchmarks]
source_type: paper
title: "Formalizing and Benchmarking Prompt Injection Attacks and Defenses"
author: "Yi Liu et al."
year: 2023
url: "https://arxiv.org/abs/2310.12815"
accessed: 2026-08-26
source_tier: P1
license: "Research paper; independent summary"
scope_role: prompt-injection-benchmark
related: ["[[Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Prompt Injection 的形式化与 Benchmark

> [!abstract] 来源定位
> 论文把 prompt injection 的任务与攻击/防御成功条件形式化，并构造比较协议。课程采用其“效用和安全同时测”的思想：只让模型拒绝所有外部内容并不是可用防御。

静态攻击集合只能测已知分布；报告必须包含自适应预算、攻击迁移、正常任务效用和失败分母。
