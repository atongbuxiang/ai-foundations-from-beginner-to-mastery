---
type: source
status: active
area: [sources, neural-networks/normalization, transformers, systems]
source_type: paper
title: "PowerNorm: Rethinking Batch Normalization in Transformers"
author: "Sheng Shen; Zhewei Yao; Amir Gholami; Michael W. Mahoney; Kurt Keutzer"
year: 2020
url: "https://proceedings.mlr.press/v119/shen20e.html"
arxiv: "2003.07845"
venue: "ICML 2020, PMLR 119:8741–8751"
accessed: 2026-08-23
source_tier: A
license: "PMLR author paper；本库仅保存独立摘要、短公式与链接"
scope_role: core
temporal_role: method-aged
related: ["[[小批量、混合精度、分布式与因果归一化边界]]", "[[RMSNorm、均值移除与缩放不变性]]", "[[BatchNorm 前向统计与训练—推理差异]]"]
created: 2026-08-23
updated: 2026-08-29
---

# Shen et al.：PowerNorm

> [!abstract] 来源定位
> 论文系统研究 NLP Transformer 中跨 batch 统计波动，并提出删除零均值、使用 running quadratic mean 与近似反向的 PowerNorm。它为“统计轴与数据制度必须共同审计”提供一手案例；本库不把该方法的特定基准优势写成所有 Transformer 的结论。

## 与本卷的接口

论文指出 vanilla BN 在其 NLP 设置中出现显著 batch-statistic fluctuation，并将方法改造拆成：

1. 不做 zero-mean centering；
2. 用 quadratic mean 取代 centered variance；
3. forward 使用 running statistic；
4. 为该状态路径设计近似 backpropagation。

这说明“换一个 norm 名称”同时改变统计量、状态、反向和系统语义。

## 断言表

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| PN-C1 | 论文 NLP batch statistics 波动大于其 CV 对照 | 经验 | 指定数据、模型、记录协议 | 保留设置 |
| PN-C2 | PowerNorm 使用 running quadratic mean | 定义 | 论文算法 | 已建立 |
| PN-C3 | 近似反向在论文假设下梯度有界 | 理论 | mild assumptions 仍需逐条读取 | 有条件引用 |
| PN-C4 | PowerNorm 普遍优于 LN/BN | 泛化命题 | 论文不足以支持 | 否 |

## 限制

- running state 会引入历史、顺序和 checkpoint 语义；
- approximate backward 不等于 forward 的精确导数；
- 论文的 Lipschitz/gradient 结论有模型假设，不能只引用摘要外推；
- 在因果/流式模型中，任何跨 token 或跨样本统计仍需做 prefix 与数据边界审计。
