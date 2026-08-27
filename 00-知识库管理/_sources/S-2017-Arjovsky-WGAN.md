---
type: source
status: verified
area: [sources, generative-models, wgan, optimal-transport]
source_type: paper
title: "Wasserstein GAN"
author: "Martin Arjovsky; Soumith Chintala; Léon Bottou"
year: 2017
url: "https://arxiv.org/abs/1701.07875"
venue: "ICML 2017"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: foundational
related: ["[[IPM、Wasserstein-1 与 Kantorovich 对偶]]", "[[Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Arjovsky et al.：Wasserstein GAN

> [!abstract] 来源定位
> 论文以 $W_1$ 对弱收敛更连续的性质解释 support 分离时的训练信号，并以 weight clipping 近似约束 critic。课程采用 metric/topology 与 critic objective，保留两条边界：neural critic 不是全体 1-Lipschitz functions；weight clipping 不是精确 Lipschitz 投影。

## 断言审计

| 断言 | 类型 | 条件/边界 | 课程判断 |
|---|---|---|---|
| $W_1=\sup_{\|f\|_L\le1}(E_Pf-E_Qf)$ | KR 对偶 | metric space、finite first moment 等 | 精确 |
| point-mass 平移下 $W_1$ 随距离连续 | 可算例 | 指定 ground metric | 精确 |
| weight clipping 严格实现全域 1-Lipschitz critic | 实现外推 | 参数—函数 Lipschitz 映射复杂 | 不成立 |
| WGAN 消除所有 mode collapse | 普遍经验外推 | 原论文协议有限 | 不采用 |

