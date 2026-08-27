---
type: source
status: active
area: [sources, masked-autoencoding, vision-transformer, self-supervision]
source_type: paper
title: "Masked Autoencoders Are Scalable Vision Learners"
author: [Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollár, Ross Girshick]
year: 2022
url: "https://openaccess.thecvf.com/content/CVPR2022/html/He_Masked_Autoencoders_Are_Scalable_Vision_Learners_CVPR_2022_paper.html"
accessed: 2026-08-23
source_tier: A
license: "CVF open access; retain citation and method conditions"
venue: "CVPR 2022"
scope_role: primary
temporal_role: modern-method
related: ["[[遮蔽预测、Teacher–Student 与自监督目标]]", "[[Linear Probe、Fine-Tuning 与迁移评估]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Masked Autoencoders Are Scalable Vision Learners

> [!abstract] 来源定位
> 以高比例 patch masking、visible-only encoder 与轻量 decoder 重建 pixels。本库用它比较 language token prediction 与 vision reconstruction 的 target geometry、decoder capacity 和信息密度。

## 本库调用

1. encoder 只处理 visible patches；
2. mask tokens 在 decoder 侧加入；
3. loss 通常只在 masked patches 上计算；
4. mask ratio 同时改变信息量、难度与计算成本；
5. pixel reconstruction quality 不等于 semantic representation quality。
