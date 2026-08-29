---
type: source
status: active
area: [sources, neural-networks, gradient-penalty, wgan, lipschitz]
source_type: paper
title: "Improved Training of Wasserstein GANs"
author: "Ishaan Gulrajani; Faruk Ahmed; Martin Arjovsky; Vincent Dumoulin; Aaron Courville"
year: 2017
url: "https://proceedings.neurips.cc/paper/2017/hash/892c3b1c6dccd52936e27cbd0ff683d6-Abstract.html"
venue: "NeurIPS 2017"
accessed: 2026-08-24
source_tier: A
license: "NeurIPS proceedings paper；本库仅保存独立摘要、必要公式与链接"
scope_role: task-specific-gradient-penalty
temporal_role: foundational
related: ["[[Jacobian、Gradient Penalty 与 Lipschitz 正则接口]]"]
created: 2026-08-24
updated: 2026-08-29
---

# Gulrajani et al.：WGAN Gradient Penalty

> [!abstract] 来源定位
> 论文以真实—生成样本插值点上 critic 输入梯度 norm 接近 1 的 penalty 替代 weight clipping。它承担 WGAN-GP 的原始对象与实验来源；target norm 1 来自 critic/Wasserstein 语境，不是所有监督模型 smoothness penalty 的默认选择。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| GP-C1 | penalty 作用于 scalar critic 对插值输入的 gradient norm | 定义 | 插值分布与 norm 已声明 | 精确 |
| GP-C2 | 它避免原始 weight clipping 的部分优化问题 | 经验机制 | 论文 GAN 设置 | 有证据 |
| GP-C3 | sampled penalty 严格执行全域 1-Lipschitz | 证书外推 | 仅有限路径/点 | 错误 |
| GP-C4 | target 1 可直接用于任意分类 loss gradient | 对象外推 | scalar critic 与 loss/logit 不同 | 错误 |
