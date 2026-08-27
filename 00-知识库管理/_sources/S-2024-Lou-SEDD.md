---
type: source
status: verified
source_type: paper
source_tier: A
title: "Discrete Diffusion Modeling by Estimating the Ratios of the Data Distribution"
author: "Aaron Lou, Chenlin Meng, Stefano Ermon"
year: 2024
url: "https://arxiv.org/abs/2310.16834"
accessed: 2026-08-25
area: [sources, ai/generative-models, diffusion, language-modeling]
related: ["[[连续时间 Markov 链、离散 Score 与采样]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Lou et al.：SEDD

> [!abstract] 原始证据
> SEDD 直接估计离散分布在相邻状态间的 probability ratios，并以 score entropy 构造训练目标。课程采用“离散 score 是边/状态对上的比值，而非欧氏梯度向量”这一主线。

## 边界

- ratio 的分母必须有正质量或受支持集约束；零概率状态需单独处理。
- 论文语言模型结果绑定模型规模、采样预算和评测协议；不写成所有离散扩散优于自回归。
- network evaluation 数与 CTMC event 数不是同一成本单位。
