---
type: solution
status: draft
topic: "[[DDPM 前向 Markov 加噪与闭式边缘]]"
exercise: "[[习题 - DDPM 前向 Markov 加噪与闭式边缘]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - DDPM 前向 Markov 加噪与闭式边缘
## A. 识别与复述
### GEN41-A01
$\beta_t\in(0,1)$，$\alpha_t=1-\beta_t$，$\bar\alpha_t=\prod_{s=1}^t\alpha_s$。$q(x_t\mid x_{t-1})=N(\sqrt{\alpha_t}x_{t-1},\beta_tI)$。
### GEN41-A02
$q(x_t\mid x_0)=N(\sqrt{\bar\alpha_t}x_0,(1-\bar\alpha_t)I)$，故可采 $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$。“分布相等”不表示新 $\epsilon$ 等于任一逐步噪声，也不重建同一中间 path。
### GEN41-A03
有限 schedule 通常只有 $\bar\alpha_T$ 很小而非严格 0；均值仍含 $\sqrt{\bar\alpha_T}x_0$，方差也非严格 1。terminal prior KL 衡量残留 mismatch。
## B. 手算与建模
### GEN41-B01
$\alpha_1=0.9,\alpha_2=0.8,\bar\alpha_2=0.72$；$q(x_2\mid x_0)=N(\sqrt{0.72}x_0,0.28I)$。
### GEN41-B02
$a=0.6,\sigma=0.8$，$x_t=0.6(2)+0.8(-0.5)=0.8$；SNR $=0.36/0.64=0.5625$。
### GEN41-B03
$t:[8]$；gather 后 $a_t,\sigma_t:[8,1,1,1]$；$x_0,\epsilon,x_t:[8,3,32,32]$。
## C. 推导与证明
### GEN41-C01
$x_2=\sqrt{\alpha_1\alpha_2}x_0+\sqrt{\alpha_2\beta_1}\epsilon_1+\sqrt{\beta_2}\epsilon_2$。独立噪声 covariance 相加：$\alpha_2\beta_1+\beta_2=\alpha_2(1-\alpha_1)+1-\alpha_2=1-\alpha_1\alpha_2$。
### GEN41-C02
假设 $x_{t-1}|x_0$ 均值 $\sqrt{\bar\alpha_{t-1}}x_0$、variance $(1-\bar\alpha_{t-1})I$。一步线性变换后均值乘 $\sqrt{\alpha_t}$，variance 变为 $\alpha_t(1-\bar\alpha_{t-1})+\beta_t=1-\bar\alpha_t$，完成归纳。
### GEN41-C03
joint factorization 为 $q(x_{1:T}|x_0)=\prod_tq(x_t|x_{t-1})$，故给 $x_{t-1}$ 后 $x_t$ 与更早状态条件独立。闭式只积分掉中间变量得到 $q(x_t|x_0)$；joint 的相关结构仍决定 posterior/ELBO。
## D. 边界、反例与纠错
### GEN41-D01
$1-\bar\alpha_t$ 是 variance，Gaussian sample 必须乘标准差 $\sqrt{1-\bar\alpha_t}$。直接乘 variance 会得到 noise variance $(1-\bar\alpha_t)^2$。
### GEN41-D02
博客若写 $x_t=a_tx_{t-1}+b_t\epsilon$ 且 $a_t^2+b_t^2=1$，则本卷 $\sqrt{\alpha_t}=a_t,\sqrt{\beta_t}=b_t$；因此本卷 $\beta_t=b_t^2$，不能同名直接替换。
### GEN41-D03
许多小于 1 的 $\alpha_t$ 连乘指数变小，低精度最小可表示正数有限，最终会舍入为 0；数学实数乘积仍正。用 float64 累加 `log1p(-beta)` 可延后下溢并保相对精度。
## E. AI 迁移
### GEN41-E01
固定 $x_0,t$，重复采样大量 $x_t$；逐维样本均值对照 $a_tx_0$、variance 对照 $\sigma_t^2$，附置信误差；再把逐步模拟与一次闭式的样本统计/分布检验对照。
### GEN41-E02
检查 shape/length；$0<\beta_t<1$；$\alpha_t=1-\beta_t$；$\bar\alpha_0=1$；$\bar\alpha_t$ 严格下降且正；posterior variance 非负；sqrt 参数有限；端点 SNR 达目标；不同 dtype 差在 tolerance 内。
### GEN41-E03
训练只需 sample $t$ 并用闭式构造 $x_t$，成本一次。逐步模拟给相同 conditional marginal但多花 $O(t)$；只有研究 joint path、posterior coupling或调试时才需要中间状态。

