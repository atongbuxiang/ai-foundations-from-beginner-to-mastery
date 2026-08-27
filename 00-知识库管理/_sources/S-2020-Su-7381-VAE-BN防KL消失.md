---
type: source
status: verified
area: [sources, generative-models/vae, optimization]
source_type: blog
title: "变分自编码器（五）：VAE + BN = 更好的VAE"
author: 苏剑林
year: 2020
url: "https://spaces.ac.cn/archives/7381"
accessed: 2026-08-25
source_tier: C
license: "CC BY-NC-SA（按站点页脚；本卡仅保存独立摘要、短公式与链接）"
series: "变分自编码器"
series_order: 5
scope_role: core
temporal_role: classical-exposition
related: ["[[Posterior Collapse、率失真与解码器容量]]", "[[S-2019-He-Lagging-Inference]]"]
created: 2026-08-25
updated: 2026-08-25
---

# 变分自编码器（五）：VAE + BN = 更好的 VAE

> [!abstract] 来源定位
> 文章从对角 Gaussian KL 的非负分项出发，用 batch normalization 控制编码均值的批内二阶矩，从而为平均 KL 构造正下界，并讨论 NLP VAE 的 KL vanishing。课程采用其可复算不等式和训练诊断；“BN 是 VAE 标配”只视为方法建议，不作跨架构定理。

## 不等式骨架

$$
KL\bigl(\mathcal N(\mu,\operatorname{diag}\sigma^2)\Vert\mathcal N(0,I)\bigr)
=\frac12\sum_j(\mu_j^2+\sigma_j^2-\log\sigma_j^2-1)
\ge\frac12\lVert\mu\rVert^2.
$$

若批内每维 $\mu_j$ 的均值/方差受控，平均 KL 获得相应下界。这个结论依具体 BN 参数与 batch statistics；正 KL 不自动保证 latent 含有有用信息。

## 课程边界

- KL vanishing 是 $q(z\mid x)=p(z)$ 的特例；“posterior 不依赖 $x$”可有更广义形式；
- 强制 rate 大于零可能编码噪声或无关信息；
- BN 引入 batch dependence、running statistics 与 train/eval 差异；
- 原文经验与 ACL 方法需按文本模型设置复现，不能直接外推所有 CV VAE。

