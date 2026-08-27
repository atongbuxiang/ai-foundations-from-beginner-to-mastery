---
type: source
status: verified
area: [sources, privacy, machine-unlearning, systems]
source_type: paper
title: "Machine Unlearning"
author: "Lucas Bourtoule et al."
year: 2021
url: "https://arxiv.org/abs/1912.03817"
accessed: 2026-08-26
source_tier: P1
license: "IEEE S&P paper; independent summary"
scope_role: sisa-unlearning-system
related: ["[[Membership、隐私攻击、数据删除与 Unlearning 边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# SISA 与 Machine Unlearning

> [!abstract] 来源定位
> 论文提出 sharded、isolated、sliced、aggregated 的 SISA 训练，以缩小删除后需重训的范围。课程把它作为系统级时间—存储—效用—删除成本权衡，而非“任意现有模型一键遗忘”的证明。

删除验证仍要独立进行；架构、分片、聚合和多次自适应请求会改变保证与成本。
