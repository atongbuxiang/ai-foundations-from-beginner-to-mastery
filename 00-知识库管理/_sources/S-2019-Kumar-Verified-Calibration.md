---
type: source
status: active
area: [sources, calibration, calibration-estimation]
source_type: paper
title: "Verified Uncertainty Calibration"
author: [Aviral Kumar, Sunita Sarawagi, Ujjwal Jain]
year: 2019
url: "https://proceedings.neurips.cc/paper_files/paper/2019/hash/f8c0c968632845cd133308b1a494967f-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and estimator conditions"
venue: "NeurIPS 2019"
scope_role: primary
temporal_role: estimator-audit
related: ["[[概率校准、Proper Scoring Rule 与可靠性图]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Verified Uncertainty Calibration

> [!abstract] 来源定位
> 研究常用校准误差估计的统计困难，并提出带估计控制的替代路线。本库用它提醒：bin 数、样本量与估计程序共同定义经验 calibration error，不能只报一个无误差条的 ECE。

## 本库调用

1. population calibration functional 与 empirical estimator 分层；
2. 固定分箱造成离散化偏差，细分箱增加方差；
3. calibration model 与 calibration evaluation 需要数据隔离；
4. 置信界必须与具体估计量和光滑性假设绑定；
5. “ECE 更低”不是不依赖估计器的普遍排序。
