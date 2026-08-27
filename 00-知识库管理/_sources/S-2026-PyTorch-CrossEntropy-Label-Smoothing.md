---
type: source
status: draft
area: [sources, neural-networks, pytorch, cross-entropy, label-smoothing]
source_type: official-docs
title: "PyTorch CrossEntropyLoss"
author: "PyTorch Contributors"
year: 2026
url: "https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html"
accessed: 2026-08-24
source_tier: B
license: "PyTorch official documentation；本库仅保存版本化接口摘要与链接"
scope_role: implementation-contract
temporal_role: current-api
related: ["[[Label Smoothing、置信度与目标偏置]]", "[[Softmax 输出层、Logit 尺度与概率参数化]]"]
created: 2026-08-24
updated: 2026-08-24
---

# PyTorch：CrossEntropyLoss 与 Label Smoothing 当前接口

> [!abstract] 来源定位
> 当前文档说明 `label_smoothing` 把原 target 与 uniform distribution 混合，并区分 class-index target 与 probability target、`weight`、`ignore_index` 和 reduction。它只承担版本化 API 事实；统计目标、校准与泛化解释由正式推导和实验承担。

## 实现边界

- `label_smoothing` 的参数是 smoothing amount，不是保留 hard-label 的权重；
- probability targets 需与 logits 同 shape，调用者负责概率合法性；
- class weight、ignore mask 与 mean reduction 会改变有效目标和分母，必须用小张量对齐；
- 多标签 BCE 不是 multiclass softmax CE，不能直接复制同一公式。
