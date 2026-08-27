---
type: source
status: verified
area: [sources, language-models, constrained-decoding]
source_type: paper
title: "Efficient Guided Generation for Large Language Models"
author: "Brandon T. Willard; Rémi Louf"
year: 2023
url: "https://arxiv.org/abs/2307.09702"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: automaton-vocabulary-index
related: ["[[Grammar-constrained Decoding、Schema 与结构化输出]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Guided Generation：前缀状态机与词表索引

> [!abstract] 来源定位
> 论文把 guided generation 构造成有限状态机的状态转移，并为 LM 词表建立可用 token 索引，以支持 regex/grammar 约束。课程用它解释 prefix state、token-byte mismatch 与 logits mask。

对合法 token 重新归一化会改变分布；逐步合法还需保证前缀可完成，避免走入无可接受终止的死路。
