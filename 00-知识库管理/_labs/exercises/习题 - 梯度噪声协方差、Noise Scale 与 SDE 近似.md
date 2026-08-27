---
type: exercise
status: verified
area: [training, optimization, stochastic-processes]
topic: "[[梯度噪声协方差、Noise Scale 与 SDE 近似]]"
solution: "[[解答 - 梯度噪声协方差、Noise Scale 与 SDE 近似]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 梯度噪声协方差、Noise Scale 与 SDE 近似

## A. 识别与复述

### TRN07-A01
区分 gradient covariance $C/B$、update covariance $\eta^2C/B$ 和 SDE diffusion coefficient。

### TRN07-A02
定义 simple noise scale $\operatorname{tr}C/\|G\|^2$，解释其 norm/parameterization 依赖。

### TRN07-A03
列出 OU 近似比一般 diffusion 近似额外需要的条件。

## B. 手算与构造

### TRN07-B01
$C=\operatorname{diag}(4,1),B=4,\eta=.1$，求 gradient 与 update covariance。

### TRN07-B02
$\|G\|^2=2,\operatorname{tr}C=20$，求 simple noise scale；分别在 $B=2,10,50$ 比较 noise/signal squared ratio。

### TRN07-B03
一维 $\lambda=2,c=8,\eta=.01,B=4$，求 SDE diffusion coefficient 与 OU stationary variance。

## C. 推导与证明

### TRN07-C01
在连续时间 $s=t\eta$ 下，用 Euler–Maruyama 匹配 $\eta^2C/B$，推出 $\sqrt{\eta/B}C^{1/2}$。

### TRN07-C02
从 OU 过程写出 stationary Lyapunov equation；在 $H,C$ 可同时对角化时求 $\Sigma_i$。

### TRN07-C03
推导存在 lag covariance $\Gamma_k$ 时长期噪声强度为什么包含自相关和。

## D. 边界、反例与纠错

### TRN07-D01
纠正 diffusion coefficient 写成 $\eta C/B$ 的量纲/二阶矩错误。

### TRN07-D02
给出 gradient mean 近零使 noise-scale ratio 不稳定的例子，并提出报告办法。

### TRN07-D03
反驳：“SGD stationary distribution 就是 Bayesian posterior。”列出矩阵匹配、局部性与离散误差条件。

## E. AI 迁移

### TRN07-E01
设计在线 gradient noise scale estimator，说明如何用两个 batch sizes 消去 full-gradient 未知量。

### TRN07-E02
设计 $1/B$ Monte Carlo 实验，并加入相关采样反例。

### TRN07-E03
在带 momentum、clipping、random reshuffling 的训练中，SDE 模型至少需增加哪些 state 或修正？

## 作答与复盘

完成独立尝试后打开 [[解答 - 梯度噪声协方差、Noise Scale 与 SDE 近似]]。
