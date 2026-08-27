---
type: source
status: active
area: [sources, natural-distribution-shift, robustness, benchmark]
source_type: paper
title: "WILDS: A Benchmark of in-the-Wild Distribution Shifts"
author: [Pang Wei Koh, Shiori Sagawa, Henrik Marklund, Sang Michael Xie, Marvin Zhang, Akshay Balsubramani, Weihua Hu, Michihiro Yasunaga, Richard Lanas Phillips, Irena Gao, Tony Lee, Etienne David, Ian Stavness, Wei Guo, Berton A. Earnshaw, Imran S. Haque, Sara Beery, Jure Leskovec, Anshul Kundaje, Emma Pierson, Sergey Levine, Chelsea Finn, Percy Liang]
year: 2021
url: "https://proceedings.mlr.press/v139/koh21a.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and dataset conditions"
venue: "ICML 2021"
scope_role: primary
temporal_role: benchmark
related: ["[[OOD、鲁棒性与因果不变性的边界]]", "[[Domain Adaptation 与 Domain Generalization Bound]]"]
created: 2026-08-23
updated: 2026-08-23
---

# WILDS

> [!abstract] 来源定位
> 汇集真实时间、地点、群体和机构变化下的多任务 benchmark。本库调用其 natural-shift 与 metadata-aware evaluation；不把 benchmark 平均分等同于对所有现实干预的鲁棒性。

## 本库调用

1. natural shift 与 synthetic corruption 分层；
2. metadata/domain split 与真实 unit；
3. average 与 worst-group/subpopulation metrics；
4. dataset-specific selection and leakage；
5. 多任务结果支持有限外推，不证明 causality。
