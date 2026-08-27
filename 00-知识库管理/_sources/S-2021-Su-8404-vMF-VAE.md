---
type: source
status: verified
area: [sources, generative-models/vae, directional-statistics]
source_type: blog
title: "变分自编码器（七）：球面上的VAE（vMF-VAE）"
author: 苏剑林
year: 2021
url: "https://spaces.ac.cn/archives/8404"
accessed: 2026-08-25
source_tier: C
license: "CC BY-NC-SA（按站点页脚；本卡仅保存独立摘要、短公式与链接）"
series: "变分自编码器"
series_order: 7
scope_role: core
temporal_role: classical-exposition
related: ["[[层次 VAE、表达性先验与近似后验 Flow]]", "[[S-2018-Davidson-Hyperspherical-VAE]]"]
created: 2026-08-25
updated: 2026-08-25
---

# 变分自编码器（七）：球面上的 VAE

> [!abstract] 来源定位
> 文章从超球面均匀分布和 von Mises–Fisher 分布进入球面 latent，详细讨论方向/浓度、采样与固定浓度下的 KL。课程采用其方向统计中文推导；采样正确性、Bessel 常数与 pathwise/rejection gradient 回查原论文。

## 核心对象

在 $S^{d-1}$ 上

$$
q(z\mid x)=C_d(\kappa)e^{\kappa\mu(x)^\top z},
\qquad \lVert\mu(x)\rVert=\lVert z\rVert=1.
$$

$\kappa=0$ 为球面均匀分布；固定 $d,\kappa>0$ 时，相对均匀 prior 的 KL 不依赖方向 $\mu$，可成为正的常数。

## 边界

- 正 KL 常数防止“数值为零”，不证明 $Z$ 携带关于 $X$ 的有用互信息；
- 球面 prior 改变 support/topology，不只是换一个正则系数；
- 固定半径适合方向性 latent 的经验主张依任务；
- normalization、sampling 和 rejection/pathwise gradient 都要纳入训练成本。

