---
type: source
status: verified
area: [sources, reasoning, faithfulness]
source_type: paper
title: "Measuring Faithfulness in Chain-of-Thought Reasoning"
author: "Tamera Lanham et al."
year: 2023
url: "https://arxiv.org/abs/2307.13702"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: rationale-intervention
related: ["[[Chain-of-Thought、Scratchpad 与 Faithfulness]]"]
created: 2026-08-26
updated: 2026-08-26
---

# CoT 截断、错误与改写干预

> [!abstract] 来源定位
> 论文通过截断、改写、插入错误等方式干预已生成 reasoning trace，再测答案变化，发现不同任务和模型对可见 CoT 的依赖差异很大。课程采用 intervention matrix，而不是把流畅度当 faithfulness。

黑盒干预测的是对可见 trace 的条件依赖；它仍不能直接观察隐藏激活中的完整计算，也可能受改写分布外和答案重采样噪声影响。
