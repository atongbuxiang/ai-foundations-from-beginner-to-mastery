---
type: source
status: verified
area: [sources, software, pytorch, muon]
source_type: documentation
title: "PyTorch torch.optim.Muon Documentation and Source"
author: [PyTorch Contributors]
year: 2026
url: "https://docs.pytorch.org/docs/stable/generated/torch.optim.Muon.html"
code: "https://github.com/pytorch/pytorch/blob/main/torch/optim/_muon.py"
accessed: 2026-08-26
source_tier: A
scope_role: implementation-authority
temporal_role: current-documentation
related: ["[[Muon 的动量、正交化与参数分组合同]]", "[[Muon 形状缩放、Update RMS 与版本差异]]", "[[Newton–Schulz Matrix Sign 的收敛与有限精度]]"]
---

# S-2026 PyTorch - Muon

## 当前接口（访问日）

- 只接收二维参数；默认 momentum `.95`、Nesterov、5 步 NS 与 Jordan 系数；
- 当前源码用 `buf.lerp_(grad, 1-momentum)` 形成 EMA-style buffer，再按 Nesterov 组合；
- 提供 `original`、`match_rms_adamw`、`spectral_unclamped` 三种 LR shape adjustment；
- decoupled weight decay 先按 base LR 缩放参数，update 再按 adjusted LR 应用；complex/foreach 当前不支持。

## 采用边界

接口和源码是易变软件事实，必须带访问日期/版本。未合并 PR、第三方实现或旧 Keller 代码不能静默视作同一 transition。
