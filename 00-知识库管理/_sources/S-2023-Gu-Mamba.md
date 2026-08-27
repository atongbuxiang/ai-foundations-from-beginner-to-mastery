---
type: source
status: draft
area: [sources, architecture/ssm, efficient-sequence-models]
source_type: paper
title: "Mamba: Linear-Time Sequence Modeling with Selective State Spaces"
author: "Albert Gu, Tri Dao"
year: 2023
url: "https://arxiv.org/abs/2312.00752"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[选择性状态空间、Mamba 与证据边界]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Mamba: Linear-Time Sequence Modeling with Selective State Spaces

> [!abstract] 来源定位
> Mamba 让离散 SSM 的部分参数依赖当前输入，用选择性传播/遗忘补足固定 LTI 核的内容无关性；这破坏了单个固定 convolution kernel，于是论文以 hardware-aware selective scan 实现并行训练接口。

## 课程采用的断言

| 断言 | 边界 |
|---|---|
| 序列长度上的算术可线性增长 | 不等于任意硬件、batch 与长度下墙钟时间都优于 Attention |
| 输入依赖参数提供 content-conditioned state update | 选择性是架构机制，非“自动检索正确事实”的保证 |
| 固定卷积路径失效 | 仍可利用 associative scan/融合 kernel，但接口、IO 和数值要另审计 |
| 论文报告若干模态与语言建模结果 | 只归属于论文版本、数据、规模与 baseline |

## 版本

课程以 arXiv v2（2024-05-31）为基准；后续 Mamba 变体不倒写入本卡。

