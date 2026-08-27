---
type: source
status: verified
area: [sources, optimization, large-batch, scale-diagnostics]
source_type: paper
title: "Large Batch Training of Convolutional Networks"
author: "You, Gitman, and Ginsburg"
year: 2017
url: "https://arxiv.org/abs/1708.03888"
accessed: 2026-08-26
source_tier: A
scope_role: original-method
related: ["[[Update-to-Weight Ratio、谱与尺度诊断]]"]
created: 2026-08-26
updated: 2026-08-26
---

# You 等：LARS 与层级信任比

> [!abstract] 来源定位
> LARS 以 layer weight norm 与 gradient norm 的比值调节局部学习率，是 update-to-weight 诊断和 layerwise adaptation 的历史主线之一。

## 本卷调用

- 区分 raw gradient-to-weight、optimizer update-to-weight 与实际参数位移；
- 将 trust ratio 的 epsilon、weight decay、excluded parameter group 写入 exact update；
- 用 layerwise ratio 发现单个 global norm 隐藏的尺度不平衡。

## 边界

LARS 的 ImageNet 大批量证据不推出所有架构都应维持同一比率；参数重缩放、normalization 和 bias 会改变 raw ratio 的解释。
