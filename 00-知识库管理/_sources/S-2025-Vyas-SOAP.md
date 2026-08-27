---
type: source
status: verified
area: [sources, optimization, shampoo, adam]
source_type: paper
title: "SOAP: Improving and Stabilizing Shampoo Using Adam for Language Modeling"
author: [Nikhil Vyas, Depen Morwani, Rosie Zhao, Itai Shapira, David Brandfonbrener, Lucas Janson, Sham Kakade]
year: 2025
url: "https://openreview.net/pdf?id=IDxZhXrpNf"
venue: "ICLR 2025"
accessed: 2026-08-26
source_tier: A
scope_role: primary-frontier
temporal_role: current-method
related: ["[[SOAP、二阶混合优化器与成本证据地图]]", "[[Shampoo、逆矩阵根与 Kronecker 预条件]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Vyas et al.：SOAP

> [!abstract] 来源定位
> SOAP 的正式 ICLR 2025 来源。核心解释是：在 Shampoo preconditioner 的特征基中持续运行 Adam 式一阶/二阶统计；以 half-power 版本连接 Shampoo 与 rotated Adafactor，并降低稀疏 eigendecomposition refresh 带来的性能退化。

## 课程采用

- basis statistics、eigendecomposition refresh、rotated first/second moments、decay 和 fallback 分开记账；
- “在旋转坐标中运行 Adam”需要同时追踪 basis 改变时 state 如何表达，不能只画一次静态旋转；
- 论文在 360M/660M language-model pretraining 的 iteration 与 wall-time 改善是指定 batch、hardware、implementation 与 tuning 下的经验结果；
- 官方仓库自称 preliminary implementation，低精度与 distributed 支持应以使用时版本复核。

## 不作的外推

不把 SOAP 与 exact natural gradient/Hessian 等同；不把少迭代直接写成全场景少 FLOPs、少显存或更好泛化。
