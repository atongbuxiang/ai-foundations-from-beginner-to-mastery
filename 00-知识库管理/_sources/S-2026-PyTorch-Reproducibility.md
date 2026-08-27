---
type: source
status: verified
area: [sources, ai-frameworks, reproducibility]
source_type: official-documentation
title: "Reproducibility"
author: PyTorch
year: 2026
url: "https://docs.pytorch.org/docs/stable/notes/randomness.html"
accessed: 2026-08-26
source_tier: B
license: "PyTorch 官方文档；知识库仅保存版本行为、独立摘要与链接"
scope_role: implementation
temporal_role: current
related: ["[[通信 Roofline、非确定性与分布式训练证据地图]]", "[[随机舍入、无偏性与微小更新保留]]", "[[随机种子、配对比较、置信区间与序贯决策]]", "[[训练实验协议、事故记录与因果证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# PyTorch：Reproducibility

> [!abstract] 来源定位
> 当前框架对随机源、确定性算法和跨平台边界的官方说明。它明确不保证跨 release、commit、platform 或 CPU/GPU 的完全复现。

## 本卷调用

- 固定 Python/框架/device RNG 只处理显式随机性的一部分；
- `torch.use_deterministic_algorithms` 可选择确定性实现或在无实现时抛错；
- deterministic kernel 常有性能代价；
- fused attention 等 backend 的 forward/backward 确定性可能不同，低精度 backend 也不保证 bitwise matching。

## 边界

- 同 seed 不等于同数据顺序、collective 顺序、kernel 或环境；
- bitwise reproducibility、数值容差复现与统计/任务结论复现须分层；
- 当前 backend 表格绑定访问日期和版本。
