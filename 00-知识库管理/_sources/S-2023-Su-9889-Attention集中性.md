---
type: source
status: draft
area: [sources, ai/attention, math/probability]
source_type: blog
title: "注意力机制真的可以‘集中注意力’吗？"
author: 苏剑林
year: 2023
url: "https://spaces.ac.cn/archives/9889"
accessed: 2026-08-24
source_tier: C
license: "科学空间；仅保存独立摘要与链接"
scope_role: analysis-bridge
temporal_role: active-research
related: ["[[Attention 的几何、核与概率视角]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]", "[[Attention 失效模式、反例与证据地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Attention 是否真的集中：集中度与分布假设

> [!abstract] 来源定位
> 文章把“集中注意力”转成可计算的权重集中/稀疏指标，并分析若干非负线性 Attention 在分布假设下的限制。课程采用其问题化方式：不凭热力图形状下结论，而报告 entropy、top-k mass、effective support 与输入分布。

## 课程采用与边界

- 同一 row 的 entropy、$\|a\|_2^2$、最大权重和 top-k mass 描述不同侧面；
- 均匀权重与 one-hot 权重给出直观端点，但实际权重的“好坏”取决于任务；
- 线性 Attention 的集中性结论依 feature map、维度、随机变量分布与归一化；
- 稀疏/集中不等于忠实解释，也不自动等于更高准确率；
- 下界或渐近估计须保留原分布假设，不能跨架构外推。

## 实验接口

按层、头、query 类型和长度报告权重指标分布，并与输出干预、任务指标和 logit 尺度联动；避免只挑一张最尖锐的 heatmap。
