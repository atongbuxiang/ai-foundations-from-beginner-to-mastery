---
type: exercise
status: draft
topic: "[[NTK、Lazy Training 与 Kernel Regime]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - NTK、Lazy Training 与 Kernel Regime]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - NTK、Lazy Training 与 Kernel Regime
## A
### LT-NTK-A01
定义 empirical NTK，并证明训练 Gram matrix 半正定。
### LT-NTK-A02
区分 NNGP kernel 与 NTK。
### LT-NTK-A03
什么额外条件把时变 NTK dynamics 变为 lazy dynamics？
## B
### LT-NTK-B01
$K_0=\operatorname{diag}(2,1/2)$、$r_0=(1,1)^T$，写出 $r_t$。
### LT-NTK-B02
若 $\lambda_{\min}(K_0)=0.1$，要使 $\|r_t\|\le0.01\|r_0\|$，给出充分的 $t$。
### LT-NTK-B03
$K=\begin{pmatrix}2&0\\0&1\end{pmatrix}$、$y-f_0(X)=(2,3)^T$、$k(x,X)=(1,1)$，求 $f_\infty(x)-f_0(x)$。
## C
### LT-NTK-C01
从平方损失 gradient flow 推导 $\dot f_t(X)=-K_t(f_t(X)-y)$。
### LT-NTK-C02
在固定核下推导 $r_t=e^{-K_0t}r_0$。
### LT-NTK-C03
推导测试点的 kernel interpolation 公式。
## D
### LT-NTK-D01
审计“无限宽网络训练误差指数下降，所以测试误差也指数下降”。
### LT-NTK-D02
为什么 raw parameter displacement 小不是 lazy training 的不变证据？
### LT-NTK-D03
审计“模型有十亿参数，因此它处于 NTK regime”。
## E
### LT-NTK-E01
设计 finite-width 网络的 lazy-regime 诊断面板。
### LT-NTK-E02
设计一个要求 feature learning 的任务来比较 NTK 与有限网络。
### LT-NTK-E03
写 NTK claim card：parameterization、极限顺序、kernel drift、optimization 与 risk bridge。

