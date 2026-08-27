---
type: source
status: verified
area: [sources, parameterization, mup, mutransfer]
source_type: paper
title: "Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer"
author: [Greg Yang, Edward J. Hu, Igor Babuschkin, Szymon Sidor, Xiaodong Liu, David Farhi, Nick Ryder, Jakub Pachocki, Weizhu Chen, Jianfeng Gao]
year: 2022
url: "https://arxiv.org/abs/2203.03466"
code: "https://github.com/microsoft/mup"
accessed: 2026-08-26
source_tier: A
venue: "NeurIPS 2021; arXiv posting 2022"
scope_role: primary-theory-and-evidence
temporal_role: modern-theory
related: ["[[μP 的 Maximal Update 与宽度尺度推导]]", "[[μTransfer、Base Shape 与超参数零样本迁移]]", "[[Scale-up 协议、μP 证据与失效边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Tensor Programs V：μTransfer

> [!abstract] 来源定位
> 论文把 maximal update parameterization（μP）与跨宽度超参数迁移连接起来：在锁定模型族与参数化后，先在小代理模型调参，再把一组超参数不经目标规模搜索地迁移到大模型。本卷用它承担 μTransfer 的正式定义、可迁移超参数分类和原始 Transformer/ResNet 证据。

## 正文采用

1. “zero-shot”修饰的是**目标规模超参数搜索**，不是无需训练、验证或目标规模健康检查；
2. 可迁移对象包括学习率、初始化尺度等论文协议内的宽度相关超参数，但 regularization、数据量、训练时长和架构变化必须另审计；
3. 宽度、head 数和固定比例 shape 可作为原论文覆盖的尺度轴；深度变化尤其是 Post-LN 情形不能默认继承；
4. 输出层、hidden matrix、attention 等参数组具有不同宽度指数，规则必须与 optimizer 和 forward convention 一起记录；
5. 小模型只承担搜索代理，目标模型仍需做 stability、loss、失败率和有限预算确认。

## 证据边界

- 论文中的成功案例是特定 Transformer/ResNet、数据、optimizer 与搜索协议的经验结果，不是任意架构的无条件迁移定理；
- “最优超参数稳定”需要先定义候选集合、评价时点、训练预算和随机性；有限网格上的 argmin 一致不等于连续最优点完全相同；
- 理论的无限宽对象、有限宽实现检查和目标规模训练结果是三层证据，正文分开报告。

