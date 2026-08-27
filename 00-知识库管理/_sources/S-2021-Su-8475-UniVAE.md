---
type: source
status: verified
area: [sources, generative-models/vae, text-generation]
source_type: blog
title: "UniVAE：基于Transformer的单模型、多尺度的VAE模型"
author: 苏剑林
year: 2021
url: "https://spaces.ac.cn/archives/8475"
accessed: 2026-08-25
source_tier: C
license: "CC BY-NC-SA（按站点页脚；本卡仅保存独立摘要、短公式与链接）"
scope_role: bridge
temporal_role: active-research
related: ["[[层次 VAE、表达性先验与近似后验 Flow]]", "[[VAE 的条件、聚类、解耦主张与证据地图]]", "[[Attention Mask、因果性与可见性合同]]"]
created: 2026-08-25
updated: 2026-08-25
---

# UniVAE：单模型、多尺度文本 VAE

> [!abstract] 来源定位
> 文章通过 Transformer attention mask 把 encoder 与 autoregressive decoder 合并，并将不同层的 `[CLS]` 表示视为多尺度 latent；还明确讨论长度泄漏、降维和层级控制。课程采用它作为“架构 mask、latent hierarchy、信息泄漏必须联审”的研究案例，不把其解耦直觉写成 theorem。

## 关键合同

- decoder 只能访问被选定层的 `[CLS]` latent 与已生成前缀；
- 不同层 latent 具有不同 receptive depth，但“控制语义层级”需 intervention 实验；
- 输入输出拼接会把 decoder 起始位置/输入长度变成额外条件；
- 前层表示能力较弱是架构假说，不自动推出应删除哪些 latent；
- coordinate independence、低相关与语义 disentanglement 是不同命题。

## 调用

GEN-15 用它讨论多尺度 inference/generative path，GEN-16 用 length leakage 作为“看似可解释 latent 其实偷带 side information”的反例。

