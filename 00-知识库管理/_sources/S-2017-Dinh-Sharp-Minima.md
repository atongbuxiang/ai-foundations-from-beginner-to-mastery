---
type: source
status: verified
area: [sources, sharpness, flat-minima, reparameterization]
source_type: paper
title: "Sharp Minima Can Generalize for Deep Nets"
author: [Laurent Dinh, Razvan Pascanu, Samy Bengio, Yoshua Bengio]
year: 2017
url: "https://proceedings.mlr.press/v70/dinh17b.html"
accessed: 2026-08-23
source_tier: A
license: "Open PMLR article; retain citation"
venue: "ICML 2017"
scope_role: primary
temporal_role: modern-critique
related: ["[[范数、平坦性、Sharpness 与参数化不变性]]"]
created: 2026-08-23
updated: 2026-08-26
---
# Sharp Minima Can Generalize for Deep Nets
> [!abstract] 来源定位
> 用 ReLU 网络的 function-preserving symmetries 展示 raw flatness/sharpness 的参数化依赖。本库调用等价函数可任意 sharpen 的反例；不据此否定全部 normalized/function-space measures。
## 本库调用
1. ReLU rescaling symmetry；
2. parameter equivalence class；
3. sharpness non-invariance；
4. function vs parameter geometry；
5. flatness claim audit。

## 已核对断言与边界

- 论文针对带 rectifier 的网络利用参数对称性构造函数等价而局部几何显著不同的参数化；因此 raw parameter-space sharpness 不能脱离坐标直接解释泛化；
- 反例否定的是缺少不变性控制的 flatness 概念，不是否定所有归一化、函数空间或扰动分布绑定的 sharpness 指标；
- 本章只在 [[Critical Batch、隐式偏置与 SGD 证据地图]] 中把它用作“单一 sharpness 数值不足以确认机制”的反例，不由此推出 SGD、batch size 或泛化的一般排序。

核对入口：[PMLR 论文页](https://proceedings.mlr.press/v70/dinh17b.html)；访问日 2026-08-26。
