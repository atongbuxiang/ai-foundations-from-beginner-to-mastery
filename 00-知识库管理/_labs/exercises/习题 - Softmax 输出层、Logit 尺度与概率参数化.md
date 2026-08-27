---
type: exercise
status: draft
area: [neural-networks/embedding-output, softmax, categorical-output]
topic: "[[Softmax 输出层、Logit 尺度与概率参数化]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Softmax 输出层、Logit 尺度与概率参数化]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Softmax 输出层、Logit 尺度与概率参数化

## A

### NN-SOP-A01
设 hidden shape 为 $[B,T,d_h]$、词表大小为 $V$。写出权重、bias、logits 与 probabilities 的 shape，并说明 softmax 归一化轴。

### NN-SOP-A02
解释 softmax 的 shift gauge：什么量不可辨识，什么量可辨识？给出两种固定 gauge 的方式。

### NN-SOP-A03
为什么有限 logits 只能表示概率单纯形的内部？若某类概率必须精确为零，工程上常用什么合同表达？

## B

### NN-SOP-B01
对 $z=(2,1,0)$ 计算 $\tau=1$ 与 $\tau=2$ 的 softmax 概率（保留五位小数），并比较 argmax 与熵的变化。

### NN-SOP-B02
概率 $p=(0.5,0.3,0.2)$。求满足 $\sum_i z_i=0$ 的一组 logits，并验证任意加常数都给出同一概率。

### NN-SOP-B03
对 $z=(1001,1000,999)$，说明朴素 exponentiation 的风险，并用减最大值计算稳定 softmax；结果应与 $(2,1,0)$ 相同。

## C

### NN-SOP-C01
证明 $\operatorname{softmax}(z+c\mathbf1)=\operatorname{softmax}(z)$，并证明
$$
\log\frac{p_i}{p_j}=z_i-z_j.
$$

### NN-SOP-C02
对 $p_i(\tau)=\exp(z_i/\tau)/\sum_j\exp(z_j/\tau)$，推导 one-hot cross-entropy 对 $z$ 的梯度与 Hessian。

### NN-SOP-C03
证明 softmax entropy 满足
$$
\frac{dH}{d\tau}=\frac{\operatorname{Var}_{p(\tau)}(z)}{\tau^3}\ge0.
$$
何时等号成立？

## D

### NN-SOP-D01
某实现先算 probabilities、再取 `log` 计算交叉熵。解释它为何可能产生 underflow、`log(0)` 或不必要的中间误差；给出 fused log-sum-exp 形式。

### NN-SOP-D02
对序列模型，分别说明 padding mask、causal mask 与词表禁用 mask 应在何处施加。为什么把某 logit 设为有限大负数不等于数学上的精确零概率？

### NN-SOP-D03
模型降低 temperature 后 accuracy 不变、NLL 变差、ECE 也变差。解释这组结果为何不矛盾，并说明 temperature 应在哪个数据 split 上拟合。

## E

### NN-SOP-E01
设计检验 logit 尺度的实验：在固定分类边界下扫描 scale，报告 accuracy、NLL、entropy、ECE、梯度范数与溢出率。写出你预期的非单调或不变关系。

### NN-SOP-E02
反驳：“Softmax 能表示任意 categorical distribution，所以线性 softmax head 没有表达瓶颈。”区分单个上下文的自由 logits 与跨上下文共享仿射参数族。

### NN-SOP-E03
在 $V=10^6$ 的输出任务中，设计 full softmax 的系统基线与验收账本。至少覆盖 logits 计算、归一化通信、激活显存、精确 NLL、近似方案偏差与校准。
