---
type: source
status: verified
area: [sources, language-models, speculative-decoding]
source_type: paper
title: "Fast Inference from Transformers via Speculative Decoding"
author: "Yaniv Leviathan; Matan Kalman; Yossi Matias"
year: 2023
url: "https://proceedings.mlr.press/v202/leviathan23a.html"
accessed: 2026-08-26
source_tier: P1
license: "PMLR paper; independent summary"
scope_role: exact-speculative-decoding
related: ["[[Speculative Decoding、Acceptance 与分布精确性]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Speculative Decoding：draft、并行验证与精确校正

> [!abstract] 来源定位
> 论文让廉价 draft model 提议多个 token，由 target 并行验证，并以接受/残差采样保持 target 分布。课程采用单步 rejection correction 的证明和 acceptance—speedup 账。

“输出不变”指算法分布在假设与数值精度下等于 target sampler；若处理器、tokenizer、约束或随机数合同不一致，结论不自动成立。
