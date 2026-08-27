---
type: source
status: verified
area: [sources, peft, adapters]
source_type: paper
title: "Parameter-Efficient Transfer Learning for NLP"
author: "Neil Houlsby et al."
year: 2019
url: "https://arxiv.org/abs/1902.00751"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: adapter-modules
temporal_role: foundational-method
related: ["[[Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Parameter-Efficient Transfer Learning：Adapters

> [!abstract] 来源定位
> 论文在冻结主干中插入任务专属 bottleneck adapter，并在 BERT/GLUE 等协议下比较参数效率。课程调用其 residual bottleneck 位置、参数量和多任务存储动机。

Adapter 可能增加每层计算和推理 latency；参数比例、性能接近程度和最优插入位置不应脱离模型宽度、任务与实现外推。

