---
type: source
status: verified
area: [sources, ai/optimization, large-batch]
source_type: blog
title: "重新思考学习率与 Batch Size（一）：现状"
author: 苏剑林
year: 2025
url: "https://spaces.ac.cn/archives/11260"
accessed: 2026-08-26
source_tier: C
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
scope_role: supporting
related: ["[[Mini-batch 梯度、平均求和与有效 Batch]]", "[[梯度噪声协方差、Noise Scale 与 SDE 近似]]", "[[Critical Batch、隐式偏置与 SGD 证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 重新思考学习率与 Batch Size（一）：现状

> [!abstract] 来源定位
> 文章把 learning rate 与 batch size 放在统一随机更新尺度中分析，适合作为中文推导入口。本卷会自行固定 mean/sum、sampling、时间尺度与 covariance convention，并用 McCandlish 等原始工作和最小数值实验补证。

## 课程采用

- batch 增大降低 stochastic-gradient fluctuation；
- learning rate 与 batch 不能脱离 reduction 和 update convention 单独比较；
- “最优 batch”必须先说明效率口径与训练阶段。

## 保留意见

博客中的近似平衡式需逐条核对独立采样、局部平稳、小步长与模型假设；不能由量纲或均衡直觉推出泛化定理。

## 已核对的课程接口

- 页面回顾单样本梯度均值 $g$、协方差 $\Sigma$ 与 batch mean 协方差 $\Sigma/B$，再用二阶局部损失变化讨论学习率—batch 耦合；
- $S_{\min}$、$E_{\min}$ 与 noise scale 的关系是特定局部模型和效率口径下的推导对象，不是所有优化器/训练阶段共享的硬件吞吐定律；
- 本库分别由 [[Mini-batch 梯度、平均求和与有效 Batch]] 固定 reduction/sampling，由 [[梯度噪声协方差、Noise Scale 与 SDE 近似]] 固定随机近似条件，再由最小实验复算有限构造。

核对入口：[科学空间原文](https://spaces.ac.cn/archives/11260)；访问日 2026-08-26。
