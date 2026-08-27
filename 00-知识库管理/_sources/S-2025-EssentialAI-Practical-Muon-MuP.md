---
type: source
status: verified
area: [sources, muon, mup, scale-up, hyperparameter-search]
source_type: preprint
title: "Practical Efficiency of Muon for Pretraining"
author: [Ishaan Shah, Anthony M. Polloreno, Karl Stratos, Philip Monk, Adarsh Chaluvaraju, Andrew Hojel, Andrew Ma, Anil Thomas, Ashish Tanwer, Darsh J Shah, Khoi Nguyen, Kurt Smith, Michael Callahan, Michael Pust, Mohit Parmar, Peter Rushton, Platon Mazarakis, Ritvik Kapila, Saurabh Srivastava, Somanshu Singla, Tim Romanski, Yash Vanjani, Ashish Vaswani]
year: 2025
url: "https://arxiv.org/abs/2505.02222"
accessed: 2026-08-26
source_tier: B
scope_role: practical-scale-up-evidence
temporal_role: current-research
related: ["[[Scale-up 协议、μP 证据与失效边界]]", "[[Muon 的扩展证据、系统成本与迁移边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Practical Efficiency of Muon for Pretraining

> [!abstract] 来源定位
> 论文研究 Muon 预训练效率，并把 Muon 与 μP 组合用于超参数迁移；其中 telescoping/multiscale 搜索用于吸收有限宽、实现和尺度迁移误差。本卷只调用其 scale-up 协议思想和最高约 4B 参数的论文内证据。

## 正文采用

- 不把“一跳 zero-shot”当唯一工程方案；可以沿尺度梯逐段确认最优区间是否漂移；
- 训练、调参、确认与失败运行都应计入扩展预算；
- optimizer、batch、数据分布和架构改变会产生 μP 之外的迁移误差；
- 目标规模仍需有限确认预算和安全门。

## 限制

Muon 相对 AdamW 的 Pareto、critical-batch 与数据效率结论都限定于论文的模型、实现、系统和预算。telescoping 是实用研究协议，不是原始 μTransfer 定义的一部分，也不能掩盖在目标规模重新大范围调参的成本。

