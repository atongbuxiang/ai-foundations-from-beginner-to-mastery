---
type: source
status: active
area: [sources, neural-networks, pytorch, dropout, stochastic-depth]
source_type: official-docs
title: "PyTorch Dropout Functions and Torchvision Stochastic Depth"
author: "PyTorch Contributors"
year: 2026
url: "https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html"
secondary_url: "https://docs.pytorch.org/vision/main/generated/torchvision.ops.stochastic_depth.html"
accessed: 2026-08-29
source_tier: B
license: "PyTorch official documentation；本库仅保存独立接口摘要与链接"
scope_role: implementation-contract
temporal_role: current-api
related: ["[[Dropout 的随机掩码、期望与 Inverted Scaling]]", "[[Stochastic Depth、DropPath 与有效深度]]"]
created: 2026-08-24
updated: 2026-08-29
---

# PyTorch：Dropout 与 Stochastic-Depth 当前接口

> [!abstract] 来源定位
> 当前官方文档定义训练态 element dropout、channel-wise variants，以及 torchvision stochastic depth 的 drop probability、`batch`/`row` mask mode 和 training flag。它承担版本化 API 事实；概率推导、历史术语和泛化解释仍由论文与本库独立推导承担。

## 当前接口事实

- 标准 Dropout 在训练时随机置零并使用 inverted scaling，evaluation 时为 identity；
- 1d/2d/3d variants 可按 channel mask，而非逐 element；
- torchvision stochastic depth 的 `batch` 模式整批共享 gate，`row` 模式按 batch row 采 gate；
- `p` 表示 drop probability，不是 keep probability；
- train/eval、随机数流、编译与重算行为必须随版本/后端测试。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| PTD-C1 | 当前标准 Dropout eval 为 identity | API | 当前版本 | 版本内成立 |
| PTD-C2 | `Dropout2d` 与逐像素独立 mask 相同 | API 误读 | 它按 channel 置零 | 错误 |
| PTD-C3 | stochastic-depth `batch` 与 `row` 给相同 joint law | 结构 | gate 共享轴不同 | 错误 |
| PTD-C4 | 设置 `training=False` 仍继续随机采 mask | API | 当前实现 | 错误 |
