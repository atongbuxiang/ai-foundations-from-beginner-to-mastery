---
type: source
status: verified
area: [sources, ai/compute, language-models, systems]
source_type: paper
title: "PaLM: Scaling Language Modeling with Pathways"
author: "Aakanksha Chowdhery et al."
year: 2023
url: "https://www.jmlr.org/papers/v24/22-1144.html"
accessed: 2026-08-26
source_tier: A
license: "JMLR paper; independent summary only"
scope_role: compute-system
temporal_role: foundational
related: ["[[IsoFLOP、训练算力口径与系统校正]]", "[[过训练、推理成本与多目标最优规模]]"]
created: 2026-08-26
updated: 2026-08-26
---

# PaLM: Scaling Language Modeling with Pathways

> [!abstract] 来源定位
> PaLM 论文除模型结果外，还报告 model FLOPs utilization、hardware FLOPs utilization、吞吐和 rematerialization 等系统量。课程用它证明 theoretical model FLOPs、hardware executed FLOPs 与 wall time 不是同一个对象。

## 可调用证据

- 论文分别报告 MFU 与 hardware FLOPs utilization；
- rematerialization 会增加执行 FLOPs，却可能通过可行 batch 提高端到端吞吐；
- attention、embedding、共享输出层和训练公式影响参数/compute 口径；
- 同样理论 FLOPs 在不同 compiler、parallelism、network 与 hardware 上可有不同 wall time。

## 边界

- PaLM 的利用率不是其他集群的默认常数；
- utilization 高不自动意味着 energy、成本或 time-to-quality 最优；
- 论文系统设置与当前硬件代际不同，课程只调用对象分账。
