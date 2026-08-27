---
type: source
status: verified
area: [sources, architecture/rnn, optimization/gradients]
source_type: paper
title: "On the Difficulty of Training Recurrent Neural Networks"
author: "Razvan Pascanu, Tomas Mikolov, Yoshua Bengio"
year: 2013
url: "https://proceedings.mlr.press/v28/pascanu13.html"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[Vanilla RNN、BPTT 与梯度消失爆炸]]"]
created: 2026-08-24
updated: 2026-08-24
---

# On the Difficulty of Training Recurrent Neural Networks

> [!abstract] 来源定位
> 论文从分析、几何与动力系统角度讨论 RNN 的梯度消失/爆炸，并提出 gradient norm clipping 处理爆炸梯度。课程采用它说明时间 Jacobian 乘积，而不把 clipping 误写成长期信用分配的完整解法。

## 课程采用的断言

| 断言 | 条件与边界 | 课程处理 |
|---|---|---|
| 长程梯度含时间 Jacobian 的有序乘积 | Jacobian 随输入、状态和时间变化 | 正式推导 |
| 某些方向可指数衰减或放大 | 需要看乘积的奇异值/方向，不能只看单个矩阵谱半径 | 条件化表述 |
| norm clipping 可限制一次更新的梯度范数 | 不恢复已经消失的信号，也不保证优化成功 | 作为工程缓解 |

## 调用

- [[Vanilla RNN、BPTT 与梯度消失爆炸]]
- [[解答 - Vanilla RNN、BPTT 与梯度消失爆炸]]
