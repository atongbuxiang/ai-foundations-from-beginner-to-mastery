---
type: source
status: verified
area: [sources, language-models, in-context-learning]
source_type: paper
title: "Language Models are Few-Shot Learners — in-context learning protocol"
author: "Tom B. Brown et al."
year: 2020
url: "https://arxiv.org/abs/2005.14165"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: foundational-phenomenon
related: ["[[Prompt 作为条件事件、序列化与敏感性]]", "[[Zero-shot、Few-shot ICL、示例顺序与标签映射]]"]
created: 2026-08-26
updated: 2026-08-26
---

# GPT-3：零样本、单样本与上下文少样本协议

> [!abstract] 来源定位
> 论文把自然语言说明和输入—输出示例直接放入自回归上下文，在不更新参数的条件下比较 zero-shot、one-shot 与 few-shot。课程采用“学习发生在条件序列变化而非部署时权重更新”这一操作定义，并保留模型规模、模板、样例数和污染审计。

论文展示的是特定模型族和任务上的规模化现象，不证明任意 prompt 都等价于统计学习算法，也不排除预训练记忆、格式匹配和任务先验的贡献。
