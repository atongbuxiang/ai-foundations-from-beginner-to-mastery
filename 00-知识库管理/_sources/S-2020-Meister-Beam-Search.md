---
type: source
status: verified
area: [sources, language-models, decoding]
source_type: paper
title: "If Beam Search is the Answer, What Was the Question?"
author: "Clara Meister; Ryan Cotterell; Tim Vieira"
year: 2020
url: "https://aclanthology.org/2020.emnlp-main.170/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: beam-search-objective
related: ["[[Greedy、Beam Search、Sequence Score 与 Length Penalty]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Beam Search：搜索误差、MAP 与任务质量并非同一对象

> [!abstract] 来源定位
> 论文研究 beam search 在神经文本生成中的实际性质，强调 exact MAP 常产生低质量文本，而有限 beam 即使有搜索误差也可能更符合任务偏好。课程据此分离模型 score、搜索最优性和外部任务 metric。

更宽 beam 只改变搜索近似；若目标函数含长度偏差或与人类质量错位，搜索更准不保证任务更好。
