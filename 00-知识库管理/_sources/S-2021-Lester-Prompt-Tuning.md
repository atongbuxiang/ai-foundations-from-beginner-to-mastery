---
type: source
status: verified
area: [sources, peft, prompt-tuning]
source_type: paper
title: "The Power of Scale for Parameter-Efficient Prompt Tuning"
author: "Brian Lester, Rami Al-Rfou, Noah Constant"
year: 2021
url: "https://aclanthology.org/2021.emnlp-main.243/"
accessed: 2026-08-26
source_tier: P1
license: "EMNLP paper; independent summary"
scope_role: soft-prompt-definition
temporal_role: foundational-method
related: ["[[Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Prompt Tuning

> [!abstract] 来源定位
> Prompt tuning 在冻结模型前优化一小段输入层连续 embeddings，并研究其随模型规模的经验表现。课程用它区分离散文字 prompt、input soft prompt 与 prefix tuning 的注入深度。

“随规模缩小与 full tuning 差距”是特定 T5/任务的经验结果；虚拟 token 仍消耗 context、prefill 与可能的 batch/task 管理成本。

