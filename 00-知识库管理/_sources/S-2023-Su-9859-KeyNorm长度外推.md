---
type: source
status: draft
area: [sources, ai/attention, ai/length-extrapolation]
source_type: blog
title: "Transformer升级之路：15、Key归一化助力长度外推"
author: 苏剑林
year: 2023
url: "https://spaces.ac.cn/archives/9859"
accessed: 2026-08-24
source_tier: C
license: "科学空间；仅保存独立摘要与链接"
scope_role: empirical-bridge
temporal_role: active-research
related: ["[[Scaled Dot-Product Attention 与 Softmax 数值语义]]", "[[Attention 失效模式、反例与证据地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Key 归一化与长度外推：小模型证据

> [!abstract] 来源定位
> 文章研究 key normalization/Cosine Attention 对长度外推的影响，并报告约一亿参数 GAU、训练长度 512、测试到 4096 的实验线索。课程用于提出“logit 尺度随长度/范数变化”的诊断，不把小模型观察外推为大模型定律。

## 证据账本

| 内容 | 等级 | 课程处理 |
|---|---|---|
| key 归一化改变 dot-product 中 norm 通道 | `I` | 由代数直接核验 |
| 文中 KNA/CosA 在所述设置改善外推 | `E` | 保留模型、训练/测试长度与指标 |
| 放大模型后仍同样有效 | `O` | 原文亦未充分验证，不写成结论 |
| 归一化解决一切长度外推 | 过度外推 | 不采用 |

## 后续实验

长度扫描时同步记录 logit mean/std/max、row entropy、top-k mass、梯度、困惑度与 wall-clock；分别改变 position scheme、normalization、temperature 和训练长度。
