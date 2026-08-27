---
type: source
status: verified
area: [sources, optimization, clipping, normalization-free]
source_type: paper
title: "High-Performance Large-Scale Image Recognition Without Normalization"
author: "Brock et al."
year: 2021
url: "https://arxiv.org/abs/2102.06171"
accessed: 2026-08-26
source_tier: A
scope_role: original-method-and-evidence
related: ["[[全局逐层梯度裁剪、AGC 与裁剪偏差]]", "[[权重衰减、尺度不变性与 Weight RMS 动力学]]", "[[Update-to-Weight Ratio、谱与尺度诊断]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Brock 等：NFNet 与 Adaptive Gradient Clipping

> [!abstract] 来源定位
> 论文为无归一化残差网络引入 AGC，用参数单元范数相对地限制梯度范数，并报告大 LR/强增强下的稳定性与 ImageNet 结果。课程采用 clipping contract，不外推其阈值或性能到所有架构。

## 课程采用

对参数单元 $W_i$，AGC 比较

$$
\frac{\lVert G_i\rVert}{\max(\lVert W_i\rVert,\epsilon)}
$$

与阈值，并只缩小超过阈值的 $G_i$。单元轴、epsilon、bias/norm 参数是否参与、在 accumulation/reduction 前后裁剪都属于算法定义。
