---
type: source
status: verified
area: [sources, pretraining-data, contamination, gpt3]
source_type: paper
title: "Language Models are Few-Shot Learners — contamination protocol"
author: "Tom B. Brown et al."
year: 2020
url: "https://arxiv.org/abs/2005.14165"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: early-decontamination-protocol
temporal_role: historical-foundation
related: ["[[Benchmark 污染、时间截止与成员重叠审计]]"]
created: 2026-08-26
updated: 2026-08-26
---

# GPT-3：训练—评测污染协议

> [!abstract] 来源定位
> GPT-3 论文及其附录讨论 benchmark overlap 检测与被污染样例上的结果，是大规模语言模型公开 decontamination 的早期实例。课程调用 n-gram overlap、阈值与 clean/dirty split 逻辑，同时强调公开数据过滤并不覆盖 paraphrase、翻译、解答泄漏和 post-training exposure。

检测到 overlap 不等于证明模型利用；未检测到也不等于无 exposure。时间截止、训练数据访问权限与阈值敏感性必须并列报告。

