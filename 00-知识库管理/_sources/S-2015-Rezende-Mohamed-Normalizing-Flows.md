---
type: source
status: draft
area: [sources, ai/generative-models, math/probability]
source_type: paper
title: "Variational Inference with Normalizing Flows"
author: "Danilo Jimenez Rezende; Shakir Mohamed"
year: 2015
url: "https://proceedings.mlr.press/v37/rezende15.html"
accessed: 2026-08-19
source_tier: A
license: "PMLR open access; repository stores only metadata and independent notes"
venue: "Proceedings of the 32nd International Conference on Machine Learning, PMLR 37"
scope_role: core
temporal_role: foundational
related: ["[[随机变量变换与密度换元]]", "[[S-2018-Su-5776-NICE流模型]]", "[[S-2019-Su-6705-从正态分布到Gumbel-Softmax]]"]
created: 2026-08-19
updated: 2026-08-19
---

# Variational Inference with Normalizing Flows

> [!abstract] 来源定位
> 该论文把一串可逆、可微变换用于构造灵活的变分后验，并用逐层 change-of-variables 累计密度修正。课程用它承担 normalizing flow 在变分推断中的原始方法证据；经典换元定理本身仍由概率/分析教材承担。

## 元数据与纳入

- 正式引用：Rezende, D. J. & Mohamed, S. (2015), *Variational Inference with Normalizing Flows*, ICML, PMLR 37:1530–1538；
- 论文页：[https://proceedings.mlr.press/v37/rezende15.html](https://proceedings.mlr.press/v37/rezende15.html)；
- PDF：[https://proceedings.mlr.press/v37/rezende15.pdf](https://proceedings.mlr.press/v37/rezende15.pdf)；
- 范围角色：`core`；当前调用者：[[随机变量变换与密度换元]]。

## 文章结构

1. amortized variational inference 与 stochastic backpropagation；
2. 基础分布的重参数化；
3. finite/infinitesimal normalizing flows；
4. 把 flow 写入变分下界；
5. 特殊 flow 与相关方法；
6. 有限实验与研究边界。

## 核心断言与课程判断

| ID | 断言 | 类型 | 条件/边界 | 当前判断 |
|---|---|---|---|---|
| C1 | 可逆光滑映射可通过 change-of-variables 把简单密度变成新密度 | 经典定理调用 | 同维、局部 Jacobian 非奇异、方向明确 | 已核验 |
| C2 | 多层映射的 log-density 修正等于逐层 log-absolute-determinant 之和 | 推导 | 每层可逆可微 | 已核验 |
| C3 | flow 可扩展变分后验族，减轻简单 mean-field 家族的表达限制 | 方法贡献 | 受 flow 架构、优化和计算预算限制 | 已建立方法 |
| C4 | location–scale 重参数允许固定噪声上的路径梯度 | 梯度方法 | 微分—期望交换和可积性 | 有条件成立 |
| C5 | 更长/更丰富 flow 能在实验中改善特定任务的后验近似 | 实验 | 论文模型与数据范围 | 不外推为普适支配 |

## 课程采用的密度账本

令

$$
z_k=f_k(z_{k-1}),\qquad k=1,\dots,K.
$$

则

$$
\log q_K(z_K)
=\log q_0(z_0)
-\sum_{k=1}^K\log\left|\det\frac{\partial f_k}{\partial z_{k-1}}\right|.
$$

课程同时写出 inverse 方向，防止把符号差异误判为不同公式。

## 证据边界

- 论文第 3 节承担 finite flow 的方法形式与应用语境；
- 换元公式的测度条件、非单射分支、维数改变和奇异分布由正式概率/分析课程补充；
- 论文中的 asymptotic expressivity 表述不能简化为“任意有限 flow 都能精确表示任意分布”；
- 实验结果不承担现代 flow 架构之间的当前性能排序。

## 已生成与后续调用

- [x] [[随机变量变换与密度换元]]：逐层 logdet、复杂度与支持限制；
- [ ] 生成模型专题：NICE、RealNVP、autoregressive/continuous flows 的结构比较；
- [ ] 变分推断专题：flow posterior 对 ELBO 和梯度方差的影响。

## 交叉验证

- Papamakarios et al. (2021), *Normalizing Flows for Probabilistic Modeling and Inference*；
- Dinh, Krueger & Bengio (2015), *NICE*；
- MIT 6.436J, *Derived Distributions*。

