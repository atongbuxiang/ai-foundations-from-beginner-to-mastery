---
type: source
status: verified
area: [sources, generative-models/vae, image-generation]
source_type: paper
title: "NVAE: A Deep Hierarchical Variational Autoencoder"
author: [Arash Vahdat, Jan Kautz]
year: 2020
url: "https://arxiv.org/abs/2007.03898"
accessed: 2026-08-25
source_tier: A
scope_role: core
temporal_role: classical
related: ["[[层次 VAE、表达性先验与近似后验 Flow]]", "[[S-2020-Su-7574-NVAE]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Vahdat 与 Kautz：NVAE

> [!abstract] 来源定位
> NVAE 是深层层次图像 VAE，组合多组 latent、residual Gaussian parameterization、depthwise separable convolution、batch normalization、谱正则和 posterior flows。它承担架构与论文协议；论文时点的 SOTA 和样本质量只在相应数据/预算下成立。

## 课程调用

- 写清 top-down prior $p(z_l\mid z_{<l})$ 与 bottom-up/top-down inference 的分工；
- 层次越深不自动每层 active；应报告 per-group rate；
- 同时改动多个部件，单因 attribution 需要 ablation；
- 2.91 BPD 等数值不跨预处理、版本与模型族直接外推。

