---
type: source
status: verified
area: [sources, calibration, neural-networks]
source_type: paper
title: "On Calibration of Modern Neural Networks"
author: [Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger]
year: 2017
url: "https://proceedings.mlr.press/v70/guo17a.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and method conditions"
venue: "ICML 2017"
scope_role: primary
temporal_role: modern-method
related: ["[[概率校准、Proper Scoring Rule 与可靠性图]]"]
created: 2026-08-23
updated: 2026-08-26
---

# On Calibration of Modern Neural Networks

> [!abstract] 来源定位
> 研究现代神经网络的经验失校准，并比较后处理方法，temperature scaling 是其中的强基线。本库调用其协议与经验结论；不把单数据集结果写成所有架构、损失或分布偏移下的定理。

## 本库调用

1. accuracy 与 probability calibration 是不同目标；
2. reliability diagram 与 ECE 的常用经验实现；
3. temperature scaling 只用验证集拟合一个温度参数；
4. 正温度不改变 logit 排序，因而不直接改变 top-1 决策；
5. 后处理校准对 deployment shift 没有自动保证。
