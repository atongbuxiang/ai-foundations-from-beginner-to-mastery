---
type: source
status: verified
area: [sources, optimization, averaging, swa]
source_type: paper
title: "Averaging Weights Leads to Wider Optima and Better Generalization"
author: "Izmailov et al."
year: 2018
url: "https://arxiv.org/abs/1803.05407"
accessed: 2026-08-26
source_tier: A
scope_role: original-method-and-evidence
related: ["[[参数 EMA、SWA 与 Checkpoint Averaging]]", "[[训练时域、Restart、Schedule-Free 与末端学习率]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Izmailov 等：Stochastic Weight Averaging

> [!abstract] 来源定位
> 论文在 SGD 的常数或周期学习率轨迹上对多个参数点作算术平均，报告更宽解与更好泛化，并用单模型近似 FGE。课程采用 SWA 算法和 BN 统计重估要求，不把“参数平均”偷换成“预测平均”。

## 课程采用

$$
\bar\theta_K=\frac{1}{K}\sum_{k=1}^K\theta_{t_k}.
$$

采样起点、间隔、LR 周期、是否保存 optimizer state、归一化运行统计如何重估都必须记录。非线性网络一般满足

$$
f_{\bar\theta}(x)\ne \frac1K\sum_k f_{\theta_{t_k}}(x).
$$
