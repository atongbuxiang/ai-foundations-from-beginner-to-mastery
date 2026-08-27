---
type: source
status: verified
area: [sources, generative-models, score-based-models, langevin]
source_type: paper
title: "Generative Modeling by Estimating Gradients of the Data Distribution"
author: "Yang Song; Stefano Ermon"
year: 2019
url: "https://arxiv.org/abs/1907.05600"
venue: "NeurIPS 2019"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: foundational
related: ["[[多噪声尺度、退火去噪与 Score 网络]]", "[[Langevin、ULA、MALA 与平稳分布]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Song–Ermon：Noise Conditional Score Network

> [!abstract] 来源定位
> NCSN 用多级 Gaussian perturbation 学习 $s_\theta(x,\sigma_i)\approx\nabla_x\log p_{\sigma_i}(x)$，再从大噪声到小噪声执行 annealed Langevin。论文直接支持多尺度训练/采样协议与其实验，不支持“任意有限步链均为精确数据样本”。

## 断言审计

| 断言 | 课程判断 |
|---|---|
| 低维流形附近原始 score 可能未定义或难估 | 正确的问题动机；由 Gaussian smoothing 提供全维 density |
| 多噪声尺度改善低密度区连接 | 理论直觉 + 实验支持，非任意 schedule 的普遍定理 |
| annealed Langevin 以逐级 score 生成样本 | 算法定义 |
| 最后一级有限步输出等于 $p_0$ | 不成立；有 smoothing、score、mixing 与 step-size 误差 |

复现必须报告 noise ladder、每级步数、步长缩放、初始化、最后去噪与总 NFE。

