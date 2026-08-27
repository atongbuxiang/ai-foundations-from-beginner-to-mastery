---
type: exercise
status: draft
area: [neural-networks/initialization, kaiming, rectifiers]
topic: "[[Kaiming、He 初始化]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Kaiming、He 初始化]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Kaiming、He 初始化

## A

### NN-HEI-A01
写出 ReLU/Leaky ReLU 的 forward second-moment factor 与 derivative second-moment factor。

### NN-HEI-A02
写出 Kaiming normal/uniform 在 slope $a$、fan mode 下的参数。

### NN-HEI-A03
区分 activation variance、activation second moment 与 positive rate。

## B

### NN-HEI-B01
对 fan-in 256、$a=0.1$，计算 Kaiming normal std 与 uniform bound。

### NN-HEI-B02
对 $W:[64,256,3,3]$ 的普通 convolution，计算两个 fan 与 ReLU fan-in/fan-out variance。

### NN-HEI-B03
计算 $Z\sim\mathcal N(0,q)$ 时 ReLU 的 mean、second moment 与 variance。

## C

### NN-HEI-C01
证明 Leaky ReLU 的 factor 是 $(1+a^2)/2$，并推导 gain。

### NN-HEI-C02
证明 symmetric continuous input 下 rectifier 的 forward factor 与 derivative factor 相同。

### NN-HEI-C03
若 PReLU 从 $a_0$ 训练到 $a_t$，推导二阶增益偏离比。

## D

### NN-HEI-D01
反驳“Kaiming 初始化保证每层 activation variance 不变”。

### NN-HEI-D02
构造 bias 或非对称输入使半轴二分假设失效。

### NN-HEI-D03
解释 truncation、clipping 与低精度 cast 如何破坏 nominal variance。

## E

### NN-HEI-E01
设计 dense/conv/grouped-conv 的 fan 与 moment 单元测试。

### NN-HEI-E02
设计 Xavier 与 Kaiming 在深 ReLU MLP 上的 matched-seed 诊断。

### NN-HEI-E03
为可学习 PReLU 网络设计初始化—训练尺度漂移监测。

## 解答入口

[[解答 - Kaiming、He 初始化]]

