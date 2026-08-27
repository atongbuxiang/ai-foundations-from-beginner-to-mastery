---
type: source
status: active
area: [sources, neural-networks, prelu, initialization]
source_type: paper
title: "Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification"
author: [Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun]
year: 2015
url: "https://openaccess.thecvf.com/content_iccv_2015/html/He_Delving_Deep_into_ICCV_2015_paper.html"
accessed: 2026-08-23
source_tier: A
venue: "ICCV 2015:1026–1034"
scope_role: foundation
temporal_role: classic
related: ["[[ReLU、Leaky ReLU 与次梯度约定]]", "[[Kaiming、He 初始化]]"]
created: 2026-08-23
updated: 2026-08-23
---
# He et al. 2015：PReLU 与 Rectifier Initialization

> [!abstract] 来源定位
> 原论文提出 PReLU，并依据 rectifier 二阶矩推导 initialization，结合 ImageNet 深 CNN 给出实验。本库用它连接 learnable negative slope 与 Kaiming/He 初始化；“几乎零额外代价”和当年 ImageNet 结果都须保留原架构与评测边界。
