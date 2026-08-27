---
type: source
status: draft
area: [sources, architecture/rnn, memory]
source_type: paper
title: "Long Short-Term Memory"
author: "Sepp Hochreiter, Jürgen Schmidhuber"
year: 1997
url: "https://doi.org/10.1162/neco.1997.9.8.1735"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[LSTM 的记忆单元、门控与梯度通道]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Long Short-Term Memory

> [!abstract] 来源定位
> LSTM 的原始来源。现代框架常用 forget-gate 版本，与 1997 结构并不逐式相同；课程显式声明采用现代标准方程，并把原论文用于历史动机和恒定误差通道，而非声称门控能无条件解决任意长依赖。

## 课程采用的断言

- 通过独立 cell state 与门控加法更新，为梯度提供一条不同于纯 $\tanh$ 递推的路径；
- 现代 LSTM 的 $partial c_t/\partial c_{t-1}$ 直接项为 forget gate，但总 Jacobian 还含门值对前态的依赖；
- 门饱和、有限精度、截断 BPTT、优化和任务可识别性仍限制可学习记忆。

## 版本边界

正文不把“现代 forget/input/output gate 方程”倒签为 1997 论文原式。比较论文、教材与库实现时，先核对 peephole、bias、gate 顺序和 cell clipping。

