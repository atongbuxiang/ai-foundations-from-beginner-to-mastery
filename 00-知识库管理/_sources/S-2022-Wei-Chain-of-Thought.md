---
type: source
status: verified
area: [sources, reasoning, chain-of-thought]
source_type: paper
title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
author: "Jason Wei et al."
year: 2022
url: "https://papers.neurips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html"
accessed: 2026-08-26
source_tier: P1
license: "NeurIPS; independent summary"
scope_role: prompting-phenomenon
related: ["[[Chain-of-Thought、Scratchpad 与 Faithfulness]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Chain-of-Thought Prompting

> [!abstract] 来源定位
> 论文在少样本 prompt 中加入中间推理文本，在算术、常识和符号任务上报告大模型性能提升。课程采用 direct answer 与 rationale-conditioned generation 的协议差分。

准确率提升不证明文字链忠实呈现内部因果计算，也不证明步骤局部正确；模型、样例、任务和额外输出 token 预算必须固定报告。
