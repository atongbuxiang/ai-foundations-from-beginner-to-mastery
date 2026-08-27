---
type: source
status: verified
area: [sources, neural-networks/normalization, transformers, optimization]
source_type: paper
title: "On Layer Normalization in the Transformer Architecture"
author: "Ruibin Xiong; Yunchang Yang; Di He; Kai Zheng; Shuxin Zheng; Chen Xing; Huishuai Zhang; Yanyan Lan; Liwei Wang; Tie-Yan Liu"
year: 2020
url: "https://proceedings.mlr.press/v119/xiong20b.html"
arxiv: "2002.04745"
venue: "ICML 2020, PMLR 119:10524–10533"
accessed: 2026-08-23
source_tier: A
license: "PMLR author paper；本库仅保存独立摘要、短公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[Pre-Norm、Post-Norm 与归一化放置]]", "[[LayerNorm 的逐样本几何与反向传播]]", "[[残差块 Jacobian 与梯度直通]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Xiong et al.：Transformer 中 LayerNorm 的位置

> [!abstract] 来源定位
> 论文用特定初始化与 mean-field 假设分析 Transformer 的 Pre-LN/Post-LN 梯度，并研究 warm-up。它是“归一化位置会改变训练动力学”的正式来源；本库只在论文假设范围内转述结果，并用一般 residual Jacobian 恒等式提供更基础的结构解释。

## 两种单子层形式

$$
\text{Pre-LN:}\quad x^+=x+F(N(x)),
$$

$$
\text{Post-LN:}\quad x^+=N(x+F(x)).
$$

一般 Jacobian 恒等式分别为

$$
J_{\mathrm{pre}}=I+J_F(N(x))J_N(x),
$$

$$
J_{\mathrm{post}}=J_N(x+F(x))(I+J_F(x)).
$$

这两个等式不需要 mean-field；论文更强的梯度量级结论需要其初始化、宽度与随机性假设。

## 断言表

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| XLN-C1 | LayerNorm 位置改变初始梯度量级 | 理论 | 论文模型与 mean-field 假设 | 有条件成立 |
| XLN-C2 | 论文 Post-LN 在输出附近初始梯度偏大 | 理论 | 同上 | 不外推任意深网 |
| XLN-C3 | Pre-LN 在论文设置下可减少 warm-up 依赖 | 理论+经验 | 指定优化设置与任务 | 保留设置 |
| XLN-C4 | Pre-LN 普遍优于 Post-LN | 泛化命题 | 原论文不足以支持 | 否 |

## 本库使用边界

- 一般 Jacobian 只说明 identity path 是否被 normalization Jacobian 左乘，不自动给出深层乘积范数；
- 学习率、warm-up、初始化、残差缩放与最终 norm 共同决定训练行为；
- “更易训练”“最终效果更高”“迁移更好”是不同实验问题；
- 后续更深架构的 DeepNorm/ReZero 等不由本论文单独覆盖。
