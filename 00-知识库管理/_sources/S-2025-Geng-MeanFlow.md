---
type: source
status: verified
area: [sources, generative-models, meanflow, flow-matching]
source_type: paper
title: "Mean Flows for One-step Generative Modeling"
author: "Zhengyang Geng; Mingyang Deng; Xingjian Bai; J. Zico Kolter; Kaiming He"
year: 2025
url: "https://arxiv.org/abs/2505.13447"
accessed: 2026-08-25
source_tier: A
scope_role: frontier
related: ["[[平均速度、MeanFlow 与有限步生成]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Geng et al.：MeanFlow

> [!abstract] 来源定位
> 原论文引入沿实际轨迹、有限时间区间的 average velocity，并用它与 instantaneous velocity 的恒等式构造无需 teacher 的一步生成训练。

若 $z_s$ 是从 $r$ 到 $t$ 的轨迹，

$$u(z_t,r,t)=\frac1{t-r}\int_r^t v(z_s,s)\,ds$$

是 path average，不是固定空间点上对两个端点速度取算术平均。原论文的一步 ImageNet 结果是前沿经验；composition、unseen interval 与 encoder/guidance 依赖必须另测。
