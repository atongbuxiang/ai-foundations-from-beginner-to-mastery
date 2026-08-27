---
type: source
status: draft
area: [sources, neural-networks/normalization]
source_type: paper
title: "Layer Normalization"
author: "Jimmy Lei Ba; Jamie Ryan Kiros; Geoffrey E. Hinton"
year: 2016
url: "https://arxiv.org/abs/1607.06450"
arxiv: "1607.06450"
accessed: 2026-08-23
source_tier: A
license: "arXiv paper；本库仅保存独立摘要、短公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[归一化的对象、轴与不变性]]", "[[LayerNorm 的逐样本几何与反向传播]]", "[[RMSNorm、均值移除与缩放不变性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Ba–Kiros–Hinton：Layer Normalization

> [!abstract] 来源定位
> LayerNorm 原始论文把统计量从“同一 feature 的不同 training cases”转到“同一 training case 的一组 hidden units”，从而移除 batch-size 与 running-statistic 依赖。论文还比较了 BatchNorm、WeightNorm 与 LayerNorm 的参数/数据重缩放不变性，并给出 RNN、序列模型和小 batch 实验。

## 元数据与原始入口

- arXiv：[1607.06450](https://arxiv.org/abs/1607.06450)；
- 定义：第 3 节与补充材料式 (15)—(16)；
- 不变性：第 5.1 节 Table 1；
- 当前调用者：[[LayerNorm 的逐样本几何与反向传播]]。

## 核心断言与课程判断

| ID | 断言 | 类型 | 条件/边界 | 当前判断 |
|---|---|---|---|---|
| C1 | 对单个样本的一组 hidden units 计算共享 mean/variance | 定义 | 必须明确“这一组”在现代张量中对应哪些尾轴 | 课程定义主来源 |
| C2 | 训练与测试使用相同的输入内统计量 | 算法语义 | 不需要 running statistics；上游 dropout 等仍可使输出随机 | 已核验 |
| C3 | 每个被归一化元素有可学习 gain 与 bias | 参数化 | 现代框架的 `normalized_shape` 决定参数形状 | 已核验 |
| C4 | LayerNorm 不引入不同 training cases 之间的新依赖 | 结构性质 | 若归约轴不含 batch；不代表 token/feature 间无耦合 | 已核验 |
| C5 | LayerNorm 对整组正尺度与共同平移具有不变性 | 代数性质 | 精确尺度不变性需 $\varepsilon=0$；负尺度产生符号翻转 | 需按课程公式精化 |
| C6 | 原论文在 RNN 与小 batch 设置中观察到训练收益 | 实验 | 旧架构/数据设置；不证明现代 Transformer 跨任务最优 | 设置内成立 |

## 课程采用的最小公式

对单个样本/位置的 $D$ 维向量 $\boldsymbol z\in\mathbb R^D$，

$$
\mu=\frac1D\sum_{j=1}^D z_j,
\qquad
q=\frac1D\sum_{j=1}^D(z_j-\mu)^2,
$$

$$
\operatorname{LN}(\boldsymbol z)
=\boldsymbol\gamma\odot
\frac{\boldsymbol z-\mu\boldsymbol 1}{\sqrt{q+\varepsilon}}
+\boldsymbol\beta.
$$

现代 Transformer 最常见合同是输入 $X\in\mathbb R^{B\times T\times D}$，对每个 $(b,t)$ 独立归约最后一个 $D$ 轴；这是一种具体轴选择，不应把“layer”误读为自动归约整个计算图层的所有维度。

## 原论文不变性表的精化

原文讨论 weight matrix/data 的 scaling 与 recentering。课程进一步把算子自身写成：若 $a>0$、$\varepsilon=0$，

$$
\widehat{a\boldsymbol z+c\boldsymbol1}=\widehat{\boldsymbol z};
$$

若 $a<0$，则标准化向量整体变号。$\varepsilon>0$ 时，尺度抵消变成近似；共同平移仍在精确算术中被 centering 消去。

## 限制与后续演化

- 原论文的“all hidden units”需结合张量布局解释；框架不会替用户猜轴；
- LayerNorm 不使用 batch state，但会在同一归约组内产生 dense Jacobian coupling；
- $D=1$ 完全退化，$D=2$ 且 $\varepsilon=0$ 时局部 Jacobian 几乎处处为零；
- Transformer 的 Pre/Post-Norm 放置属于残差 Jacobian 问题，在 NN-39 与 NN-45 单独处理；
- RMSNorm 删除 centering 后改变的是几何和不变性，不是“更便宜的同一算子”。

