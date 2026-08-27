---
type: source
status: verified
area: [sources, generative-models, diffusion, vae]
source_type: blog
title: "生成扩散模型漫谈（二）：DDPM = 自回归式 VAE"
author: 苏剑林
year: 2022
url: "https://spaces.ac.cn/archives/9152"
accessed: 2026-08-25
source_tier: C
scope_role: bridge
temporal_role: classical-exposition
related: ["[[DDPM 反向后验、ELBO 与逐步 KL]]", "[[条件核、边缘一致性与统一离散扩散框架]]"]
created: 2026-08-25
updated: 2026-08-25
---
# 生成扩散模型漫谈（二）：DDPM = 自回归式 VAE

> [!abstract] 来源定位
> 文章把 $x_{1:T}$ 看作层次 latent variables，把 DDPM ELBO 读成多层 VAE，是 GEN-42 的教学桥。课程用“时间方向上的递归条件分布”这一精确表述，不把 diffusion 与 token autoregression 或一般 NVAE 宣称为逐层同构。

## 边界

- forward variational posterior $q(x_{1:T}\mid x_0)$ 固定；reverse generative model $p_\theta(x_{0:T})$ 学习；
- 参数跨时间共享、每步 Gaussian 结构和固定 noising 使它不同于一般 hierarchical VAE；
- “容易训练”“不应用 BatchNorm”“sum loss 必须优于 mean loss”均是实现经验，需要 learning-rate/dtype/normalization 受控实验；
- 原文提醒其 $\alpha_t,\beta_t$ 与原论文不同，本卷不混用两套符号。

一级来源：[[S-2020-Ho-DDPM]]、[[S-2021-Nichol-Dhariwal-Improved-DDPM]]。

