---
type: source
status: active
area: [sources, neural-networks, implementation]
source_type: textbook
title: "Dive into Deep Learning"
author: [Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola]
year: 2023
url: "https://d2l.ai/"
accessed: 2026-08-23
source_tier: A
license: "Official open interactive book; retain citation and edition context"
scope_role: primary
temporal_role: implementation-backbone
related: ["[[线性层、批量张量与参数计数]]", "[[多层感知机与逐层前向计算]]", "[[神经网络基础 MOC]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Dive into Deep Learning
> [!abstract] 来源定位
> 把线性模型、MLP、训练循环和现代架构连接到可执行张量代码的交互式教材。本库调用形状约定、vectorization、dense layer 与 MLP 实现接口；理论量词和历史断言仍回到正式教材/原论文，不把框架 API 当定义。
## 本库调用
1. row-batch 约定 $XW+b$；
2. dense layer 与 parameter count；
3. MLP 的隐藏层/输出层形状；
4. vectorization 与 minibatch；
5. 实现约定与数学对象的对应。

