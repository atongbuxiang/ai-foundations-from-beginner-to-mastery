---
type: source
status: verified
source_type: paper
source_tier: A
title: "Structured Denoising Diffusion Models in Discrete State-Spaces"
author: "Jacob Austin et al."
year: 2021
url: "https://arxiv.org/abs/2107.03006"
accessed: 2026-08-25
area: [sources, ai/generative-models, diffusion]
related: ["[[Categorical Diffusion、转移矩阵与离散后验]]", "[[Absorbing-state、Mask Diffusion 与并行迭代生成]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Austin et al.：D3PM

> [!abstract] 原始证据
> D3PM 用离散状态转移矩阵定义 forward corruption，覆盖均匀、近邻、embedding 与 absorbing-state 核，并给出离散后验、ELBO 与辅助 cross-entropy 训练。课程的 $Q_t,\bar Q_t$ 和 absorbing mask 定义以此为一级来源。

## 采用与边界

- 采用：matrix-product marginal、Bayes posterior、$x_0$-parameterization 与 transition design。
- 不外推：特定 CIFAR/text 结果不构成所有离散模态上的优势；辅助 CE 改变训练 objective，不能与纯 ELBO 数值混写。
- 记号：课程使用 row-stochastic $Q_t[i,j]=q(x_t=j\mid x_{t-1}=i)$，与采用 column convention 的文献必须转置后再比较。
