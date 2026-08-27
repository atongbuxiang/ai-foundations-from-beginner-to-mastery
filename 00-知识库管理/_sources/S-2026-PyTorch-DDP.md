---
type: source
status: verified
area: [sources, ai-frameworks, distributed-training]
source_type: official-documentation
title: "DistributedDataParallel"
author: PyTorch
year: 2026
url: "https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html"
accessed: 2026-08-26
source_tier: B
license: "PyTorch 官方文档；知识库仅保存版本行为、独立摘要与链接"
scope_role: implementation
temporal_role: current
related: ["[[数据并行、All-Reduce 与全局 Batch 语义]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# PyTorch：DistributedDataParallel

> [!abstract] 来源定位
> 当前 DDP 的同步语义来源。DDP 复制模型、在 backward 中对梯度 bucket 做 collective，并假设各 rank 以相同 optimizer 语义更新；输入切分仍由用户/sampler 负责。

## 本卷调用

- DDP 默认 process group、gradient averaging 与 loss reduction 共同决定全局梯度尺度；
- bucket 可让通信与 backward 重叠，bucket size 因此是系统参数；
- uneven inputs、join 和 `divide_by_initial_world_size` 会改变样本权重；
- 参数不在每 step 广播，副本同步依赖相同初态与相同归约梯度。

## 边界

- 这是一份随版本变化的框架合同，不是抽象 All-Reduce 定理；
- 数学等价不保证低精度归约逐比特相同；
- `no_sync`、gradient accumulation、unused parameter 和自定义 hook 需逐项记录。
