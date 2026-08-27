---
type: source
status: verified
area: [sources, language-models, decoding, evaluation]
source_type: paper
title: "On Decoding Strategies for Neural Text Generators"
author: "Gian Wiher; Clara Meister; Ryan Cotterell"
year: 2022
url: "https://aclanthology.org/2022.tacl-1.58/"
accessed: 2026-08-26
source_tier: P1
license: "TACL paper; independent summary"
scope_role: cross-task-decoding-comparison
related: ["[[解码质量、延迟、吞吐、随机性与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Decoding Strategies：质量—多样性权衡依任务而变

> [!abstract] 来源定位
> 论文系统比较多类 generation tasks 和 decoding strategies，强调 mode-seeking、sampling、长度和多样性的效果具有任务依赖性。

课程据此拒绝“一个 sampler 全任务最佳”；每个解码结论都要绑定任务、模型、评估者和预算。
