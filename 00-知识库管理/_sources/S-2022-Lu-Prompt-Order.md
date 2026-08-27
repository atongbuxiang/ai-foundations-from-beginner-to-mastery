---
type: source
status: verified
area: [sources, in-context-learning, prompt-order]
source_type: paper
title: "Fantastically Ordered Prompts and Where to Find Them"
author: "Yao Lu et al."
year: 2022
url: "https://aclanthology.org/2022.acl-long.556/"
accessed: 2026-08-26
source_tier: P1
license: "ACL Anthology; independent summary"
scope_role: order-sensitivity
related: ["[[Zero-shot、Few-shot ICL、示例顺序与标签映射]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 示例顺序敏感性

> [!abstract] 来源定位
> 论文系统枚举少样本示例排列，展示不同次序可产生巨大性能差异，并用无标注 probing set 的熵统计选择候选顺序。课程采用 permutation sweep、选择偏差和额外调参预算的审计框架。

“好顺序”绑定模型、模板、样例集合和任务；先看测试标签再选顺序会把 prompt search 变成未报告的监督调参。
