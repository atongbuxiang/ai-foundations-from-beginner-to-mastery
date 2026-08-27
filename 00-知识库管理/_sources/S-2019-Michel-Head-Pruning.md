---
type: source
status: draft
area: [sources, ai/attention, ai/model-compression]
source_type: paper
title: "Are Sixteen Heads Really Better than One?"
author: "Paul Michel, Omer Levy, Graham Neubig"
year: 2019
url: "https://proceedings.neurips.cc/paper/2019/hash/2c601ad9d2ff9bc8b282670cdd54f69f-Abstract.html"
accessed: 2026-08-24
source_tier: A
license: "NeurIPS proceedings; independent summary only"
scope_role: empirical-boundary
temporal_role: modern
related: ["[[Multi-Head Attention、投影子空间与参数量]]", "[[Attention 失效模式、反例与证据地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Are Sixteen Heads Really Better than One?：Head 剪枝证据

> [!abstract] 来源定位
> 论文发现所研究训练模型中的许多 attention heads 可在测试时移除而只造成有限性能下降，并提出 head importance/pruning 分析。它是特定模型、任务和训练结果上的经验事实，不是“多头理论上冗余”或“只需一个头”的普遍定理。

## 课程采用

- 结构参数量与训练后功能利用率是不同问题；
- 零掉单头、联合剪枝与重新训练得到的结论不能混用；
- importance 依任务、层、seed、metric 与补偿机制；
- 固定 $d_{model}$ 时增加 head 数通常不改变标准四个投影的主阶参数量，却会改变每头宽度、score 张量形状和 kernel 行为。

## 最小复现实验

记录 checkpoint、head mask 位置、是否微调、单头/组合干预、任务指标、延迟与显存；报告多 seed 和 pruning curve，而不是只展示最可剪的一次结果。
