---
type: source
status: verified
area: [sources, ai-training, low-precision, attention]
source_type: blog
title: "低精度 Attention 可能存在有偏的舍入误差"
author: 苏剑林
year: 2025
url: "https://spaces.ac.cn/archives/11371"
accessed: 2026-08-26
source_tier: B
license: "作者博客；仅保存独立摘要、短记号映射与链接"
scope_role: exposition
temporal_role: active-research
related: ["[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]", "[[随机舍入、无偏性与微小更新保留]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 科学空间：低精度 Attention 可能存在有偏的舍入误差

> [!abstract] 来源定位
> 文章以低精度 Attention 个例串起格式、舍入偏差与训练崩溃的因果疑问，是本卷的中文问题入口。作者明确追问偏差究竟是崩溃的因还是果，因此课程把它用作竞争解释，而非“低精度必然导致 Attention 崩溃”的定论。

## 可调用内容

- 确定性近邻舍入在非对称数值分布上可能产生条件偏差；
- Attention 概率集中、低精度乘加和归一化之间可能形成反馈；
- 对 Attention 计算做干预能改变异常指标，但干预结果本身仍不足以完成因果归因；
- 正常小模型的注意力集中度未必达到论文假设区间，提醒外推必须绑定尺度和状态。

## 边界

- 浮点格式和舍入定义回查 IEEE/厂商与数值分析来源；
- 单个 Attention 机制不代表所有 GEMM、优化器或分布式归约；
- “干预有效”需与首个异常 step、机制中介和替代故障解释一起报告。
