---
type: source
status: verified
area: [sources, language-models, llm-as-judge, causal-adjustment]
source_type: paper
title: "Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators"
author: "Yann Dubois et al."
year: 2024
url: "https://arxiv.org/abs/2404.04475"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: length-bias-adjustment
related: ["[[LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Length-Controlled AlpacaEval：长度混杂与反事实分数

> [!abstract] 来源定位
> 论文以回归模型控制候选与基线输出长度差，估计长度相同时的反事实偏好，针对自动裁判的 verbosity bias。本库调用 raw/length-controlled win rate 分账与 mediator 假设。

长度控制依赖模型形式、overlap/positivity 与未测混杂假设；它不是把长答案机械截短，也不能自动修复 position、事实性或 judge-family 偏差。
