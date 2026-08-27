---
type: source
status: verified
area: [sources, generative-models, evaluation, fid, reproducibility]
source_type: paper
title: "On Aliased Resizing and Surprising Subtleties in GAN Evaluation"
author: "Gaurav Parmar; Richard Zhang; Jun-Yan Zhu"
year: 2022
url: "https://github.com/GaParmar/clean-fid"
venue: "CVPR 2022"
accessed: 2026-08-25
source_tier: A
scope_role: bridge
related: ["[[Likelihood、FID、KID、Precision–Recall 与人类评估]]", "[[生成模型实验协议、FD Loss 与前沿证据地图]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Parmar et al.：CleanFID

> [!abstract] 来源定位
> 论文与官方实现展示 resize、quantization 和低层预处理足以显著改变 FID。课程据此要求记录 evaluator 版本、数据 split、样本数、resize/antialias、颜色空间与 reference statistics hash。
