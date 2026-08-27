---
type: source
status: verified
area: [sources, ai-frameworks, numerical-analysis]
source_type: official-documentation
title: "Numerical accuracy"
author: PyTorch
year: 2026
url: "https://docs.pytorch.org/docs/stable/notes/numerical_accuracy.html"
accessed: 2026-08-15
source_tier: B
license: "PyTorch 官方文档；知识库仅保存独立摘要、版本事实与链接"
scope_role: implementation
temporal_role: current
aliases: [PyTorch-2026-Numerical-Accuracy]
related: ["[[浮点数与舍入误差]]", "[[矩阵扰动]]", "[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
created: 2026-08-15
updated: 2026-08-15
---

# PyTorch：Numerical accuracy

> [!abstract] 来源定位
> 当前 PyTorch 数值精度说明。它明确指出浮点加乘不结合，批量与切片计算、CPU/GPU、版本和平台之间不保证逐比特相同，并记录 TF32 与线性代数病态输入的接口边界。

## 本章调用

| 官方说明 | 教学映射 |
|---|---|
| 加法/乘法不结合 | 并行归约与括号依赖 |
| batch 与 slice 不保证逐比特相同 | kernel 选择也是运算图的一部分 |
| CPU/GPU/版本差异 | 逐比特、数值、任务复现分层 |
| TF32 只读取输入的 10 个 mantissa/fraction bits | storage dtype 不等于 multiply precision |
| `svd/eig/eigh` 对近重谱敏感 | 浮点误差还要乘问题条件性 |

## 使用纪律

- 只把该页用于 PyTorch 当前行为，不代替 IEEE 或 Higham 的数学定义；
- TF32 默认与 API 配置会随版本变化，引用时保留访问日期；
- “提高到 float64 often helps”不解释为“float64 保证正确”。

## 生成节点

- [x] [[浮点数与舍入误差]]
