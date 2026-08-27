---
type: source
status: draft
area: [sources, ai/transformers, ai/deep-networks, ai/normalization]
source_type: paper
title: "DeepNet: Scaling Transformers to 1,000 Layers"
author: "Hongyu Wang, Shuming Ma, Li Dong, Shaohan Huang, Dongdong Zhang, Furu Wei"
year: 2022
url: "https://arxiv.org/abs/2203.00555"
accessed: 2026-08-24
source_tier: A
license: "arXiv/author paper; independent summary only"
scope_role: core
temporal_role: deep-stability
related: ["[[Transformer Block、残差、归一化与 FFN]]", "[[Transformer 表达、稳定性与证据边界]]", "[[S-2021-Su-8978-千层Transformer困难]]", "[[S-2022-Su-8994-Why-Residual]]"]
created: 2026-08-24
updated: 2026-08-24
---

# DeepNet：DeepNorm 与千层 Transformer

> [!abstract] 来源定位
> DeepNet 用修改后的 residual/normalization 形式与深度相关初始化控制模型更新，并在论文设置中训练到 1,000 层。课程采用其精确参数化与条件化分析；“增量爆炸是所有深网唯一困难”或“千层总优于宽模型”均不由论文证明。

## 结构入口

DeepNorm 子层可概括为

$$
x_{l+1}=\operatorname{LN}(\alpha x_l+G_l(x_l;\theta_l)),
$$

并对参数初始化施加与深度/架构类型相关的 scale。具体 $\alpha,\beta$ 必须按 encoder-only、decoder-only 或 encoder–decoder 的论文公式调用，不能用单一常数跨家族复制。

## 证据分层

- 结构和参数 scale 为 `I`；
- update bound 为带模型/初始化假设的 `T`；
- 1000 层与翻译结果是所述训练协议下 `E`；
- 深度对所有任务的普遍收益仍是 `O`。
