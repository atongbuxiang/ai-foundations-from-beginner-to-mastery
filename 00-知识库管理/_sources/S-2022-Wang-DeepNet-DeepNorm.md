---
type: source
status: active
area: [sources, neural-networks, transformers, residual-scaling, initialization]
source_type: paper
title: "DeepNet: Scaling Transformers to 1,000 Layers"
author: "Hongyu Wang; Shuming Ma; Li Dong; Shaohan Huang; Dongdong Zhang; Furu Wei"
year: 2022
url: "https://arxiv.org/abs/2203.00555"
doi: "https://doi.org/10.1109/TPAMI.2024.3386927"
venue: "arXiv 2022；IEEE TPAMI 2024"
accessed: 2026-08-29
source_tier: A
license: "author preprint/final article metadata；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: modern-foundational
related: ["[[ReZero、Fixup、DeepNorm 与深网缩放]]", "[[Pre-Norm、Post-Norm 与归一化放置]]", "[[残差缩放、Lipschitz 界与深度稳定性]]"]
created: 2026-08-23
updated: 2026-08-29
---

# Wang et al.：DeepNet 与 DeepNorm

> [!abstract] 来源定位
> DeepNet 以 DeepNorm 修改 Post-LN Transformer 的 residual connection，并为不同 encoder/decoder 结构给出 depth-dependent 的运行时系数 $\alpha$ 与初始化系数 $\beta$。论文的理论对象是特定假设下的模型更新界，实验覆盖极深 Transformer；本库不把它改写成任意优化器、任意架构的稳定性定理。

## 方法合同

单子层写作

$$
x_{\ell+1}=\operatorname{LN}\!\left(\alpha x_\ell+G_\ell(x_\ell;\theta_\ell)\right).
$$

$\alpha$ 是训练与推理期都存在的固定 shortcut scale；$\beta$ 只用于缩放指定权重的初始化。论文对 encoder-only 的 $N$ 层给出

$$
\alpha=(2N)^{1/4},
\qquad
\beta=(8N)^{-1/4}.
$$

decoder-only 的 $M$ 层同形；encoder–decoder 两侧使用不同公式，不能只记一对常数。

## 初始化选择边界

论文算法把 $\beta$ 用于 FFN 权重以及 attention 的 value/output 权重；query/key 不按同一规则缩放。把所有矩阵统一乘 $\beta$ 会改变方法合同。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| DP-C1 | $\alpha$ 与 $\beta$ 具有 depth-dependent 公式 | 方法 | 必须区分模型类型与两侧深度 | 精确 |
| DP-C2 | $\beta$ 是运行时 residual gate | 结构误读 | $\beta$ 只改指定参数初始化 | 错误 |
| DP-C3 | DeepNorm 从精确恒等映射开始 | 结构误读 | Post-LN 且 $\alpha\ne1$ | 一般错误 |
| DP-C4 | 更新界无条件覆盖 Adam 全程 | 理论外推 | 论文推导有初始化与优化近似假设 | 不成立 |

## 课程调用边界

本卡支持复现论文参数化和说明“控制 parameter update”不同于“使 state Jacobian 为 $I$”。最终训练稳定与精度仍需模型、优化器、精度和系统证据。
