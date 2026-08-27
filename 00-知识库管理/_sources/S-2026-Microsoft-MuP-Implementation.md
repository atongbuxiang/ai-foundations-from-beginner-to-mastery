---
type: source
status: verified
area: [sources, software, mup, pytorch]
source_type: implementation
title: "microsoft/mup: Maximal Update Parametrization and Hyperparameter Transfer"
author: [Microsoft Research Contributors]
year: 2026
url: "https://github.com/microsoft/mup"
accessed: 2026-08-26
source_tier: A
license: MIT
scope_role: implementation-authority
temporal_role: current-software
related: ["[[Tensor Programs、坐标检查与无限宽极限]]", "[[μTransfer、Base Shape 与超参数零样本迁移]]", "[[Embedding、Readout、Attention 与特殊参数组缩放]]"]
created: 2026-08-26
updated: 2026-08-26
---

# microsoft/mup 实现合同

> [!abstract] 来源定位
> 该仓库是 Tensor Programs V 配套的 PyTorch 实现来源。本卷用访问日 README 与代码语义说明 base/delta shape、`infshape`、`MuReadout`、`MuSGD`/`MuAdam`、attention scaling 和 coordinate check；易变实现事实均绑定 2026-08-26。

## 当前工作流

1. 建立同深度的 base model，并建立在所有拟扩展维度上不同的 delta model；
2. 由 base/delta shape 推断每个 tensor dimension 是 finite 还是 infinite；
3. 在重新初始化和创建 optimizer 前调用 `set_base_shapes`；
4. 使用 μP-aware initializer、optimizer 与 readout；
5. 对多个宽度、多个早期 step 做 coordinate check。

## 关键实现边界

- README 当前示例要求 target 与 base 深度相同；改变深度不在该 shape oracle 的自动保证内；
- hidden Adam learning rate 依 `fan_in/base_fan_in` 调整，custom tensor orientation 必须显式声明；
- Transformer 示例使用与标准 $1/\sqrt d$ 不同的 attention scaling，并保留 base-width 兼容常数；
- `infshape`、scheduler 相对缩放、checkpoint 恢复与 DataParallel 行为存在实现注意事项；
- coord check 只检查若干统计量的宽度趋势，是强诊断但不是正确性的形式证明。

