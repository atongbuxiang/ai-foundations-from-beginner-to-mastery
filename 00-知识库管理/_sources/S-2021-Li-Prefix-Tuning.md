---
type: source
status: verified
area: [sources, peft, prefix-tuning]
source_type: paper
title: "Prefix-Tuning: Optimizing Continuous Prompts for Generation"
author: "Xiang Lisa Li and Percy Liang"
year: 2021
url: "https://aclanthology.org/2021.acl-long.353/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: prefix-tuning-definition
temporal_role: foundational-method
related: ["[[Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Prefix-Tuning

> [!abstract] 来源定位
> Prefix-tuning 冻结语言模型，优化任务专属连续 prefix，使后续 token 在各层注意这些虚拟状态。课程区分 input-embedding soft prompt 与 per-layer key/value prefix，并计算额外 KV、context 与 serving 成本。

论文在 GPT-2/BART 生成任务中的结果不证明 prefix 对所有 decoder-only LLM、长上下文或多任务服务优于 LoRA/full tuning。

