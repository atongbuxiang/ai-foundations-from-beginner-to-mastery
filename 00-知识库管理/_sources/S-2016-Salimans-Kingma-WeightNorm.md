---
type: source
status: active
area: [sources, neural-networks/normalization, parameterization]
source_type: paper
title: "Weight Normalization: A Simple Reparameterization to Accelerate Training of Deep Neural Networks"
author: "Tim Salimans; Diederik P. Kingma"
year: 2016
url: "https://proceedings.neurips.cc/paper_files/paper/2016/hash/ed265bc903a5a097f61d3ec064d96d2e-Abstract.html"
arxiv: "1602.07868"
venue: "NeurIPS 2016"
accessed: 2026-08-23
source_tier: A
license: "NeurIPS author paper；本库仅保存独立摘要、短公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[InstanceNorm、GroupNorm 与 WeightNorm]]", "[[参数对称性、等价表示与可辨识边界]]", "[[正交初始化与 Dynamical Isometry]]"]
created: 2026-08-23
updated: 2026-08-29
---

# Salimans–Kingma：Weight Normalization

> [!abstract] 来源定位
> WeightNorm 不对 activation 组求统计量，而把每个权重向量重参数化为 magnitude 与 direction。它属于参数几何而非 Batch/Layer/GroupNorm 的同轴变体；论文给出方法与经验结果，本库独立推导梯度投影、尺度 gauge 和部署物化边界。

## 正式参数化

$$
\boldsymbol w
=g\frac{\boldsymbol v}{\|\boldsymbol v\|_2}
=g\boldsymbol u,
\qquad \|\boldsymbol u\|_2=1.
$$

若上游权重梯度为 $\boldsymbol s=\nabla_{\boldsymbol w}L$，则

$$
\frac{\partial L}{\partial g}=\boldsymbol s^{\mathsf T}\boldsymbol u,
$$

$$
\nabla_{\boldsymbol v}L
=\frac g{\|\boldsymbol v\|_2}
\left(I-\boldsymbol u\boldsymbol u^{\mathsf T}\right)\boldsymbol s.
$$

所以 $\boldsymbol v^{\mathsf T}\nabla_{\boldsymbol v}L=0$：direction 参数收到切向梯度。

## 断言与边界

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| WN-C1 | magnitude 与 direction 显式分离 | 定义 | $\boldsymbol v\ne0$ | 已建立 |
| WN-C2 | 不引入 minibatch companion dependence | 数学结构 | 普通确定性前向 | 已建立 |
| WN-C3 | 改善优化条件与收敛 | 机制/经验 | 参数化、优化器和任务相关 | 非普遍定理 |
| WN-C4 | 计算开销低于 BN | 系统经验 | 实现是否缓存/物化权重相关 | 需实测 |

## 限制

- $\boldsymbol v=0$ 时参数化未定义，必须有 epsilon/初始化合同；
- $\boldsymbol v\mapsto a\boldsymbol v$（$a>0$）不改变权重，形成 gauge；
- WeightNorm 不固定完整矩阵谱范数，也不保证层的 Lipschitz 常数；
- 与 optimizer state、weight decay、parametrization removal 的交互属于实现语义。
