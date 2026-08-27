---
type: source
status: verified
area: [sources, generative-models, gan, stabilization]
source_type: paper
title: "Improved Techniques for Training GANs"
author: "Tim Salimans et al."
year: 2016
url: "https://arxiv.org/abs/1606.03498"
venue: "NeurIPS 2016"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: empirical-techniques
temporal_role: historical
related: ["[[Mode Collapse、模式覆盖与生成器熵]]", "[[GAN 稳定化方法、受控比较与证据地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Salimans et al.：GAN 训练技巧

> [!abstract] 来源定位
> 论文提出 feature matching、minibatch discrimination、historical averaging 等组合技巧，并给特定图像/半监督设置证据。课程将每项视为改变 generator objective、batch interaction 或 optimizer 的经验干预，不把组合结果归因于单一方法。

## 边界

- minibatch discrimination 可暴露重复样本，但使 critic 对整个 batch 依赖；
- feature matching 不再直接优化原 generator minimax loss；
- Inception Score 依赖分类器与 label entropy，不能单独量化真实分布覆盖；
- 多技巧组合必须用同预算消融才能做因果归因。

