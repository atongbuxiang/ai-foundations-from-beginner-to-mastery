---
type: source
status: draft
area: [sources, neural-networks/residual-stability, resnet]
source_type: paper
title: "Deep Residual Learning for Image Recognition"
author: "Kaiming He; Xiangyu Zhang; Shaoqing Ren; Jian Sun"
year: 2016
url: "https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html"
arxiv: "1512.03385"
venue: "CVPR 2016"
accessed: 2026-08-23
source_tier: A
license: "CVF open-access paper；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[残差学习、恒等捷径与退化问题]]", "[[残差块 Jacobian 与梯度直通]]", "[[Pre-Activation、Pre-Norm 与 Post-Norm 残差]]"]
created: 2026-08-23
updated: 2026-08-23
---

# He et al.：Deep Residual Learning

> [!abstract] 来源定位
> 论文提出以输入为参照学习 residual function，并用 plain/residual 深网对照展示 degradation problem 与优化改善。它承担 ResNet 的历史问题、原始 block 和实验事实；本库不把旧视觉 benchmark 结果外推为所有架构中的单一因果机制。

## 核心对象

论文把目标映射写成 $H(x)$，令分支学习

$$
F(x)=H(x)-x,
$$

于是 block 输出为

$$
y=F(x)+x.
$$

当 shape 改变时，shortcut 可写成 $W_sx$；这已不是恒等映射，必须把 $W_s$ 的范数、秩和下采样一同计入传播分析。

## 断言表

| ID | 断言 | 类型 | 条件/证据 | 本库判断 |
|---|---|---|---|---|
| RES-C1 | 深 plain net 出现更高训练误差的 degradation | 经验 | 论文所用 CIFAR/ImageNet 架构与训练协议 | 原始证据成立，不等于所有 plain net 必然退化 |
| RES-C2 | residual parameterization 更易优化 | 经验 | 与论文中的配对基线比较 | 支持，但不是仅由 $I+J_F$ 一式完全解释 |
| RES-C3 | $F=0$ 时 block 可表达 identity | 结构 | shortcut 与 after-addition map 必须允许 identity | 有条件精确 |
| RES-C4 | 加深后函数类必然严格嵌套 | 表达 | 还依赖 shape、激活、normalization 与参数是否能实现零分支 | 不能无条件采用 |
| RES-C5 | 152-layer 结果证明深度单独造成性能提升 | 因果 | 架构、参数化、训练预算同时变化 | 证据不足 |

## 课程调用边界

- “存在一个 identity 参数设置”只证明表示可行，不证明优化器会找到它；
- training degradation 与 overfitting 不同：前者在原论文中表现为训练误差也变差；
- shortcut projection、stride 与 channel change 必须从 $I$ 改写成一般 $P$；
- 原论文的 accuracy、depth 与硬件结果属于历史实验，不是现代任务的默认基线。

