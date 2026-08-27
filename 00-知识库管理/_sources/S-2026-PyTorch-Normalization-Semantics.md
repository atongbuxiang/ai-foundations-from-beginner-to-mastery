---
type: source
status: draft
area: [sources, neural-networks/normalization, implementation]
source_type: documentation
title: "PyTorch BatchNorm2d and LayerNorm API Semantics"
author: "PyTorch Contributors"
year: 2026
url: "https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html"
accessed: 2026-08-23
source_tier: A
license: "PyTorch documentation license；本库仅保存独立语义摘要与链接"
scope_role: core
temporal_role: implementation-aged
related: ["[[归一化的对象、轴与不变性]]", "[[BatchNorm 前向统计与训练—推理差异]]", "[[LayerNorm 的逐样本几何与反向传播]]", "[[小批量、混合精度、分布式与因果归一化边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# PyTorch：BatchNorm 与 LayerNorm 实现语义

> [!abstract] 来源定位
> 原论文给方法，框架文档给可执行合同。本卡记录访问日 PyTorch 2.13 文档中 reduction axes、variance estimator、running buffers、momentum、affine 参数形状和 train/eval 语义；这些细节属于版本化实现事实，后续升级框架时必须重查，不能当作所有库的数学定义。

## 原始入口

- [BatchNorm2d 文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html)；
- [LayerNorm 文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html)；
- 访问时稳定页重定向到 PyTorch 2.13。

## BatchNorm2d 合同

对输入 $(N,C,H,W)$：

| 对象 | PyTorch 2.13 语义 |
|---|---|
| 统计归约 | 对每个 channel，在 $(N,H,W)$ 上归约 |
| forward variance | biased estimator，等价于 `correction=0` |
| running variance update 的当前观测 | unbiased estimator，等价于 `correction=1` |
| affine 参数 | $\gamma,\beta\in\mathbb R^C$，默认分别为 1 与 0 |
| running state | 默认训练期更新，evaluation 使用 |
| `momentum` | $s_{new}=(1-m)s_{old}+m s_t$，不是 optimizer momentum |
| `momentum=None` | cumulative moving average |
| `track_running_stats=False` | train 与 eval 都使用当前 batch statistics |

最容易错的是：训练 forward 的 denominator 与写入 `running_var` 的当前 variance observation 在 estimator 上不同。手工复现若只对比一个 buffer，必须同时声明 `correction`。

## LayerNorm 合同

对 `normalized_shape` 含 $D$ 个尾维：

| 对象 | PyTorch 2.13 语义 |
|---|---|
| 统计归约 | 输入的最后 $D$ 个维度 |
| variance | biased estimator，`correction=0` |
| affine 参数 | 与 `normalized_shape` 同形的 per-element gain/bias |
| train/eval | 两种 mode 都使用当前 input statistics |
| running state | 无 |

若输入为 $(B,T,D)$ 且 `normalized_shape=D`，每个 token 独立归约 feature 轴；若错误传入 `(T,D)`，同一样本内 token 与 feature 会被联合归约，语义、梯度耦合和因果边界均改变。

## 版本与跨框架边界

- TensorFlow/JAX/自写 kernel 的 momentum 命名、epsilon 默认值、参数布局和 variance correction 可能不同；
- fused inference kernel 可能把 BN 折叠进 convolution/linear；
- autocast/accumulation dtype 不由数学公式自动决定；
- 本卡支撑“PyTorch 2.13 怎样做”，不支撑“所有 BatchNorm/LayerNorm 必须这样做”。

