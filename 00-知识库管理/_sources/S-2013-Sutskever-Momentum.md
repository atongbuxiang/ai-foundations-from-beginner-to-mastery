---
type: source
status: verified
area: [sources, optimization, momentum, deep-learning]
source_type: paper
title: "On the Importance of Initialization and Momentum in Deep Learning"
author: [Ilya Sutskever, James Martens, George Dahl, Geoffrey Hinton]
year: 2013
url: "https://proceedings.mlr.press/v28/sutskever13.html"
accessed: 2026-08-26
source_tier: A
venue: "ICML 2013, PMLR 28(3):1139–1147"
scope_role: primary
related: ["[[Momentum、EMA、偏差修正与框架约定]]", "[[Nesterov、Lookahead 与动量形式的等价边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Sutskever 等 2013：深度学习中的初始化与动量

> [!abstract] 来源定位
> 原论文把恰当初始化、逐渐增大的 momentum schedule 与深层/循环网络训练联系起来，并给出适于深度学习实现的 Nesterov 表述。它提供算法形式与历史实证，不提供任意非凸网络的普遍加速定理。

## 课程调用

- velocity 中包含 learning rate 的 convention；
- classical momentum 与 Nesterov look-ahead 的差别；
- 初始状态、momentum schedule 与参数化共同决定轨迹；
- 与当前框架的 buffer convention 做逐式翻译。

## 证据边界

论文中的模型、初始化、数据与训练预算属于特定实验设置。“能达到 Hessian-free 方法当时的性能”不是对现代模型和任意任务的支配关系。

