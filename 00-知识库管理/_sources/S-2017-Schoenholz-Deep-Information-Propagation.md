---
type: source
status: active
area: [sources, neural-networks, mean-field, signal-propagation]
source_type: paper
title: "Deep Information Propagation"
author: [Samuel S. Schoenholz, Justin Gilmer, Surya Ganguli, Jascha Sohl-Dickstein]
year: 2017
url: "https://research.google/pubs/deep-information-propagation/"
accessed: 2026-08-23
source_tier: A
venue: "ICLR 2017"
related: ["[[方差传播与宽层均值场近似]]", "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]", "[[相关传播、Edge of Chaos 与临界初始化]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Schoenholz et al. 2017：Deep Information Propagation

> [!abstract] 来源定位
> 论文以宽随机网络的 mean-field theory 研究 variance、correlation、depth scale 与 backpropagation，正式连接 ordered/chaotic phase 和梯度消失/爆炸。本库在 NN-25/28 只采用标量 moment 与梯度递推接口；相关传播、临界线和深度尺度留给 NN-29。
