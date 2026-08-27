---
type: source
status: draft
area: [sources, neural-networks, highway-networks, gating]
source_type: paper
title: "Highway Networks"
author: "Rupesh Kumar Srivastava; Klaus Greff; Jürgen Schmidhuber"
year: 2015
url: "https://arxiv.org/abs/1505.00387"
venue: "arXiv:1505.00387"
accessed: 2026-08-23
source_tier: A
license: "author preprint；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[Highway、Dense Connection 与 Skip 结构比较]]", "[[GLU、GeGLU、SwiGLU 与乘性门]]", "[[残差学习、恒等捷径与退化问题]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Srivastava、Greff、Schmidhuber：Highway Networks

> [!abstract] 来源定位
> 论文用可学习 transform/carry gates 建立跨层信息通路，并展示很深前馈网络的可训练性。它是 Highway 结构与 gate-bias 初始化的原始来源；本库补上 gate 对输入依赖时不能漏掉的 Jacobian 项，并把经验结果限制在论文协议内。

## 原始结构

常见 coupled-gate 写法为

$$
y=T(x)\odot H(x)+[1-T(x)]\odot x.
$$

$T(x)$ 控制 transform，$1-T(x)$ 控制 carry。令 transform gate 初始偏向 0，可使网络初期更接近 carry path；这不是无门控恒等残差，因为 gate 仍是数据依赖映射。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| HW-C1 | Highway 用门控在 transform 与 carry 间插值 | 结构 | 两支 shape 可融合 | 精确 |
| HW-C2 | 负 transform-gate bias 可打开初始 carry path | 初始化机制 | 依赖 sigmoid 饱和度与输入 | 有条件成立 |
| HW-C3 | Highway 等同于 additive residual | 结构外推 | gate 导数与逐坐标乘法不同 | 不等同 |
| HW-C4 | 任意深度都可稳定训练 | 普遍经验外推 | 优化、宽度、任务与数值系统 | 原论文不足以支持 |

## 本库补严

对向量 gate，完整 Jacobian 含

$$
\operatorname{Diag}(T)J_H+
\operatorname{Diag}(1-T)+
\operatorname{Diag}(H-x)J_T.
$$

最后一项会让 gate 学习与 carry/transform 差值耦合；把 $T$ 当常数会漏掉真实梯度。
