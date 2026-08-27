---
type: source
status: verified
area: [sources, reasoning, verifiers]
source_type: paper
title: "Training Verifiers to Solve Math Word Problems"
author: "Karl Cobbe et al."
year: 2021
url: "https://arxiv.org/abs/2110.14168"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: outcome-verification
related: ["[[Self-Consistency、Best-of-N 与 Pass-at-k]]", "[[Test-time Compute、Search、Verifier 与预算]]"]
created: 2026-08-26
updated: 2026-08-26
---

# GSM8K 与 outcome verifier

> [!abstract] 来源定位
> 论文生成多个数学解答候选，再训练 verifier 按最终正确性排序。课程据此严格分离 generator coverage 与 selector accuracy，并记录候选数、长度、去重和 verifier 训练数据。

更多候选只有在覆盖率增长且 verifier 能排序时才转化为 top-1 提升；同分布 verifier 也可能偏好风格、长度或伪证据。
