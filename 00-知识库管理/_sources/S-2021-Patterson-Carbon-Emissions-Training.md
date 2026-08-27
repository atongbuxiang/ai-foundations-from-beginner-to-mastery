---
type: source
status: verified
area: [sources, ai/compute, energy, carbon]
source_type: paper
title: "Carbon Emissions and Large Neural Network Training"
author: "David Patterson et al."
year: 2021
url: "https://arxiv.org/abs/2104.10350"
accessed: 2026-08-26
source_tier: A
license: "arXiv paper; independent summary only"
scope_role: energy-ledger
temporal_role: active-research
related: ["[[IsoFLOP、训练算力口径与系统校正]]", "[[过训练、推理成本与多目标最优规模]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Carbon Emissions and Large Neural Network Training

> [!abstract] 来源定位
> 论文估算多种大型模型的 energy 与 CO2e，并展示模型、硬件、数据中心效率和电网碳强度会造成数量级差异。课程用它要求 FLOPs、joules/kWh、货币成本和 CO2e 分账。

## 可调用证据

- energy 需要功率随时间积分，而不是由参数量直接决定；
- CO2e 还需地点/时段相关的碳强度；
- hardware 与 datacenter efficiency 会显著改变相同训练任务的 energy；
- 未公开系统细节的事后估计可能误差很大。

## 边界

- 历史模型和电网数据不能直接代表当前项目；
- carbon accounting 还可包含制造、网络与生命周期，本论文重点不是完整 LCA；
- 低 CO2e 地点不等于低 wall time 或低货币成本。
