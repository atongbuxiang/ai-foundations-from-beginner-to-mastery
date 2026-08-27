---
type: source
status: verified
area: [sources, representation-learning, identifiability]
source_type: paper
title: "Challenging Common Assumptions in the Unsupervised Learning of Disentangled Representations"
author: [Francesco Locatello, Stefan Bauer, Mario Lucic, Gunnar Rätsch, Sylvain Gelly, Bernhard Schölkopf, Olivier Bachem]
year: 2018
url: "https://arxiv.org/abs/1811.12359"
accessed: 2026-08-25
source_tier: A
scope_role: counterpoint
temporal_role: classical
related: ["[[VAE 的条件、聚类、解耦主张与证据地图]]", "[[表示坍缩、非坍缩与可辨识边界]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Locatello et al.：无监督解耦的不可识别边界

> [!abstract] 来源定位
> 论文给出无监督 disentanglement 在缺少数据/模型归纳偏置时不可识别的构造，并以大规模实验显示常见指标、seed 和方法选择高度敏感。课程用它阻止“factorized Gaussian prior 自动恢复真实语义因素”的过强结论。

## 课程边界

- 不可能性针对未声明归纳偏置/监督的广泛设置，不是说任何弱监督、组变换或因果结构下都不能识别；
- coordinate independence 不等于与 ground-truth factors 对齐；
- downstream usefulness 必须直接测，不由 disentanglement score 代替；
- 任何成功主张需写明 supervision、augmentations、architecture 和 model-selection signal。

