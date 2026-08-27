---
type: source
status: draft
area: [sources, ai/transformers, rerope, long-context]
source_type: blog
title: "Transformer升级之路：12、无限外推的ReRoPE？"
author: 苏剑林
year: 2023
url: "https://spaces.ac.cn/archives/9708"
accessed: 2026-08-24
source_tier: C
license: "科学空间；仅保存独立摘要、方法合同与链接"
scope_role: frontier-method
temporal_role: long-context
related: ["[[长度外推、位置插值与 RoPE 缩放]]", "[[位置分辨率、混叠与长度外推评测]]"]
created: 2026-08-24
updated: 2026-08-24
---

# ReRoPE：截断相对相位的后处理

> [!abstract] 来源定位
> ReRoPE 把训练窗口内的相对位移保持原样，对窗口外位移使用截断/分段映射，试图避免未训练过的相对相位。标题问号是证据边界的一部分。

## 计算合同

目标相对位移函数可写为 $\rho(\Delta)=\min(\Delta,w)$（方向和 causal 约定另行处理）。由于 $\rho(i-j)$ 一般不能分解为两个独立绝对旋转，朴素实现需分块或两次 score 计算，改变推理成本与 cache kernel。

## 边界

文中小模型与 LLaMA 设置结果为 E；“无限”不是定理，也没有覆盖任意长度、数据、依赖任务、精度和硬件。必须同时测远程依赖及额外计算。
