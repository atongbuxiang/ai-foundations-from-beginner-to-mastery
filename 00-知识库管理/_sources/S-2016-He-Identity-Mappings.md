---
type: source
status: active
area: [sources, neural-networks/residual-stability, identity-mapping]
source_type: paper
title: "Identity Mappings in Deep Residual Networks"
author: "Kaiming He; Xiangyu Zhang; Shaoqing Ren; Jian Sun"
year: 2016
url: "https://arxiv.org/abs/1603.05027"
venue: "ECCV 2016"
accessed: 2026-08-23
source_tier: A
license: "author preprint；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[残差学习、恒等捷径与退化问题]]", "[[残差块 Jacobian 与梯度直通]]", "[[Pre-Activation、Pre-Norm 与 Post-Norm 残差]]"]
created: 2026-08-23
updated: 2026-08-29
---

# He et al.：Identity Mappings

> [!abstract] 来源定位
> 论文分析 identity shortcut 与 after-addition identity 对前向/反向信号传播的作用，并通过 residual-unit 消融支持 pre-activation 设计。它承担恒等 rail 的原始公式与实验；本库另外给出一般 Jacobian、singular-value 反例和有限精度边界。

## 精确展开

在 identity shortcut 与 identity after-addition map 下，

$$
x_{ell+1}=x_ell+F_ell(x_ell),
$$

所以

$$
x_L=x_ell+sum_{i=ell}^{L-1}F_i(x_i).
$$

对损失求导得到“直接项 + residual 项”的结构。注意 residual 项仍依赖全部中间状态，不能把非线性网络误写成互不相干的并行支路。

## 断言表

| ID | 断言 | 类型 | 条件/证据 | 本库判断 |
|---|---|---|---|---|
| IDM-C1 | identity shortcut 提供未乘权重矩阵的直接项 | 代数 | shape 不变、shortcut 真为 identity | 精确 |
| IDM-C2 | 任意梯度都不会消失或爆炸 | 强外推 | branch 可与直接项相消，跨层积仍可能病态 | 不成立 |
| IDM-C3 | pre-activation 改善极深网络训练 | 经验 | 论文架构、数据和协议 | 原始证据成立 |
| IDM-C4 | gated/scaled shortcut 与 identity 等价 | 结构 | gate/scale 会进入直达项乘积 | 一般不等价 |

## 课程调用边界

本卡支持“存在 algebraic identity rail”，不支持“full Jacobian singular values 自动集中在 1”。后者还需要 branch Jacobian 的 norm、方向、相关性、非正规性和训练演化。
