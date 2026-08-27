---
type: exercise
status: draft
area: [generative-models, inverse-problems]
topic: "[[逆问题、约束采样与 Plug-and-Play 控制]]"
solution: "[[解答 - 逆问题、约束采样与 Plug-and-Play 控制]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 逆问题、约束采样与 Plug-and-Play 控制
## A. 识别与复述
### GEN67-A01
写出 $p(x_0\mid y)$ 与 noisy-time posterior score。
### GEN67-A02
为什么 $p(y\mid x_t)$ 通常不是 $p(y\mid x_0)$ 把 $x_0$ 换成 $x_t$？
### GEN67-A03
区分 likelihood guidance、hard projection、proximal step 与 PnP。
## B. 手算与建模
### GEN67-B01
$y=Ax+\eta$，$A=[1\ 2]$、$y=3$、$x=(1,0)$、$\sigma_y^2=2$。求 $\nabla_x\log p(y\mid x)$。
### GEN67-B02
一维模型取 $\tau_0=1,\alpha=.8,\sigma=.6,a=2,\sigma_y=.5$。求 $k,c$ 与 exact $y\mid x_t$ 方差。
### GEN67-B03
对 $g(x)=\frac12\|x-y\|^2$ 求 $\operatorname{prox}_{\lambda g}(z)$。
## C. 推导与证明
### GEN67-C01
推导 $p(y\mid x_t)=\int p(y\mid x_0)p(x_0\mid x_t)dx_0$。
### GEN67-C02
推导一维线性 Gaussian 的 exact likelihood score，并与 plug-in 比较。
### GEN67-C03
从 Gaussian likelihood 推导含 $J_{\hat x_0}^TA^T$ 的 chain-rule gradient。
## D. 边界、反例与纠错
### GEN67-D01
给出 noisy measurement 下 hard projection 过拟合噪声的反例。
### GEN67-D02
解释 `detach(x0_hat)` 为何改变优化/采样对象。
### GEN67-D03
反驳“measurement residual 最小的样本就是 posterior 最好的样本”。
## E. AI 迁移
### GEN67-E01
设计 operator adjoint test 与 finite-difference gradient test。
### GEN67-E02
为 DPS 类论文写 posterior calibration 复现清单。
### GEN67-E03
若 measurement noise 被错设为实际的一半，预测 guidance 与 coverage 会怎样变化并设计验证。
## 解答入口
[[解答 - 逆问题、约束采样与 Plug-and-Play 控制]]
