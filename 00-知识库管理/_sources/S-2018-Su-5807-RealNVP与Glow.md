---
type: source
status: verified
area: [sources, generative-models, normalizing-flows]
source_type: blog
title: "细水长 flow 之 RealNVP 与 Glow：流模型的传承与升华"
author: 苏剑林
year: 2018
url: "https://spaces.ac.cn/archives/5807"
accessed: 2026-08-25
source_tier: C
license: "科学空间站点许可；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: classical-exposition
related: ["[[Coupling Layer、NICE 与 RealNVP]]", "[[Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]"]
created: 2026-08-25
updated: 2026-08-25
---
# 细水长 flow 之 RealNVP 与 Glow

> [!abstract] 来源定位
> 文章沿 NICE→affine coupling→multiscale→Glow 的历史结构解释 flow，是 GEN-34—35 的中文主线。本卷保留方向合同：编码 $z=f(x)$ 时 density 使用 $\log|\det J_f|$；生成 $x=f^{-1}(z)$ 时符号相反，不能只背一条公式。

## 断言与边界

- affine coupling 的 Jacobian 为块三角，logdet 是 scale 输出之和：精确；
- Glow 的 invertible $1\times1$ convolution 学习 channel mixing：精确；图像 $H\times W$ 上 logdet 为 $HW\log|\det W|$；
- ActNorm 的 data-dependent initialization 不等于 batch normalization 的 batch-dependent forward；
- split/multiscale 可节省后续计算，但 latent factorization 与信息分配是模型假设；
- 2018 Keras 实现只作历史案例，不作当前 API 证据。

一级来源由 [[S-2016-Dinh-RealNVP]] 与 [[S-2018-Kingma-Dhariwal-Glow]]承担。

