---
type: solution
status: draft
topic: "[[Marginal Score、Conditional Score 与去噪等价]]"
exercise: "[[习题 - Marginal Score、Conditional Score 与去噪等价]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Marginal Score、Conditional Score 与去噪等价
## A. 识别与复述
### GEN52-A01
$s^{marg}_t(x)=\nabla_x\log p_t(x)$；$s^{cond}_t(x,x_0)=\nabla_x\log q_t(x|x_0)$。在正则条件下
$$s^{marg}_t(x)=E[s^{cond}_t(X_t,X_0)|X_t=x].$$
### GEN52-A02
等号指 conditional target 对模型输入作 $L^2$ 投影得到 marginal score，并使标准 population MSE 相差模型无关常数，因而 gradient/minimizer 相同。它不指 target 逐样本相同、loss 数值相同或 estimator variance 相同。
### GEN52-A03
$X_t=aX_0+\sigma\epsilon$ 时 $s^{cond}=-(X_t-aX_0)/\sigma^2=-\epsilon/\sigma$。故 $s=-\widehat\epsilon/\sigma$；$\widehat X_0=(X_t-\sigma\widehat\epsilon)/a=(X_t+\sigma^2\widehat s)/a$。
## B. 手算与建模
### GEN52-B01
边缘 variance 是 $a^2\tau_0^2+\sigma^2=2^2\cdot4+9=25$，故 $s^{marg}(x)=-x/25$。conditional score 是 $-(x-2x_0)/9=-\epsilon/3$。
### GEN52-B02
$$C=\frac{a^2\tau_0^2}{\sigma^2(a^2\tau_0^2+\sigma^2)}=\frac{16}{9\cdot25}=\frac{16}{225}.$$
它是 conditional target 给定 $X_t$ 后仍剩的 variance，不依赖 predictor。
### GEN52-B03
$s_\theta=-0.5/0.6=-5/6\approx-0.8333$。$x_{0,\theta}=(1-0.6\cdot0.5)/0.8=0.875$。也可用 $(x+\sigma^2s)/a$ 得同值。
## C. 推导与证明
### GEN52-C01
微分积分交换后，$\nabla p_t=\int p_0q_t\nabla\log q_tdx_0$。除以 $p_t(x)$，系数 $p_0q_t/p_t$ 正是 posterior $p(x_0|x_t=x)$，得到条件期望 identity。
### GEN52-C02
令 $U=s^{cond}$、$m=E[U|X_t,t]$。展开 $\|U-s\|^2=\|U-m\|^2+\|m-s\|^2+2(U-m)^\top(m-s)$。最后一项条件于输入的期望为零，故得到常数差。
### GEN52-C03
若 $w=w(X_t,t)$，条件化时可把 $w(m-s)$ 提出，交叉项仍为零。若 $w$ 依赖 $X_0$、$U$、模型输出或与 target 相关的 batch normalization，不能提出条件期望，分解需重做。
## D. 边界、反例与纠错
### GEN52-D01
同一个 minibatch 上 $U$ 与 $m$ 不同，故两个平方和一般不同；只有对总体期望做正交分解才相差固定 $C$。有限 batch 的差还随机波动。
### GEN52-D02
标准常数差对任意共同模型类都成立，因为对每个 $s_\theta$ 有 $L_{cond}(\theta)=L_{marg}(\theta)+C$。有限 capacity 不破坏 population 等价；真正会不同的是 empirical sampling、非标准权重、parameterization、optimizer 与数值误差。
### GEN52-D03
batch 近似后 score 是随机分子除随机分母，ratio expectation 不等于 ratio of expectations，故有限 batch 一般有偏；每个 query 还要与许多 clean samples 计算 kernel，高维权重会退化，成本近似 $O(B^2)$。
## E. AI 迁移
### GEN52-E01
选可解析 Gaussian mixture，采 $(X_0,X_t)$；在网格或 bin 内平均 conditional score，与解析 mixture marginal score比较。报告 bin/kernel bias、样本量与置信区间，并用全局矩条件 $E[s(X)\varphi(X)]$ 交叉检查。
### GEN52-E02
用同一参数点和同一 $X_t$，一条估计器用 sampled conditional target，另一条用解析 oracle marginal score。跨许多 batch 比较 gradient 均值应一致，covariance/范数 variance 通常不同；按 noise level 分层报告。
### GEN52-E03
先问使用的 score loss 权重、population/empirical 层、terminal mismatch、continuous/finite sampler。Wasserstein theorem 要保留 regularity、常数和端点项；FID 是另一表示空间的有限样本指标。需要受控实验而非由 loss 单调性直接推出。
