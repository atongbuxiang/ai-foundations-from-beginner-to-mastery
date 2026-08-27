---
type: source
status: active
area: [sources, self-supervised-learning, stop-gradient, collapse]
source_type: paper
title: "Exploring Simple Siamese Representation Learning"
author: [Xinlei Chen, Kaiming He]
year: 2021
url: "https://openaccess.thecvf.com/content/CVPR2021/html/Chen_Exploring_Simple_Siamese_Representation_Learning_CVPR_2021_paper.html"
accessed: 2026-08-23
source_tier: A
license: "CVF open access; retain citation and method conditions"
venue: "CVPR 2021"
scope_role: primary
temporal_role: modern-method
related: ["[[表示坍缩、非坍缩与可辨识边界]]", "[[遮蔽预测、Teacher–Student 与自监督目标]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Exploring Simple Siamese Representation Learning

> [!abstract] 来源定位
> 展示 shared-weight Siamese、predictor 与 stop-gradient 在无 negatives、无 momentum encoder 时的经验非坍缩。本库保留论文把机制解释称为 hypothesis 的证据等级。

## 本库调用

1. stop-gradient 改变 vector field，而不改变 forward scalar value；
2. constant representation 仍可能是 loss 的解；
3. “解存在”不等于“训练会收敛到该解”；
4. predictor 与 branch asymmetry 不能从算法合同中省略；
5. ablation 支持必要性判断，但不自动给出一般充分条件。
