---
type: source
status: verified
area: [sources, generative-models, energy-based-models, neural-ebm]
source_type: paper
title: "Implicit Generation and Generalization in Energy-Based Models"
author: "Yilun Du; Igor Mordatch"
year: 2019
url: "https://arxiv.org/abs/1903.08689"
venue: "arXiv / NeurIPS-era work"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: case-study
temporal_role: classical
related: ["[[能量模型、未归一化密度与配分函数]]", "[[最大似然的正相负相、对比散度与噪声对比估计]]", "[[Langevin、ULA、MALA 与平稳分布]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Du–Mordatch：Neural EBM 的隐式生成

> [!abstract] 来源定位
> 论文展示 replay buffer、随机重启和有限步 Langevin 可将 neural EBM 扩展到高维视觉任务，并报告生成、修复与若干泛化实验。它是工程可行性案例，不是 finite-step MCMC 无偏或 mode coverage 的一般证明。

## 复现合同

必须记录：energy architecture、数据预处理、Langevin 步长/噪声、链长、buffer 替换率、随机重启率、温度、训练负样本 stop-gradient、测试链预算和评价模型。删除任一项，结果不可唯一解释。

## 边界

- replay samples 来自随训练变化的非平稳 kernel；
- 模型相误差会反馈到参数更新；
- 低温采样改变部署分布；
- compositional/OOD 等结论属于给定 benchmark；
- “likelihood-based”形式不等于 exact likelihood 已被可靠估计。

