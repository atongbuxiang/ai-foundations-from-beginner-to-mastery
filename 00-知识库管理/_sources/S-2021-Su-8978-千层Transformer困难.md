---
type: source
status: active
area: [sources, scientific-spaces, transformers, initialization, depth-scaling]
source_type: blog
title: "训练1000层的Transformer究竟有什么困难？"
author: [苏剑林]
year: 2022
url: "https://spaces.ac.cn/archives/8978"
accessed: 2026-08-23
source_tier: C
venue: "科学空间"
related: ["[[LSUV、Fixup 与现代初始化诊断]]", "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]", "[[ReZero、Fixup、DeepNorm 与深网缩放]]", "[[Transformer Block、残差、归一化与 FFN]]", "[[Transformer 表达、稳定性与证据边界]]", "[[S-2022-Wang-DeepNet]]"]
created: 2026-08-23
updated: 2026-08-24
---
# 苏剑林 2022：千层 Transformer 的尺度困难

> [!abstract] 来源定位
> 文章以深层 Transformer 的梯度量级、残差路径与初始化缩放讨论极深训练困难。本库把它作为中文问题入口和系统尺度审计案例；具体架构结论需回查相应论文，且不把 Transformer 经验直接外推到普通 MLP/CNN。

## 核心调用边界

- 文中把随参数矩阵数量累积的模型更新量称为“增量爆炸”，是特定近似与尺度分析；
- $\alpha=(2N)^{1/4},\lambda=(2N)^{-1/4}$ 的讨论与 DeepNet 参数化相连，具体 encoder/decoder 系数回查原论文；
- “梯度不爆仍训练困难”是重要问题提醒，但不证明增量尺度是唯一机制；
- warm-up、初始化、residual scale、optimizer 与 normalization 必须联合实验；
- 千层可训练是论文设置下 `E`，不是所有任务更深都更优。

> [!note] 文件名兼容
> 该网页发布日期为 2022-03-09；文件名中的 `2021` 是早期索引遗留，为避免破坏已有 Wiki 链接暂不改名，正文元数据以网页日期为准。
