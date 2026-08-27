---
type: source
status: verified
area: [sources, optimization, learning-rate, restart]
source_type: paper
title: "SGDR: Stochastic Gradient Descent with Warm Restarts"
author: "Loshchilov and Hutter"
year: 2017
url: "https://arxiv.org/abs/1608.03983"
accessed: 2026-08-26
source_tier: A
scope_role: original-method
related: ["[[Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]", "[[训练时域、Restart、Schedule-Free 与末端学习率]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Loshchilov 与 Hutter：Cosine Annealing 与 Warm Restarts

> [!abstract] 来源定位
> SGDR 定义了周期内 cosine annealing 与 partial warm restart，并在若干视觉任务上研究 anytime performance。课程采用其精确定义和实验协议，不把周期重启描述成必然逃离局部极小。

## 课程采用

周期 $i$ 内令 $T_{\mathrm{cur}}\in[0,T_i]$：

$$
\eta_t=\eta_{\min}
+\frac{\eta_{\max}-\eta_{\min}}{2}
\left(1+\cos\frac{\pi T_{\mathrm{cur}}}{T_i}\right).
$$

重启的是 schedule phase 和 LR，不是自动重置 momentum、Adam moments、data order 或模型参数；这些都必须另行声明。
