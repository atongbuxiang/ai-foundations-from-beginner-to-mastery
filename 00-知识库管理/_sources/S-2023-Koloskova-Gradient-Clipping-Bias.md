---
type: source
status: verified
area: [sources, optimization, clipping, stochastic-bias]
source_type: paper
title: "Revisiting Gradient Clipping: Stochastic Bias and Tight Convergence Guarantees"
author: "Koloskova, Hendrikx and Stich"
year: 2023
url: "https://arxiv.org/abs/2305.01588"
accessed: 2026-08-26
source_tier: A
scope_role: theory-and-counterexample
related: ["[[全局逐层梯度裁剪、AGC 与裁剪偏差]]", "[[Mini-batch 梯度、平均求和与有效 Batch]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Koloskova 等：随机梯度裁剪的偏差

> [!abstract] 来源定位
> 论文给出任意阈值下 deterministic/stochastic clipping 的紧界与反例，指出随机情形中非线性 clipping 一般破坏无偏性，标准噪声假设下甚至不能保证收敛到真实最优点。

## 课程采用

若 $\widehat g$ 无偏，通常仍有

$$
\mathbb E\!\left[\operatorname{clip}_c(\widehat g)\right]
\ne \operatorname{clip}_c\!\left(\mathbb E[\widehat g]\right),
$$

更不必等于 $\nabla L$。课程要求报告 clip rate、阈值、方向偏差与 heavy-tail/outlier 条件，而不是只说“裁剪防爆炸”。
