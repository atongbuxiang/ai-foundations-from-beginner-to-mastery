---
type: solution
status: verified
area: [training, optimization, stochastic-processes]
topic: "[[梯度噪声协方差、Noise Scale 与 SDE 近似]]"
exercise: "[[习题 - 梯度噪声协方差、Noise Scale 与 SDE 近似]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 梯度噪声协方差、Noise Scale 与 SDE 近似

## A. 识别与复述

### TRN07-A01
Batch gradient noise covariance 是 $C/B$，单位是 gradient squared；乘 update LR 后是 $\eta^2C/B$，单位是 parameter displacement squared。在连续时间 $s=t\eta$ 的 SDE 中 coefficient 是 $\sqrt{\eta/B}C^{1/2}$，再乘 Brownian increment $\Delta W\sim N(0,\eta I)$ 才得到同一步 covariance。

### TRN07-A02
$\mathcal B=\operatorname{tr}C/\|G\|^2$。换 norm、preconditioner 或坐标缩放会同时改变 trace 与 gradient norm，故它不是坐标不变常数；它还随参数和训练阶段变化。

### TRN07-A03
OU 还需在稳定点附近线性化 $G\approx Hu$，把 $C(\theta)$ 近似为常矩阵 $C_*$，并要求 $H$ 的实部为正以存在 stationary covariance。一般 state-dependent diffusion 不需局部常二次假设。

## B. 手算与构造

### TRN07-B01
$C/B=\operatorname{diag}(1,.25)$。$\eta^2=.01$，所以 update covariance $=\operatorname{diag}(.01,.0025)$。

### TRN07-B02
$\mathcal B=20/2=10$。Noise/signal squared ratio 是 $\mathcal B/B$：$B=2$ 为 5，$B=10$ 为 1，$B=50$ 为 .2。

### TRN07-B03
Diffusion coefficient $\sqrt{\eta c/B}=\sqrt{.01\cdot8/4}=\sqrt{.02}\approx.141421$。Stationary variance $\eta c/(2B\lambda)=.08/16=.005$。

## C. 推导与证明

### TRN07-C01
设 $d\Theta=-Gds+\sigma dW$，Euler–Maruyama 一步 $\Delta s=\eta$ 的 noise covariance 是 $\sigma\sigma^T\eta$。令它等于 $\eta^2C/B$，得 $\sigma\sigma^T=\eta C/B$，可取 $\sigma=\sqrt{\eta/B}C^{1/2}$。

### TRN07-C02
对 $du=-Hu,ds+Q^{1/2}dW$，stationary covariance 满足 $H\Sigma+\Sigma H^T=Q$；这里 $Q=\eta C/B$。若同一基中 $H=\operatorname{diag}\lambda_i,C=\operatorname{diag}c_i$，则 $(\lambda_i+\lambda_i)\Sigma_i=\eta c_i/B$，故 $\Sigma_i=\eta c_i/(2B\lambda_i)$。

### TRN07-C03
对和 $S_n=\sum_{t=1}^n\xi_t$，

$$\operatorname{Cov}(S_n)=n\Gamma_0+\sum_{k=1}^{n-1}(n-k)(\Gamma_k+\Gamma_k^T).$$

除以 $n$ 并在可求和条件下令 $n\to\infty$，长期每步 covariance 是 $\Gamma_0+\sum_{k\ge1}(\Gamma_k+\Gamma_k^T)$。所以单步 $C$ 不足以描述 correlated noise。

## D. 边界、反例与纠错

### TRN07-D01
Coefficient 必须是 covariance 的矩阵平方根。若误写 $\sigma=\eta C/B$，EM covariance 变为 $\eta(\eta C/B)(\eta C/B)^T$，一般是 $O(\eta^3/B^2)$ 且包含 $C^2$，不等于目标 $O(\eta^2C/B)$。

### TRN07-D02
例如真实 $\|G\|=10^{-6}$、$\operatorname{tr}C=1$，ratio 为 $10^{12}$；有限样本 mean 的小偏差会巨大改变分母。应同时报告 $\widehat{\operatorname{tr}C}$、$\|\widehat G\|^2$、bias correction/CI、窗口和 floor，不把无穷大截断后当稳定常数。

### TRN07-D03
Posterior covariance 需与目标 Bayesian curvature/temperature 对齐；SGD covariance 依赖 $C,\eta,B$ 和 preconditioner。还需局部二次、stationarity、小步长、正态扩散近似和正确 prior/likelihood scale。一般 SGD stationary law 既非精确 posterior，也未必存在。

## E. AI 迁移

### TRN07-E01
估计 $A_B=E\|\widehat G_B\|^2=\|G\|^2+\operatorname{tr}C/B$。用独立重复得到 $A_{B_1},A_{B_2}$，则

$$\widehat{\operatorname{tr}C}=\frac{A_{B_1}-A_{B_2}}{1/B_1-1/B_2},\quad
\widehat{\|G\|^2}=A_{B_1}-\widehat{\operatorname{tr}C}/B_1.$$

再取比值；应做有限样本 bias/CI 和负估计诊断。

### TRN07-E02
固定 per-example gradient population，对 $B=1,2,4,\ldots$ iid 重采样，估计 covariance trace/eigenvalues 并验证 $B\widehat C_B$；反例把 batch 内样本设为相同或 AR(1) 相关，观察缩放偏离。固定随机种子列表但跨 seed 报区间。

### TRN07-E03
Momentum 要增加 velocity/buffer state并形成 colored noise；clipping 添加 state-dependent bias；reshuffling 添加 sampler phase 和 temporal correlation。还可能需要 time-inhomogeneous $C_t$、jump/heavy-tail 模型和 parameter-dependent diffusion。

## 无提示重做

- [ ] 不看答案从离散 covariance 推出 SDE coefficient。
- [ ] 解一维 OU stationary variance并检查单位。
