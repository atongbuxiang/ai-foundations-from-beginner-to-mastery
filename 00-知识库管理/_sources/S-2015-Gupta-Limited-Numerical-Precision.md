---
type: source
status: verified
area: [sources, ai-training, stochastic-rounding]
source_type: paper
title: "Deep Learning with Limited Numerical Precision"
author: "Suyog Gupta, Ankur Agrawal, Kailash Gopalakrishnan, Pritish Narayanan"
year: 2015
url: "https://proceedings.mlr.press/v37/gupta15.html"
accessed: 2026-08-26
source_tier: A
license: "PMLR paper；知识库仅保存独立摘要与链接"
scope_role: foundational
temporal_role: foundational
related: ["[[随机舍入、无偏性与微小更新保留]]", "[[训练量化、优化器状态压缩与 QAT]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Deep Learning with Limited Numerical Precision

> [!abstract] 来源定位
> 论文在低精度定点训练中突出 stochastic rounding 的作用，是把“微小更新被确定性舍入抹掉”转成可计算随机估计器的经典来源。

## 可调用证据

- 对相邻格点按距离随机选择，可使单次量化满足条件无偏；
- 确定性 round-to-nearest 会让小于半个量化步的同号更新持续消失；
- 论文展示 16-bit fixed-point 配 stochastic rounding 的当时网络训练结果；
- 数值格式、舍入器与累加器必须联合报告。

## 边界

- 单步条件无偏不保证非线性优化轨迹、停止时间或最终模型无偏；
- 方差会累积，随机数质量和并行实现也进入误差；
- 论文的 fixed-point 实验不能直接替代 FP16/BF16/FP8 的格式分析。
