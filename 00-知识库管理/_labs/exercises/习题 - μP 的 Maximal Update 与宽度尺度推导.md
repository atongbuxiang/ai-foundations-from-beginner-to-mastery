---
type: exercise
status: verified
area: [training, optimization, parameterization, mup]
topic: "[[μP 的 Maximal Update 与宽度尺度推导]]"
solution: "[[解答 - μP 的 Maximal Update 与宽度尺度推导]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - μP 的 Maximal Update 与宽度尺度推导

> [!abstract] 训练目标
> 能从随机初始化的 $\sqrt n$ 累积与训练更新的 $n$ 对齐累积，独立推导 input、hidden、readout 在 SGD/Adam 下的 width exponent。

## A. 识别与复述

### TRN43-A01
解释 maximal update 中“maximal”的准确语义。它为什么不等于最大 raw LR 或每个参数坐标 $O(1)$ 更新？

### TRN43-A02
比较 Gaussian-like random sum 与 gradient-induced coherent sum。何时应使用 $\sqrt n$，何时可能出现 $n$？

### TRN43-A03
复述 μP 表中 input、hidden、output 三类参数的 init variance、SGD LR 与 Adam LR 的 width 量级，并写明表依赖的约定。

## B. 手算与构造

### TRN43-B01
令 $x_i=1$，$\delta=2$，$\Delta W_i=-\gamma_nx_i\delta$。对 $n=100$，分别取 $\gamma_n=1/\sqrt n,1/n,1/n^2$，计算 $\Delta y=\sum_ix_i\Delta W_i$，判断爆炸、非退化或消失趋势。

### TRN43-B02
三层 MLP 中 $d_{out}$ 固定、$W^3_{jk}=O(1/n)$、$\delta^3=O(1)$。求 $\delta^2_j$、$\nabla W^2_{ij}$ 的量级；分别给 SGD 与 Adam 产生 $\Delta W^2=O(1/n)$ 所需 LR。

### TRN43-B03
取 $n=1024$、base width $n_0=256$、base Adam LR $\eta_0=2\times10^{-3}$。按 hidden/readout 的 $1/\mathrm{fan\_in}$ ratio 与 input 的 width-invariant Adam 规则，计算三组 target LR；说明这不是把 global LR 统一除以 4。

## C. 推导与证明

### TRN43-C01
从 $W^3$ 的 $1/n$ 初始化开始，完整推导 $\delta^2=O(1/n)$、$\nabla W^2=O(1/n)$、$\delta^1=O(1/n)$ 与 $\nabla W^1=O(1/n)$。逐步标注哪些和使用随机抵消。

### TRN43-C02
在一般 exponent ledger 中，init entry 为 $n^{-a}$、forward multiplier 为 $n^{-p}$、actual update entry 为 $n^{-u}$。推导随机初始输出与对齐 feature update 的 exponent，并给出同时 $O(1)$ 的条件。

### TRN43-C03
假设 Adam direction 在 $\epsilon$ 不主导时为 $O(1)$。解释为何 hidden gradient 的 $1/n$ 被归一化后必须由 LR 补回；再给出 $\epsilon$ 主导时该推导失效的公式。

## D. 边界、反例与纠错

### TRN43-D01
反驳：“所有 μP 参数组的 LR 都应随 width 变小。”至少用 input SGD 与 hidden SGD 两个反例。

### TRN43-D02
构造 entry RMS 为 $1/n$、但与输入不对齐的随机更新；比较其 feature update 与外积对齐更新，说明只报 entry scale 不够。

### TRN43-D03
为什么 readout 初始化 logit 随 width 趋零不等于模型退化？在什么情况下它才是真正的失败？

## E. AI 迁移

### TRN43-E01
给一个含 input projection、两个 hidden matrices、readout 的 MLP 写 exponent ledger：init、raw grad、optimizer direction、group LR、actual update、feature update。

### TRN43-E02
设计一个一至八步的 μP 调试实验，用于区分 init bug、LR-group bug、Adam-$\epsilon$ bug 与 feature-update 聚合 bug。

### TRN43-E03
把博客或论文中的 μP 规则迁移到一个转置存储的自定义 Linear 层时，应完成哪些 shape、梯度和数值检查？

## 作答与复盘

先不看表，从三层 MLP 反向推导一次，再查看 [[解答 - μP 的 Maximal Update 与宽度尺度推导]]。如果推导中把训练更新按独立随机项相加，必须标记为关键错误。
