---
type: source
status: verified
area: [sources, ai-frameworks, mixed-precision]
source_type: official-documentation
title: "Automatic Mixed Precision package — torch.amp"
author: PyTorch
year: 2026
url: "https://docs.pytorch.org/docs/stable/amp.html"
accessed: 2026-08-26
source_tier: B
license: "PyTorch 官方文档；知识库仅保存版本行为、独立摘要与链接"
scope_role: implementation
temporal_role: current
related: ["[[Loss Scaling、Master Weight 与低精度梯度累积]]", "[[数据并行、All-Reduce 与全局 Batch 语义]]"]
created: 2026-08-26
updated: 2026-08-26
---

# PyTorch：Automatic Mixed Precision

> [!abstract] 来源定位
> 当前 AMP 实现合同：autocast 按算子选择执行 dtype；GradScaler 放大、反缩放、检查非有限梯度，并可能跳过 optimizer step。它用于核对代码时钟，不替代混合精度原理来源。

## 本卷调用

- 梯度裁剪/检查前应先 unscale，否则阈值和 telemetry 都在错误单位；
- 非有限梯度可使 `scaler.step(optimizer)` 跳过真正的 optimizer update；
- scheduler、EMA、global-step、moment state 是否同时推进必须由训练循环明确；
- autocast policy 是算子级而非“模型统一 dtype”。

## 边界

- API、默认 scale 和 allowlist 会随版本变化；
- GradScaler 不保证 scale 始终大于 1，也不保证所有模型收敛；
- distributed accumulation/no_sync 的等价性需另查 DDP 合同。
