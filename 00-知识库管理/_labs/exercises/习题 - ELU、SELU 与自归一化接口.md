---
type: exercise
status: draft
area: [neural-networks/activations, elu, selu, self-normalization]
topic: "[[ELU、SELU 与自归一化接口]]"
difficulty: [A, B, C, D, E]
related: ["[[解答 - ELU、SELU 与自归一化接口]]", "[[方差传播与宽层均值场近似]]"]
solution: "[[解答 - ELU、SELU 与自归一化接口]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - ELU、SELU 与自归一化接口

## A. 识别与复述

### NN-SELU-A01
比较 ReLU、leaky ReLU、ELU 的负侧极限、导数、齐次性与稀疏性。

### NN-SELU-A02
判断 ELU 在 0 处何时连续、$C^1$、$C^2$；再判断经典 SELU 的可微性。

### NN-SELU-A03
精确定义 SELU self-normalization 的 moment-map fixed-point claim，并说明它不等于 BatchNorm。

## B. 手算与建模

### NN-SELU-B01
取 $\alpha=1$，计算 ELU 在 $x=-20,-1,0,2$ 的 output 与两侧 derivative，并指出有限精度风险。

### NN-SELU-B02
令 $X$ 均值 0、方差 1，alpha-dropout 保留率 $q=0.9$、drop value $c=-\lambda\alpha$。推导 affine correction $a,b$。

### NN-SELU-B03
用 $E[e^{tZ}\mathbf1_{Z\le0}]=e^{t^2/2}\Phi(-t)$ 写出标准正态经 SELU 后的均值和二阶矩方程。

## C. 推导与证明

### NN-SELU-C01
证明 ELU 负侧用 `expm1` 与 $e^x-1$ 数学等价，并用 Taylor 说明其近零数值优势。

### NN-SELU-C02
从 $F(0,1)=(0,1)$ 推导 $\alpha,\lambda$ 的两个方程；说明为何 fixed point 本身不推出 attraction。

### NN-SELU-C03
给出从 local Jacobian spectral radius 到 contraction 仍缺少的条件，并用 Banach 定理组织完整证明义务。

## D. 边界、反例与纠错

### NN-SELU-D01
反驳：“使用 SELU 后每个 mini-batch、每一层都精确均值 0、方差 1。”

### NN-SELU-D02
解释 ordinary inverted dropout 为什么破坏 SELU moment map，并说明 alpha dropout 修复的对象。

### NN-SELU-D03
构造 residual addition 改变 variance map 的最小例子，说明 plain FNN theorem 不能机械套用。

## E. AI 迁移

### NN-SELU-E01
为 SELU plain MLP 设计 fixed-point perturbation 实验，并定义收缩证据与失败边界。

### NN-SELU-E02
审计“Transformer 把 GELU 换成 SELU 即可省掉 LayerNorm”的主张。

### NN-SELU-E03
为 FP16 ELU/SELU kernel 设计 `expm1`、负饱和、zero kink、gradient 与 wall-clock 验收。

## 解答入口

[[解答 - ELU、SELU 与自归一化接口]]
