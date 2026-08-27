---
type: source
status: active
area: [sources, transfer-learning, evaluation, linear-probe]
source_type: paper
title: "Do Better ImageNet Models Transfer Better?"
author: [Simon Kornblith, Jonathon Shlens, Quoc V. Le]
year: 2019
url: "https://openaccess.thecvf.com/content_CVPR_2019/html/Kornblith_Do_Better_ImageNet_Models_Transfer_Better_CVPR_2019_paper.html"
accessed: 2026-08-23
source_tier: A
license: "CVF open access; retain citation and experimental conditions"
venue: "CVPR 2019"
scope_role: primary
temporal_role: modern-evaluation
related: ["[[Linear Probe、Fine-Tuning 与迁移评估]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Do Better ImageNet Models Transfer Better?

> [!abstract] 来源定位
> 系统比较 fixed-feature logistic regression、full fine-tuning 与 from-scratch，并显示 upstream accuracy、training regularization 与 downstream transfer 的关系依赖协议。本库用它建立 transfer matrix，而非追逐单一排行榜相关系数。

## 本库调用

1. frozen linear、fine-tuned 与 scratch 是三个 estimand；
2. head regularization 和 preprocessing 会改变 linear-probe 排名；
3. upstream accuracy 不能替代多任务 downstream evaluation；
4. 小型 fine-grained task 可能表现不同；
5. 同架构、同训练合同与 uncertainty reporting 是公平比较前提。
