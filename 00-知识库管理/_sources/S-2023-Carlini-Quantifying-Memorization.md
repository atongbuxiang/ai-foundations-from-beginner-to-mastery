---
type: source
status: verified
area: [sources, language-models, privacy, memorization, scaling]
source_type: paper
title: "Quantifying Memorization Across Neural Language Models"
author: "Nicholas Carlini et al."
year: 2023
url: "https://openreview.net/forum?id=TatRHT_1cK"
accessed: 2026-08-26
source_tier: P1
license: "ICLR paper; independent summary"
scope_role: memorization-scaling-evidence
related: ["[[Memorization、Exposure、Canary 与训练数据抽取]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 跨语言模型量化 Memorization

> [!abstract] 来源定位
> 论文系统研究模型规模、重复、上下文与抽取式记忆之间的经验关系。课程借它说明记忆率必须绑定匹配规则、提示长度和数据重复度，不能从单条逐字复现外推总体隐私风险。

经验曲线不是跨架构定律；若 tokenizer、语料、训练轮数或攻击流程变化，应重新估计而不是复用论文常数。
