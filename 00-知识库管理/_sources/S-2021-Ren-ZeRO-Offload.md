---
type: source
status: verified
area: [sources, distributed-training, offload]
source_type: paper
title: "ZeRO-Offload: Democratizing Billion-Scale Model Training"
author: "Jie Ren et al."
year: 2021
url: "https://www.usenix.org/conference/atc21/presentation/ren-jie"
accessed: 2026-08-26
source_tier: A
license: "USENIX open-access paper；知识库仅保存独立摘要与链接"
scope_role: offload
temporal_role: foundational
related: ["[[ZeRO、FSDP、激活重计算与 Offload]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# ZeRO-Offload

> [!abstract] 来源定位
> 论文把部分 model state 与 optimizer compute 放到 CPU，建立 GPU capacity、CPU compute 与 PCIe 数据移动的三方权衡，是“offload 省显存但不免费”的原始来源。

## 可调用证据

- offload 的可行性取决于每 step 需移动的 bytes 是否能被计算重叠；
- optimizer states/updates 适合放 CPU 的判断来自计算强度与驻留量；
- pinned memory、分区和调度影响 PCIe/NVLink 利用率；
- 论文在列明 V100 系统上展示单 GPU/多 GPU 大模型训练能力。

## 边界

- 论文吞吐与模型上限绑定当时 CPU/GPU/互联；
- NVMe、CPU 参数、optimizer offload 是不同路径；
- 可 fit 不等于 time-to-quality 更优。
