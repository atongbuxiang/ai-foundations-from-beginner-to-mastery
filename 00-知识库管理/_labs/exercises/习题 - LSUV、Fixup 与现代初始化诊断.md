---
type: exercise
status: draft
area: [neural-networks/initialization, lsuv, fixup, diagnostics]
topic: "[[LSUV、Fixup 与现代初始化诊断]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - LSUV、Fixup 与现代初始化诊断]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - LSUV、Fixup 与现代初始化诊断

## A

### NN-DIAG-A01
写出 LSUV 的两阶段算法、当前层重缩放公式与停止条件。

### NN-DIAG-A02
写出 Fixup 的三条完整规则，并定义 $L,m$。

### NN-DIAG-A03
列出初始化诊断仪表盘的 parameter、forward、correlation、backward、spectrum、update/system 六层对象。

## B

### NN-DIAG-B01
某层 LSUV 测得 variance 4，重缩放一次后又测得 1.21。忽略 $\varepsilon$，求两次权重乘数与累计乘数。

### NN-DIAG-B02
Fixup 网络有 $L=64$ 个 branches、每 branch $m=3$ 个 weight layers。求每个非零 branch weight 的额外 amplitude scale，以及两个非零 weights 的 product scale。

### NN-DIAG-B03
三层参数 norm 分别为 $(10,1,0)$，update norm 为 $(0.1,0.02,0.003)$。取 $\epsilon=10^{-3}$，计算各层 update ratio 并解释 zero-initialized layer 的 denominator 语义。

## C

### NN-DIAG-C01
在局部 positive-homogeneous 假设下，证明 $W\leftarrow W/\sqrt v$ 会把输出 variance 从 $v$ 变为约 1，并指出证明断点。

### NN-DIAG-C02
推导 $\left(L^{-1/(2m-2)}\right)^{m-1}=L^{-1/2}$，解释它如何对应 $L$ 个近不相关 branch contributions。

### NN-DIAG-C03
说明 Fixup zero-last-layer 下不同 branch layers 的 step-0 学习顺序，并与全零串行 MLP 比较。

## D

### NN-DIAG-D01
反驳：“LSUV 把每层 variance 校准为 1，因此等价于训练时 BatchNorm。”

### NN-DIAG-D02
反驳：“Fixup 只需要把每个 residual branch 最后一层置零。”

### NN-DIAG-D03
构造 forward variance 正常、但 update ratio 或 singular extremes 异常的初始化诊断反例。

## E

### NN-DIAG-E01
设计 LSUV 对 calibration batch、axes、mode 与 tolerance 的 sensitivity audit。

### NN-DIAG-E02
设计 Fixup 三条规则的 ablation，规定 matched optimizer、depth、seed 与结论边界。

### NN-DIAG-E03
写一份“定位第一处失效”的执行协议，从参数到系统层规定记录项与局部修正原则。

## 解答入口

[[解答 - LSUV、Fixup 与现代初始化诊断]]
