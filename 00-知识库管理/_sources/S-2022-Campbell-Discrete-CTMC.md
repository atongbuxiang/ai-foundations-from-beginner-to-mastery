---
type: source
status: verified
source_type: paper
source_tier: A
title: "A Continuous Time Framework for Discrete Denoising Models"
author: "Andrew Campbell et al."
year: 2022
url: "https://arxiv.org/abs/2205.14987"
accessed: 2026-08-25
area: [sources, ai/generative-models, stochastic-processes]
related: ["[[连续时间 Markov 链、离散 Score 与采样]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Campbell et al.：离散去噪的连续时间框架

> [!abstract] 原始证据
> 论文把离散数据的前向加噪和反向生成都写成连续时间 Markov 链（CTMC），给出连续时间 ELBO、jump-process sampler 与分布误差界。课程采用 generator/rate 与 reverse-rate 的对象合同。

## 边界

- CTMC 的 generator 不是 DDPM 的协方差矩阵；非对角元是跳跃率，行和为零。
- 精确反向率依赖未知 $p_t$ 的概率比；模型与数值事件模拟分别产生误差。
- 论文误差界的假设不能被删成“连续时间必然更准”。
