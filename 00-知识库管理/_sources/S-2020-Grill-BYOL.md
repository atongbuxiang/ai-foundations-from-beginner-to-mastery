---
type: source
status: active
area: [sources, self-supervised-learning, teacher-student, collapse]
source_type: paper
title: "Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning"
author: [Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec, Pierre H. Richemond, Elena Buchatskaya, Carl Doersch, Bernardo Avila Pires, Zhaohan Guo, Mohammad Gheshlaghi Azar, Bilal Piot, Koray Kavukcuoglu, Rémi Munos, Michal Valko]
year: 2020
url: "https://proceedings.neurips.cc/paper/2020/hash/f3ada80d5c4ee70142b17b8192b2958e-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and method conditions"
venue: "NeurIPS 2020"
scope_role: primary
temporal_role: modern-method
related: ["[[表示坍缩、非坍缩与可辨识边界]]", "[[遮蔽预测、Teacher–Student 与自监督目标]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Bootstrap Your Own Latent

> [!abstract] 来源定位
> 以 online predictor 对齐 EMA target representation，在无显式 negative pairs 时获得强经验结果。本库调用其算法合同与 ablation，不把“训练未坍缩”写成对所有优化器、归一化和数据分布的普遍证明。

## 本库调用

1. online 与 target 网络角色不对称；
2. target 参数由 EMA 更新而不是反向传播；
3. predictor、normalization、augmentation 与 optimizer 同属算法；
4. constant solution 的可行性与训练动力学稳定性必须区分；
5. downstream linear evaluation 是独立于 pretext loss 的证据。
