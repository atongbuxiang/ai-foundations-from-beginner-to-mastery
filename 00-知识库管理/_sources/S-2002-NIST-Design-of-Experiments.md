---
type: source
status: verified
area: [sources, statistics, design-of-experiments]
source_type: official-handbook
title: "NIST/SEMATECH e-Handbook of Statistical Methods — Process Improvement"
author: NIST/SEMATECH
year: 2002
url: "https://www.itl.nist.gov/div898/handbook/pri/pri.htm"
accessed: 2026-08-26
source_tier: A
scope_role: formal-methods
related: ["[[单因素、全因子消融与交互效应]]", "[[数据优化器调度交互、混杂与归因边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# NIST/SEMATECH：实验设计

> [!abstract] 来源定位
> 官方统计手册给出 factorial design、interaction、blocking、randomization、replication 与 fractional factorial/aliasing 的经典入口。

## 本卷调用

- 用正交编码把 $2^k$ 设计的主效应和交互效应写成 contrasts；
- 通过 randomization 防时间趋势，blocking 吸收已知 nuisance factor，replication 估计随机误差；
- screening 可用低分辨率 fraction，但主效应与交互的 alias 必须显式报告；
- 发现曲率或强交互后，转向更高分辨率设计或 response-surface，而非继续单因素调参。

## 边界

经典 DOE 假定 experimental unit 和误差结构已定义；ML 中 seed、数据抽样、checkpoint 与共享预训练状态会改变 experimental unit，必须另写层级。
