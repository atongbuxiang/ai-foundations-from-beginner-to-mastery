---
type: source
status: verified
area: [sources, ai/scaling-laws, replication, uncertainty]
source_type: paper
title: "Chinchilla Scaling: A Replication Attempt"
author: "Tamay Besiroglu, Ege Erdil, Matthew Barnett, Josh You"
year: 2024
url: "https://arxiv.org/abs/2404.10102"
accessed: 2026-08-26
source_tier: B
license: "arXiv preprint; independent summary only"
scope_role: audit
temporal_role: active-research
related: ["[[Chinchilla、Compute-optimal 参数与数据分配]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Chinchilla Scaling: A Replication Attempt

> [!abstract] 来源定位
> 论文重建并审计 Chinchilla 的第三种拟合程序，指出公开材料中的点估计、拟合质量和置信区间存在难以协调之处。课程用它训练“原论文很重要”与“统计程序仍需复核”可以同时成立。

## 可调用证据

- 三种估计路线不应只比较最终指数，还应比较它们使用的数据与目标函数；
- 从图像重建数据会引入额外测量误差；
- 极窄置信区间必须与独立实验数量、噪声结构和拟合自由度相容；
- 可复现 scaling 结论需要释放原始 runs、损失、参数统计口径与拟合代码。

## 边界

- 这是 replication critique，不抹去 Chinchilla 的总体 IsoFLOP 证据；
- 从图表数字化得到的数据不是原始训练日志；
- 课程不把争议压缩成“某一方指数绝对正确”，而比较可识别性与预测误差。
