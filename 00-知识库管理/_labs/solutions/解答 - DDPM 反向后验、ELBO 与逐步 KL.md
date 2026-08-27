---
type: solution
status: draft
topic: "[[DDPM 反向后验、ELBO 与逐步 KL]]"
exercise: "[[习题 - DDPM 反向后验、ELBO 与逐步 KL]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - DDPM 反向后验、ELBO 与逐步 KL
## A. 识别与复述
### GEN42-A01
前者额外知道 clean $x_0$，是两项 Gaussian 的闭式 posterior，用作训练 teacher；后者把 $x_0|x_t$ 混合掉，通常复杂且部署真正需要近似。
### GEN42-A02
$\tilde\beta_t=\beta_t(1-\bar\alpha_{t-1})/(1-\bar\alpha_t)$；$\tilde\mu_t=[\sqrt{\bar\alpha_{t-1}}\beta_t/(1-\bar\alpha_t)]x_0+[\sqrt{\alpha_t}(1-\bar\alpha_{t-1})/(1-\bar\alpha_t)]x_t$。
### GEN42-A03
Terminal $KL(q(x_T|x_0)||p(x_T))$；$t=2…T$ 的 denoising posterior-vs-model KL；$-log p_\theta(x_0|x_1)$ reconstruction/decoder term。
## B. 手算与建模
### GEN42-B01
$\bar\alpha_t=0.8(0.75)=0.6$；$\tilde\beta_t=0.25(0.2)/(0.4)=0.125$。
### GEN42-B02
$c_0=\sqrt{0.9}(0.2)/0.28\approx0.67763$；$c_t=\sqrt{0.8}(0.1)/0.28\approx0.31944$。
### GEN42-B03
同方差 Gaussian KL 的 mean 部分 $(0.2)^2/(2\cdot0.5)=0.04$。
## C. 推导与证明
### GEN42-C01
把 likelihood 看成关于 $x_{t-1}$：precision 为 $\alpha_t/\beta_t$；prior conditional precision 为 $1/(1-\bar\alpha_{t-1})$。相加取逆，通分并用 $\bar\alpha_t=\alpha_t\bar\alpha_{t-1}$，得 $\beta_t(1-\bar\alpha_{t-1})/(1-\bar\alpha_t)$。
### GEN42-C02
将 $x_0=(x_t-\sqrt{1-\bar\alpha_t}\epsilon)/\sqrt{\bar\alpha_t}$ 代入两系数式；收集 $x_t$ 与 $\epsilon$，用 $\bar\alpha_t=\alpha_t\bar\alpha_{t-1}$ 化简为 $\alpha_t^{-1/2}(x_t-\beta_t\epsilon/\sqrt{1-\bar\alpha_t})$。
### GEN42-C03
用 $q(x_{1:T}|x_0)$ 作变分分布，Jensen 得 $E_q[\log p(x_{0:T})-\log q]$。把 forward factor 用 Bayes 写成 posterior ratios，连乘 telescoping，剩下 terminal prior ratio、逐步 posterior/model ratios 和 $p_\theta(x_0|x_1)$；取负期望即三类项。
## D. 边界、反例与纠错
### GEN42-D01
若 $x_0|x_t$ 是多峰，$q(x_{t-1}|x_t)=\int q(x_{t-1}|x_t,x_0)q(x_0|x_t)dx_0$ 是 Gaussian mixture，一般非 Gaussian。只在特殊 Gaussian data/线性情形才闭合。
### GEN42-D02
$x_0,x_t$ 的单位相同但噪声尺度/相关性不同，Bayesian linear estimator 系数不是概率 mixture 权重；没有 convex-combination 必要。代回 posterior 公式而不是查和为 1。
### GEN42-D03
VLB 权重含 schedule 与 reverse variance，并有 terminal/reconstruction/variance terms。Simple loss 删除或改变权重，只共享某些 Bayes optimum，不共享数值和 likelihood 单位。
## E. AI 迁移
### GEN42-E01
小维直接从 joint Gaussian covariance 用条件 Gaussian 公式计算 posterior，与 $\tilde\mu,\tilde\beta$ 对照；随机 sample 后检验 standardized residual $(x_{t-1}-\tilde\mu)/\sqrt{\tilde\beta}$ 近标准正态。
### GEN42-E02
输入 $x_t:[B,C,H,W],t:[B]$；mean/noise head 同形；fixed variance gather 后为 $[B,1,1,1]$，learned per-pixel variance 则同形。sample 输出 $[B,C,H,W]$，per-sample KL 对非 batch 轴 reduction。
### GEN42-E03
正确：$x_{1:T}$ 是 latent chain，forward 是 variational posterior，reverse joint 给 generative decoder，存在 ELBO。错误：把它等同 token AR、说每层独立参数/任意 encoder，或忽略固定 noising、Markov Gaussian与时间参数共享。

