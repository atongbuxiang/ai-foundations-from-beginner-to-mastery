---
type: source
status: verified
area: [sources, optimization, large-batch, scaling]
source_type: paper
title: "An Empirical Model of Large-Batch Training"
author: [Sam McCandlish, Jared Kaplan, Dario Amodei, OpenAI Dota Team]
year: 2018
url: "https://arxiv.org/abs/1812.06162"
accessed: 2026-08-26
source_tier: B
scope_role: primary-preprint
related: ["[[梯度噪声协方差、Noise Scale 与 SDE 近似]]", "[[Critical Batch、隐式偏置与 SGD 证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# McCandlish 等 2018：Gradient Noise Scale 与大批量训练模型

> [!abstract] 来源定位
> 论文提出可测的 gradient noise scale，并以跨监督学习、生成模型和强化学习实验建立“最大有用 batch”经验模型。它是广泛但仍经验驱动的证据，不是任意优化器、调度器与硬件上的普遍临界常数定理。

## 课程调用

1. 用 gradient mean 与 covariance 定义 simple noise-scale 估计量；
2. 区分 step efficiency 与 example/compute efficiency；
3. 使用 $S/S_{min}\approx1+B_{noise}/B$、$E/E_{min}\approx1+B/B_{noise}$ 作为受条件约束的拟合模型；
4. 把 critical batch 解释为收益递减的尺度，而非稳定性硬边界。

## 审计问题

- 目标 loss、训练阶段与估计窗口是什么？
- $B$ 是样本、token、sequence 还是 transition？
- estimator 是否无偏、采样是否相关？
- 比较固定 steps、examples、FLOPs 还是 wall time？
- LR、schedule、optimizer 与模型参数化是否共同重调？

