---
type: source
status: draft
area: [sources, neural-networks, pytorch, adaptive-softmax, cross-entropy]
source_type: official-docs
title: "PyTorch AdaptiveLogSoftmaxWithLoss and CrossEntropyLoss"
author: "PyTorch Contributors"
year: 2026
url: "https://docs.pytorch.org/docs/stable/generated/torch.nn.AdaptiveLogSoftmaxWithLoss.html"
secondary_url: "https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html"
accessed: 2026-08-24
source_tier: B
license: "PyTorch official documentation；本库仅保存独立摘要、接口事实与链接"
scope_role: implementation-contract
temporal_role: current-api
related: ["[[Sampled、Hierarchical 与 Adaptive Softmax]]", "[[Padding、Mask、特殊符号与词表边界]]"]
created: 2026-08-24
updated: 2026-08-24
---

# PyTorch：大词表损失与 Ignore-Index 合同

> [!abstract] 来源定位
> 当前官方文档给出 `AdaptiveLogSoftmaxWithLoss` 的 cutoffs、frequency ordering、tail dimension 和 full `log_prob` 接口，以及 `CrossEntropyLoss(ignore_index=...)` 的 loss/gradient/reduction 语义。它承担版本化实现事实；概率分解、偏差与复杂度由原论文和本库推导承担。

## 当前接口事实

- adaptive targets 需要按频率排序，高频类使用较小 ID；
- `cutoffs` 定义 head/tail buckets，`div_value` 控制更深 tail 的表示维度；
-训练返回目标 log probability/loss，`log_prob` 可计算所有 classes；
- class-index target 的 `ignore_index` 不贡献输入梯度，mean reduction 的分母只计 non-ignored targets；
- 以上支持范围和默认值必须随框架版本复核。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| PTL-C1 | adaptive class IDs 的频率顺序属于 API 前置条件 | API | 当前版本 | 版本内成立 |
| PTL-C2 | `ignore_index` 等于 attention padding mask | 对象混淆 | 一个作用 loss target，一个作用 attention edge | 错误 |
| PTL-C3 | mean reduction 自动除以原矩形张量元素总数 | API 误读 | ignored target 不进分母 | 错误 |
| PTL-C4 | `log_prob` 可返回全类 log probabilities | API | 当前版本 | 版本内成立 |
