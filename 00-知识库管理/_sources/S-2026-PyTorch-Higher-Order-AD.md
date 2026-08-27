---
type: source
status: verified
area: [sources, software, automatic-differentiation, pytorch]
source_type: documentation
title: "PyTorch torch.func and Higher-Order Automatic Differentiation Documentation"
author: [PyTorch Contributors]
year: 2026
url: "https://docs.pytorch.org/docs/stable/func.api"
accessed: 2026-08-26
source_tier: A
scope_role: implementation-authority
temporal_role: current-documentation
related: ["[[Hessian-vector Product、共轭梯度与隐式二阶步]]", "[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]"]
created: 2026-08-26
updated: 2026-08-26
---

# PyTorch 当前高阶自动微分语义

> [!abstract] 来源定位
> 当前官方 API 负责 HVP/JVP/VJP 与 per-sample gradient 的实现语义，不承担优化收敛定理。`torch.func.hessian` 当前以 forward-over-reverse 为默认组合；HVP 可用 `jvp(grad(f))`，forward-mode coverage 不足时可改 reverse-over-reverse。

## 审计字段

- 标量 loss、参数 pytree 与 tangent shape；
- `functional_call` 下 parameters/buffers 的显式状态；
- forward/reverse 组合、graph retention、operator coverage 与 batch/vmap；
- per-sample gradients 是否真按样本保留，而非 batch-mean gradient outer product；
- HVP 精度、symmetry bilinear test、finite-difference residual 与重复 matvec 成本；
- PyTorch 版本、compile/fusion、dtype 和 randomness policy。

API 仍可能演进，跨版本复现应保存一步 reference output，而不是只保存函数名。
