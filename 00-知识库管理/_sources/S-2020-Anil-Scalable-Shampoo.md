---
type: source
status: verified
area: [sources, optimization, distributed-training, shampoo]
source_type: paper
title: "Scalable Second Order Optimization for Deep Learning"
author: [Rohan Anil, Vineet Gupta, Tomer Koren, Kevin Regan, Yoram Singer]
year: 2020
url: "https://arxiv.org/abs/2002.09018"
accessed: 2026-08-26
source_tier: B
scope_role: systems-and-evidence
temporal_role: scaling-reference
related: ["[[Shampoo、逆矩阵根与 Kronecker 预条件]]", "[[SOAP、二阶混合优化器与成本证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Anil et al.：Scalable Shampoo

> [!abstract] 来源定位
> 将 Shampoo/full-matrix AdaGrad 变体扩展到大型深度模型的系统与经验来源，强调 inverse-root 数值算法、较低频率更新、block 切分、grafting 与 CPU/accelerator 异构执行。

## 课程采用与边界

- 把 preconditioner statistics update、inverse-root refresh 与每步 apply 分成三个时钟；
- 单独记录 block size、precision、root residual、grafting、momentum、communication 和 amortized wall time；
- 原文在 Transformer/BERT/Criteo/ResNet 等任务的结果是特定系统证据，不将“second order”标签或少迭代直接等同于少总时间；
- 当代实现可进一步支持 sharding/quantized communication，但需按具体版本重新核对。
