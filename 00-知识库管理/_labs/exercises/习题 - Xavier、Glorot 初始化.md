---
type: exercise
status: draft
area: [neural-networks/initialization, xavier, glorot]
topic: "[[Xavier、Glorot 初始化]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Xavier、Glorot 初始化]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Xavier、Glorot 初始化

## A

### NN-XAV-A01
定义 fan-in、fan-out，并说明它们如何由 forward/VJP 求和方向得到。

### NN-XAV-A02
写出 Xavier normal 与 uniform 的 variance、standard deviation/bound。

### NN-XAV-A03
区分“Gram 的期望为 identity”“一次抽样近正交”“dynamical isometry”。

## B

### NN-XAV-B01
对 $W:[120,30]$ 的 $z=Wx$，计算 fan-in/fan-out、Xavier variance、uniform bound 与两条乘数。

### NN-XAV-B02
对权重存储为 $[30,120]$ 且 forward 用 $xW$ 的实现，说明如何避免框架把 fan 算反。

### NN-XAV-B03
比较同方差 Gaussian 与 uniform 在 fourth moment、tail 和最大绝对值上的差别。

## C

### NN-XAV-C01
从前向与反向二阶矩分别推导 $1/n_{\mathrm{in}}$、$1/n_{\mathrm{out}}$。

### NN-XAV-C02
证明 Xavier 是 effective fan 为算术平均时的 reciprocal scale，并计算 aspect ratio 极限。

### NN-XAV-C03
证明 square iid matrix 在 variance $1/n$ 时 $\mathbb E[WW^T]=I$，并说明为何这不控制所有奇异值。

## D

### NN-XAV-D01
反驳“Xavier 同时精确保持任意非方层的前向和反向 variance”。

### NN-XAV-D02
解释 Xavier 为何不能单独消除 sigmoid 饱和与均值漂移。

### NN-XAV-D03
审计把 embedding、depthwise convolution 和 residual branch 一律套 Xavier 的做法。

## E

### NN-XAV-E01
设计 Xavier initializer 的 distribution、shape、layout、dtype 与 determinism 验收。

### NN-XAV-E02
设计 fan-in、fan-out、Xavier 三轨的 aspect-ratio×depth 消融。

### NN-XAV-E03
给出初始化参数日志的最小 schema，使 checkpoint 可复现且能识别框架默认值。

## 解答入口

[[解答 - Xavier、Glorot 初始化]]

