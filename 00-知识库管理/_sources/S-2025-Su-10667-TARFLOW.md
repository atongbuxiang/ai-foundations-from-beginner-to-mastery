---
type: source
status: verified
area: [sources, generative-models, normalizing-flows, transformer]
source_type: blog
title: "细水长 flow 之 TARFLOW：流模型满血归来？"
author: 苏剑林
year: 2025
url: "https://spaces.ac.cn/archives/10667"
accessed: 2026-08-25
source_tier: C
license: "科学空间站点许可；本库仅保存独立摘要、必要公式与链接"
scope_role: frontier-bridge
temporal_role: active-research
related: ["[[Flow 的 Support、Dequantization、TARFLOW 与证据地图]]", "[[去噪 Score Matching、Tweedie 公式与条件期望]]"]
created: 2026-08-25
updated: 2026-08-25
---
# 细水长 flow 之 TARFLOW

> [!abstract] 来源定位
> 文章解释 Transformer autoregressive blocks、Gaussian noise augmentation、Tweedie post-denoise 与 guidance，并特别指出 TARFLOW 的某一方向仍需串行 inversion。课程采用“强 flow 结果来自 architecture + augmentation + denoise + guidance 的组合”这一证据账，不把标题问句升级为家族胜负。

## 断言审计

- TARFLOW 可视为 patch-level Transformer MAF：论文定义；
- noise augmentation 后 flow 学的是平滑 density：精确对象变化；
- $y+\sigma^2\nabla_y\log q_\theta(y)$ 是 posterior-mean 去噪：只有在 Gaussian/noisy-density 近似条件下；
- autoregressive direction 一侧并行、一侧串行：由 triangular dependency 决定；
- “逼近 SOTA/流模型归来”：截至指定数据、预算和 evaluator 的实验结论。

一级来源：[[S-2025-Zhai-TARFlow]]；2025 STARFlow 与 2026 iTARFlow 只作后续时间线，不回写成原论文结论。

