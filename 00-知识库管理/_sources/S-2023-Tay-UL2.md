---
type: source
status: verified
area: [sources, language-modeling, denoising, ul2]
source_type: paper
title: "UL2: Unifying Language Learning Paradigms"
author: "Yi Tay et al."
year: 2023
url: "https://arxiv.org/abs/2205.05131"
accessed: 2026-08-26
source_tier: P1
license: "ICLR 2023 论文；本库仅保存独立摘要、对象合同与链接"
scope_role: primary
temporal_role: mixture-of-denoisers
related: ["[[Mixture-of-Denoisers、UL2 与多目标采样]]"]
created: 2026-08-26
updated: 2026-08-26
---

# UL2：Mixture-of-Denoisers

> [!abstract] 来源定位
> UL2 明确拆分 architecture archetype 与 pretraining objective，并以 Mixture-of-Denoisers 组合不同 corruption/sequential regimes。课程采用其层级 sampler 与 R/S/X denoiser 问题地图；性能结论只在论文控制变量和公开 checkpoint 范围内成立。

## 课程补严

配置中的 mode probability $\pi_m$ 不等于实际 loss/gradient 权重。必须同步记录：每 mode 的样本频率、corruption rate、有效 target 数、loss reduction、encoder/decoder token 成本和梯度统计。若这些量不同，名义 `1:1:1` mixture 也不是等梯度贡献。

