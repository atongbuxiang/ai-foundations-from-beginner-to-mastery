---
type: source
status: verified
area: [sources, ai/scaling-laws, emergence, evaluation]
source_type: paper
title: "Are Emergent Abilities of Large Language Models a Mirage?"
author: "Rylan Schaeffer, Brando Miranda, Sanmi Koyejo"
year: 2023
url: "https://openreview.net/forum?id=ITw9edRDlD"
accessed: 2026-08-26
source_tier: A
license: "NeurIPS paper; independent summary only"
scope_role: metric-audit
temporal_role: active-research
related: ["[[Broken Scaling、涌现表象与优化架构数据分解]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Are Emergent Abilities of Large Language Models a Mirage?

> [!abstract] 来源定位
> 论文给出并验证一种替代解释：底层表现可以随尺度平滑变化，而非线性/不连续指标与有限测试样本把它显示成突变。课程用它建立 emergence claim 的 metric intervention。

## 可调用证据

- exact match、argmax/grade 等离散指标可把平滑概率变化压成阈值；
- 连续、线性或更细粒度指标可能恢复平滑趋势；
- 小模型低成功率配合有限样本会产生大量观测零；
- 在语言与视觉例子中改变 metric 能制造或削弱表面 emergence。

## 边界

- 论文没有证明所有 emergence 都是度量幻觉；
- 指标平滑后仍有 kink 时，还需检查数据、架构、优化与真正 regime change；
- 固定输出上的 metric audit 不能替代机制干预。
