---
type: source
status: verified
area: [sources, language-models, factuality, evaluation]
source_type: paper
title: "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation"
author: "Sewon Min et al."
year: 2023
url: "https://aclanthology.org/2023.emnlp-main.741/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: atomic-factual-precision
related: ["[[Hallucination、Factuality、Grounding 与 Attribution 分解]]"]
created: 2026-08-26
updated: 2026-08-26
---

# FActScore：原子事实与知识源支持比例

> [!abstract] 来源定位
> FActScore 把长文本分解为 atomic facts，再计算由指定可靠知识源支持的比例。本库调用 claim denominator、decomposition 与 support 判定协议；自动 pipeline 的检索器/judge 误差必须与人标事实性分开。

该分数接近 atomic factual precision，不测遗漏事实的 recall，也不自动测 citation correctness、时效、来源权威性或整段论证质量。
