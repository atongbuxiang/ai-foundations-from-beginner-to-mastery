---
type: source
status: active
area: [sources, neural-networks/normalization, vision]
source_type: paper
title: "Group Normalization"
author: "Yuxin Wu; Kaiming He"
year: 2018
url: "https://openaccess.thecvf.com/content_ECCV_2018/html/Yuxin_Wu_Group_Normalization_ECCV_2018_paper.html"
venue: "ECCV 2018"
accessed: 2026-08-23
source_tier: A
license: "CVF open-access author paper；本库仅保存独立摘要、短公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[InstanceNorm、GroupNorm 与 WeightNorm]]", "[[小批量、混合精度、分布式与因果归一化边界]]"]
created: 2026-08-23
updated: 2026-08-29
---

# Wu–He：Group Normalization

> [!abstract] 来源定位
> 论文针对小 batch 下 BatchNorm 统计估计不稳定，提出把同一样本的 channels 分组，并在组内 channels 与空间位置上计算均值方差。它给出 GN 的定义、与 LN/IN 的轴关系及视觉任务实验；本库补充 affine 参数差异、组大小退化与因果边界。

## 统计组

若 $C$ 被 $G$ 整除，每组含 $C/G$ 个 channels。固定样本 $n$ 与组 $g$，归约

$$
(c,h,w),\qquad c\in\mathcal C_g,
$$

名义组大小为

$$
m=\frac CGHW.
$$

论文实现使用 per-channel $\gamma_c,\beta_c$，而不是每个空间位置独立 affine。

## 断言表

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| GN-C1 | GN 不跨 batch 计算统计量 | 定义 | 分组与布局明确 | 已建立 |
| GN-C2 | $G=1$ 与 LN 共享归约统计 | 结构关系 | LN 需归约 $(C,H,W)$ | 统计核心等价 |
| GN-C3 | $G=C$ 与 IN 共享归约统计 | 结构关系 | 每组一个 channel | 统计核心等价 |
| GN-C4 | 小 batch 实验比 BN 稳定 | 经验 | 论文 ResNet/检测/分割设置 | 不外推所有任务 |

## 必须保留的细节

- “$G=1$ 等于 LayerNorm”若忽略 affine shape 会过强：PyTorch GN 是 per-channel affine，LayerNorm$(C,H,W)$ 是 per-element affine；
- “$G=C$ 等于 InstanceNorm”也要核对 affine 默认值与 running-state 选项；
- group count 是离散超参数，$C$ 必须可整除；
- 卷积通道排序决定哪些 features 共享统计量，分组本身是一种归纳偏置。
