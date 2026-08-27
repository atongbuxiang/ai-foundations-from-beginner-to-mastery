---
type: source
status: verified
area: [sources, software, optimization, pytorch]
source_type: documentation
title: "PyTorch SGD Documentation"
author: [PyTorch Contributors]
year: 2026
url: "https://docs.pytorch.org/docs/main/generated/torch.optim.SGD.html"
accessed: 2026-08-26
source_tier: A
scope_role: implementation-authority
temporal_role: current-documentation
related: ["[[训练系统的对象、状态与一步更新合同]]", "[[Momentum、EMA、偏差修正与框架约定]]", "[[Nesterov、Lookahead 与动量形式的等价边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# PyTorch SGD：当前实现语义

> [!abstract] 来源定位
> 这是当前 PyTorch `torch.optim.SGD` 的实现合同来源，而不是优化理论来源。课程以 2026-08-26 访问版本为准，固定 buffer 初始化、dampening、Nesterov、weight decay 与 learning-rate placement。

## 已核对的实现事实

1. 无 dampening 时，buffer 递推为 $b_t=\mu b_{t-1}+g_t$，参数步为 $p_t=p_{t-1}-\gamma b_t$；
2. 首个 momentum buffer 初始化为第一步 gradient，而不是零；
3. dampening 从第二个 step 开始作用；
4. Nesterov 方向在更新前写成 $g_t+\mu b_t$；
5. 文档明确指出其 learning-rate placement 与 Sutskever 等人的 velocity convention 不同；
6. `foreach`、`fused` 与单 tensor 路径可能改变性能和末位数值，不应改变声明的高层更新合同。

## 复现要求

记录 PyTorch 版本、param-group、`momentum`、`dampening`、`nesterov`、`weight_decay`、`maximize`、dtype、step 计数与 optimizer state。只写“SGD+momentum=0.9”不足以复现。

