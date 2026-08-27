---
type: source
status: verified
area: [sources, generative-models/flow, density-estimation]
source_type: paper
title: "Flow++: Improving Flow-Based Generative Models with Variational Dequantization and Architecture Design"
author: [Jonathan Ho, Xi Chen, Aravind Srinivas, Yan Duan, Pieter Abbeel]
year: 2019
url: "https://arxiv.org/abs/1902.00275"
accessed: 2026-08-25
source_tier: A
scope_role: core
temporal_role: classical
related: ["[[离散似然、连续似然、Dequantization 与 Bits-per-dim]]", "[[Flow 的 Support、Dequantization、TARFLOW 与证据地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Ho et al.：Flow++ 与变分 Dequantization

> [!abstract] 来源定位
> Flow++ 把 uniform dequantization 推广为可学习的 $q_\phi(u\mid x)$，用变分下界连接连续密度与离散像素质量。它承担 variational dequantization 的一级来源；论文同时改变 coupling transform 和 conditioner，故经验提升不能只归因于 dequantizer。

## 下界骨架

令离散 $x\in\mathbb Z^D$，$u\in[0,1)^D$，连续变量 $y=x+u$。由

$$
P_\theta(x)=\int_{[0,1)^D}p_\theta(x+u)\,du
$$

和 Jensen，

$$
\log P_\theta(x)
\ge \mathbb E_{q_\phi(u\mid x)}
\left[\log p_\theta(x+u)-\log q_\phi(u\mid x)\right].
$$

gap 为 $q_\phi(u\mid x)$ 与模型在该 bin 内后验的 KL；uniform dequantization 是 $q=1$ 的特例。

## 课程边界

- 这是离散 log mass 的 lower bound，不是连续 point density 与离散 mass 的直接相等；
- bin 宽、数据缩放、log base 与维度归约决定 BPD 常数；
- train-time random dequantization 与 sample-time rounding/clipping 是两份合同。

