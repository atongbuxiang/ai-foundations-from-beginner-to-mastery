---
type: source
status: verified
area: [sources, reasoning, self-consistency]
source_type: paper
title: "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
author: "Xuezhi Wang et al."
year: 2023
url: "https://openreview.net/forum?id=1PL1NIMMrw"
accessed: 2026-08-26
source_tier: P1
license: "ICLR/OpenReview; independent summary"
scope_role: sampling-and-aggregation
related: ["[[Self-Consistency、Best-of-N 与 Pass-at-k]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Self-Consistency：路径采样与答案边缘化

> [!abstract] 来源定位
> 方法从 CoT 分布采样多条路径，再按规范化后的最终答案聚合。课程将它写成样本答案计数、majority rule、tie rule 与采样温度的完整合同。

多数一致不保证正确；相关样本会降低有效样本量，答案抽取器和等价类规范化可能改变结论，且额外 token/API 预算必须计入。
