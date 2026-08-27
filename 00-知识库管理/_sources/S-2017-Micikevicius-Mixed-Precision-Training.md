---
type: source
status: verified
area: [sources, ai-training, mixed-precision]
source_type: paper
title: "Mixed Precision Training"
author: "Paulius Micikevicius et al."
year: 2017
url: "https://arxiv.org/abs/1710.03740"
accessed: 2026-08-26
source_tier: A
license: "arXiv / conference paper；知识库仅保存独立摘要与链接"
scope_role: canonical
temporal_role: foundational
related: ["[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]", "[[Loss Scaling、Master Weight 与低精度梯度累积]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Mixed Precision Training

> [!abstract] 来源定位
> 混合精度训练的奠基性实验来源。论文把 FP16 权重/激活/梯度与 FP32 主权重、loss scaling 组合起来，说明“低精度训练”不是把整张计算图统一 cast 成一种 dtype。

## 可调用证据

- FP16 的有限范围会让小梯度 underflow；放大 loss 可在反向链上整体放大梯度；
- 更新前必须反缩放，且 Inf/NaN 检查决定该 step 是否执行；
- FP32 master weights 用于积累小于 FP16 当前 ulp 的更新；
- 论文在当时多类网络上展示与 FP32 接近的训练质量和约两倍内存节省。

## 边界

- 实验结论绑定论文的模型、硬件和 FP16 policy，不自动覆盖 BF16/FP8 或今天的 fused kernel；
- loss scaling 改善 range，不增加 significand precision；
- 论文流程不替代当前框架对 skipped step、scheduler 和 distributed state 的实现合同。
