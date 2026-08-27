---
type: source
status: verified
area: [sources, language-models, sampling, reproducibility]
source_type: paper
title: "Turning Down the Heat: A Critical Analysis of Min-p Sampling in Language Models"
author: "Rylan Schaeffer; Joshua Kazdan; Yegor Denisov-Blanch"
year: 2025
url: "https://arxiv.org/abs/2506.13681"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: replication-critique
related: ["[[Top-k、Top-p、Typical 与 Min-p 截断采样]]", "[[解码质量、延迟、吞吐、随机性与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Min-p 实证复核：定义可用不等于优势已确立

> [!abstract] 来源定位
> 该复核重新检查 min-p 的人评、统计、超参数 sweep 与 adoption 主张，并报告原证据不足以支持普遍质量/多样性优势。课程用它示范：算法定义、实现可用性和经验优越性是三个不同主张。

它也不证明 min-p 在所有任务无效；结论应绑定模型、任务、参数预算与评估协议。
