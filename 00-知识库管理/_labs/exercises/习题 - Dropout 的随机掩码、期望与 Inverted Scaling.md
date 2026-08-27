---
type: exercise
status: draft
area: [neural-networks/regularization, dropout, bernoulli-noise, train-eval]
topic: "[[Dropout 的随机掩码、期望与 Inverted Scaling]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Dropout 的随机掩码、期望与 Inverted Scaling]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Dropout 的随机掩码、期望与 Inverted Scaling

## A

### NN-DRO-A01
定义 drop probability $p$、keep probability $q$ 与 Bernoulli mask $M$。分别写出 inverted Dropout 在 train/eval 模式的算子，并说明“均值保持”条件于什么。

### NN-DRO-A02
区分 element、channel、token、sample 与 path mask；对 shape 为 $(B,T,D)$ 的张量分别给出一种可广播 mask shape，并说明各自共享了哪些轴。

### NN-DRO-A03
比较历史 test-time scaling 与现代 inverted scaling：随机性和缩放分别出现在哪一阶段？二者在线性层前为何能匹配同一个一阶矩？

## B

### NN-DRO-B01
令 $x=(2,-1,3)$、$q=0.5$，采到 $m=(1,0,1)$。计算 train-time 输出、每个坐标的条件均值、条件方差、条件二阶矩，以及 $\mathbb E|Y|_2^2$。

### NN-DRO-B02
上游梯度为 $g=(1,-2,4)$，沿用 B01 的 mask。求对输入的 VJP。若 Dropout 输入来自 $x=Wa$，写出对 $W$ 与 $a$ 的梯度表达式。

### NN-DRO-B03
取标量 $x=1,q=0.5$，令 $Y=Mx/q$，$f(y)=\operatorname{ReLU}(y-1)$。计算 $\mathbb E[f(Y)]$ 与 $f(\mathbb E Y)$，并指出该反例否定了什么、没有否定什么。

## C

### NN-DRO-C01
从 Bernoulli moments 出发，完整推导固定 $x_i$ 下 $Y_i=M_ix_i/q$ 的条件均值、方差与二阶矩。再说明 $q\to0$ 时哪一项发散。

### NN-DRO-C02
设 $A$ 为确定矩阵、$b$ 为确定向量。证明 $\mathbb E[A Y+b\mid x]=Ax+b$；再给出一般非线性 $f$ 下不能交换 $\mathbb E$ 与 $f$ 的理由。

### NN-DRO-C03
设同一 mask 在多个坐标间共享。推导 $\operatorname{Cov}(Y_i,Y_j\mid x)$；与独立 element masks 比较，并解释为什么相同边际方差不决定联合随机函数。

## D

### NN-DRO-D01
审计命题：“只要用了 inverted scaling，Dropout 网络在 evaluation 的输出就等于所有随机子网络输出的精确平均。”给出成立条件、反例和可接受的较弱表述。

### NN-DRO-D02
分析 Dropout 与 BatchNorm/LayerNorm 的顺序。分别讨论 `Dropout → BatchNorm`、`BatchNorm → Dropout` 与 `LayerNorm → Dropout` 的 train/eval 统计和状态风险。

### NN-DRO-D03
解释 activation checkpointing、gradient accumulation 与 data parallel 下 RNG 合同为何是 correctness 问题。至少给出三个必须记录或测试的不变量。

## E

### NN-DRO-E01
设计一个 property-test suite，验证自写 inverted Dropout 的 shape、broadcast、mean、variance、backward、eval identity 与 seeded reproducibility。

### NN-DRO-E02
设计 element/channel/token 三种 mask granularity 的公平实验。规定 matched hyperparameters、随机性、指标与结论边界。

### NN-DRO-E03
阅读一段声称“Dropout 保持网络输出期望且无需模型集成”的实现说明时，写出逐层 claim audit：哪些对象可精确证明，哪些需 Monte Carlo，哪些必须用 held-out experiment。

## 解答入口

[[解答 - Dropout 的随机掩码、期望与 Inverted Scaling]]
