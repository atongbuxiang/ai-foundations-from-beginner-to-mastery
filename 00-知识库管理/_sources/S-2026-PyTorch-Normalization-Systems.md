---
type: source
status: active
area: [sources, neural-networks/normalization, implementation, distributed, mixed-precision]
source_type: documentation
title: "PyTorch normalization families, SyncBatchNorm and AMP semantics"
author: "PyTorch Contributors"
year: 2026
url: "https://docs.pytorch.org/docs/stable/generated/torch.nn.SyncBatchNorm.html"
accessed: 2026-08-23
source_tier: A
license: "PyTorch documentation license；本库仅保存独立语义摘要与链接"
scope_role: core
temporal_role: implementation-aged
related: ["[[RMSNorm、均值移除与缩放不变性]]", "[[InstanceNorm、GroupNorm 与 WeightNorm]]", "[[小批量、混合精度、分布式与因果归一化边界]]"]
created: 2026-08-23
updated: 2026-08-29
---

# PyTorch：归一化谱系、同步统计与混合精度语义

> [!abstract] 来源定位
> 本卡记录访问日 PyTorch 2.13 的 RMSNorm、InstanceNorm2d、GroupNorm、WeightNorm parametrization、SyncBatchNorm 与 AMP 合同。它只约束该版本 API，不替代数学定义，也不保证其他框架、自定义 fused kernel 或未来版本相同。

## 官方页面

- [RMSNorm](https://docs.pytorch.org/docs/main/generated/torch.nn.modules.normalization.RMSNorm.html)
- [InstanceNorm2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.modules.instancenorm.InstanceNorm2d.html)
- [GroupNorm](https://docs.pytorch.org/docs/stable/generated/torch.nn.GroupNorm.html)
- [WeightNorm parametrization](https://docs.pytorch.org/docs/stable/generated/torch.nn.utils.parametrizations.weight_norm.html)
- [SyncBatchNorm](https://docs.pytorch.org/docs/stable/generated/torch.nn.SyncBatchNorm.html)
- [Automatic Mixed Precision](https://docs.pytorch.org/docs/stable/amp.html)

## 访问日语义表

| 对象 | PyTorch 2.13 语义 | 不能省略的边界 |
|---|---|---|
| RMSNorm | 归约 normalized shape 的尾维；per-element gain；无 bias | `eps=None` 取 opmath dtype 的 machine epsilon |
| GroupNorm | 每样本、每组归约；biased variance；per-channel affine | train/eval 都用当前输入统计 |
| InstanceNorm2d | 每样本、每 channel 归约空间轴；biased variance | 默认 `affine=False, track_running_stats=False`；可改成有 state |
| WeightNorm | $w=g v/\|v\|$ parametrization | 默认 `dim=0` 按 output channel/plane；不是 activation norm |
| SyncBatchNorm | process group 内训练 batch statistics 同步 | eval 不同步；当前文档限制 DDP 单 GPU/进程 |
| AMP | 按 op 选择 fp16/bf16/fp32；CUDA group/layer norm 在 fp32 列表 | custom/fused op 与其他设备策略需单独检查 |

## 关键实现警告

1. RMSNorm 默认 epsilon 与 LayerNorm 常见默认值不同，不能省略显式配置后比较；
2. GroupNorm 的 $G=1/C$ 只保证统计核心与 LN/IN 极端情形对应，affine/state 合同仍可能不同；
3. SyncBatchNorm 改变统计组、通信与反向耦合，不是“只同步 buffers”；
4. loss scaling 只缩放 backward 信号，不能修复 forward statistic 的 overflow/cancellation；
5. autocast 列表是版本与设备相关的 dispatcher 语义，自定义 kernel 必须检查 accumulation dtype。
