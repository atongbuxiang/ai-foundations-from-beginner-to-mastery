---
type: source
status: draft
area: [sources, neural-networks, dropconnect, weight-noise]
source_type: paper
title: "Regularization of Neural Networks using DropConnect"
author: "Li Wan; Matthew Zeiler; Sixin Zhang; Yann LeCun; Rob Fergus"
year: 2013
url: "https://proceedings.mlr.press/v28/wan13.html"
venue: "ICML 2013"
accessed: 2026-08-24
source_tier: A
license: "PMLR paper；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[DropConnect、权重噪声与激活噪声]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Wan et al.：DropConnect

> [!abstract] 来源定位
> 论文把随机删除对象从 activations 改为 individual weights，使每个输出 unit 接收随机连接子集，并给出当时视觉任务实验和理论分析。它承担 DropConnect 的原始定义；本库另行推导它与 activation dropout 在输出协方差、mask storage 和 kernel 形状上的差异。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| DC-C1 | DropConnect 对 weight entries 采样 mask | 定义 | 声明 keep rate 与缩放 | 精确 |
| DC-C2 | 单输出 conditional variance 可与某些 activation-noise 形式匹配 | 二阶矩 | 独立 mask 与相同尺度 | 条件成立 |
| DC-C3 | 因方差匹配，两者完整 joint law 和梯度都相同 | 分布外推 | 输出协方差/mask 共享不同 | 错误 |
| DC-C4 | unstructured weight mask 必然带来训练加速 | 系统外推 | 可能破坏 dense GEMM | 不成立 |
