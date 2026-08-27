---
type: source
status: verified
area: [sources, reasoning, search]
source_type: paper
title: "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
author: "Shunyu Yao et al."
year: 2023
url: "https://papers.neurips.cc/paper_files/paper/2023/hash/271db9922b8d1f4dd7aaef84ed5ac703-Abstract-Conference.html"
accessed: 2026-08-26
source_tier: P1
license: "NeurIPS; independent summary"
scope_role: search-framework
related: ["[[Test-time Compute、Search、Verifier 与预算]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Tree of Thoughts：状态、扩展、评价与回溯

> [!abstract] 来源定位
> 方法把 coherent thought 当搜索节点，通过生成候选、价值评估、BFS/DFS 与回溯探索解空间。课程采用 search state、branching factor、depth、proposal 与 evaluator 的可复现合同。

搜索收益不能只与单条 greedy CoT 比较；必须匹配模型调用、生成 token、并行度、延迟和 evaluator 访问预算，并检查搜索器是否借用任务特定规则。
