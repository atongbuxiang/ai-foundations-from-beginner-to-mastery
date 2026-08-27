---
type: source
status: verified
area: [sources, reasoning, faithfulness]
source_type: paper
title: "Language Models Don't Always Say What They Think"
author: "Miles Turpin et al."
year: 2023
url: "https://arxiv.org/abs/2305.04388"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: bias-intervention
related: ["[[Chain-of-Thought、Scratchpad 与 Faithfulness]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 偏置干预下的 CoT 不忠实

> [!abstract] 来源定位
> 论文向多选 prompt 注入答案位置等偏置，观察最终预测被影响而生成解释经常不提该因素，并出现为偏置答案合理化。课程采用 bias intervention、mention rate 与 answer flip 的联合审计。

未提到一个影响因素可证明该解释在相应完整性定义下不足，但不等于恢复了全部内部计算；faithfulness 需要先声明因果、充分性、完整性或可执行性定义。
