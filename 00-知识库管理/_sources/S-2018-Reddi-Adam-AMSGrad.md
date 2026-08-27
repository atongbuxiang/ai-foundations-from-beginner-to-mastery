---
type: source
status: verified
area: [sources, optimization, adam, amsgrad]
source_type: paper
title: "On the Convergence of Adam and Beyond"
author: "Sashank J. Reddi; Satyen Kale; Sanjiv Kumar"
year: 2018
url: "https://openreview.net/forum?id=ryQu7f-RZ"
venue: "ICLR 2018"
accessed: 2026-08-26
source_tier: A
license: "OpenReview 论文；本库仅保存独立摘要、必要反例结构与链接"
scope_role: counterexample-and-repair
temporal_role: foundational-correction
related: ["[[Adam 收敛反例、AMSGrad 与条件化保证]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Reddi、Kale、Kumar：Adam 反例与 AMSGrad

> [!abstract] 来源定位
> 论文给出简单凸在线优化中 Adam 不收敛到最优解的显式例子，指出指数滑动二阶矩可能让有效学习率失去所需的长期控制，并提出 AMSGrad 的 long-term memory 修补。

## 课程采用

- 反例不是“深网里偶尔跑坏”的故事，而是可逐周期手算的梯度序列；
- 关键诊断量涉及 $\alpha_t/\sqrt{v_t}$ 的时间行为，而非只看 $v_t$ 是否正数；
- AMSGrad 使用 $\widehat v_t^{\max}=\max(\widehat v_{t-1}^{\max},v_t)$ 防止 denominator 忘记过去峰值；
- 保证仍依赖凸性、bounded gradients/domain、step schedule 等假设，不应写成“打开 `amsgrad=True` 就保证深网收敛”。

## 复算要求

课程不只转述结论：必须写出周期梯度、比较 Adam 与 AMSGrad 的累计位移，并审计 bias correction、epsilon 和 indexing 是否改变数值但不掩盖机制。
