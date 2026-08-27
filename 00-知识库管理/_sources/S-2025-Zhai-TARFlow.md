---
type: source
status: verified
area: [sources, generative-models, normalizing-flows, transformer]
source_type: paper
title: "Normalizing Flows are Capable Generative Models"
author: "Shuangfei Zhai; Ruixiang Zhang; Preetum Nakkiran; David Berthelot; Jiatao Gu; Huangjie Zheng; Tianrong Chen; Miguel A. Bautista; Navdeep Jaitly; Josh Susskind"
year: 2025
url: "https://arxiv.org/abs/2412.06329"
venue: "ICML 2025"
accessed: 2026-08-25
source_tier: A
scope_role: frontier
temporal_role: active-research
related: ["[[Flow 的 Support、Dequantization、TARFLOW 与证据地图]]", "[[Autoregressive Flow、MAF 与 IAF 的方向权衡]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Zhai et al.：TARFlow

> [!abstract] 来源定位
> TARFlow 是 patch-level Transformer autoregressive flow，交替方向堆叠，并用 Gaussian augmentation、post-training denoising 与 guidance 改善样本。论文在指定图像 benchmark 上报告强 likelihood 与接近 diffusion 的质量/多样性；课程将 core flow 与三个部署增强分开消融。

## 复现边界

- training density 对应 noisy pixels；post-denoise 改变输出分布；
- guidance 又改变部署分布，未必保留训练 likelihood；
- autoregressive inverse 的串行 critical path 使“一步模型”不等于低 latency；
- 参数量、硬件、batch、precision、NFE/transformer calls 与 evaluator 必须 compute-match；
- 2025 STARFlow 与 2026 iTARFlow 是后续工作，不是原 TARFlow 结果。

