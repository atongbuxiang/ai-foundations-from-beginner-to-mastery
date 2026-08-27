---
type: concept
status: verified
area: [generative-models, diffusion, variance]
node_id: GEN-45
prerequisites: ["[[DDPM 反向后验、ELBO 与逐步 KL]]", "[[协方差、相关性与条件期望]]"]
related: ["[[DDIM、非 Markov 前向族与确定性采样]]", "[[最小 DDPM 的张量合同、复现门与证据地图]]"]
sources: ["[[S-2022-Su-9245-最优扩散方差估计]]", "[[S-2022-Su-9246-最优扩散方差估计下]]", "[[S-2021-Nichol-Dhariwal-Improved-DDPM]]", "[[S-2022-Bao-Analytic-DPM]]"]
exercises: ["[[习题 - 反向均值、固定方差、学习方差与 Analytic-DPM]]"]
solutions: ["[[解答 - 反向均值、固定方差、学习方差与 Analytic-DPM]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-ddpm-reverse-variance-ledger-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 反向均值、固定方差、学习方差与 Analytic-DPM

> [!abstract] 一句话结论
> Reverse mean 决定一步往哪里走，reverse variance 决定还保留多少条件不确定性。$\tilde\beta_t$ 是知道 $x_0$ 时的 posterior variance，不自动等于真实 $q(x_{t-1}\mid x_t)$ 或 imperfect mean 下的最优 model variance；Gaussian NLL 下的最优 isotropic variance还包含条件方差与 mean error。

## 一、三种 variance 不能混名

1. forward variance $\beta_t$：$q(x_t\mid x_{t-1})$ 的噪声；
2. posterior variance $\tilde\beta_t$：$q(x_{t-1}\mid x_t,x_0)$ 的闭式方差；
3. model variance $\sigma^2_{\theta,t}(x_t)$：$p_\theta(x_{t-1}\mid x_t)$ 的选择/预测。

因为 conditioning 从 $(x_t,x_0)$ 减少为 $x_t$，真实 reverse conditional 还包含对 $x_0|x_t$ 的不确定性；不能只把 $\tilde\beta_t$ 换个字母就叫“真实 reverse variance”。

## 二、给定 mean 时最优 isotropic variance

固定 $x_t$，令真实 conditional 随机变量 $Y=X_{t-1}|x_t$，模型

$$p(Y|x_t)=N(Y;\mu_\theta(x_t),s^2(x_t)I_d).$$

忽略与 $s^2$ 无关常数，conditional expected NLL 是

$$
R(s^2)=\frac d2\log s^2+
\frac{1}{2s^2}E[\|Y-\mu_\theta\|^2|x_t].
$$

对 $s^2$ 求导并令零：

$$
\boxed{s_*^2(x_t)=\frac1dE[\|Y-\mu_\theta(x_t)\|^2|x_t].}
$$

二阶导在该点为正，故为 minimum。

## 三、mean error 为什么进入 variance

令 $m^*(x_t)=E[Y|x_t]$，条件 bias–variance 分解给

$$
E\|Y-\mu_\theta\|^2
=\operatorname{tr}\operatorname{Cov}(Y|x_t)
+\|m^*(x_t)-\mu_\theta(x_t)\|^2.
$$

因此

$$s_*^2=\frac1d\operatorname{tr}\operatorname{Cov}(Y|x_t)
+\frac1d\|m^*-\mu_\theta\|^2.$$

mean 不准时，提高 variance 可降低 overconfident NLL；但这不修复 mean 的样本偏移，只改变随机扩散程度。

## 四、固定 variance 的两个经典端点

DDPM 常比较 $\sigma_t^2=\beta_t$ 与 $\sigma_t^2=\tilde\beta_t$。通常 $\tilde\beta_t\le\beta_t$。前者噪声更大，后者对应含 $x_0$ posterior 的 uncertainty。$t=1$ 时 $\tilde\beta_1=0$，decoder likelihood/离散数据处理需要专门合同，不能直接取 `log(0)`。

## 五、learned-range variance

Improved DDPM 常让网络输出一个插值变量 $r_\theta$，在 log space 组合

$$
\log\sigma^2_\theta
=r_\theta\log\beta_t+(1-r_\theta)\log\tilde\beta_t,
$$

具体 $r$ 的映射/范围依实现。log interpolation 保持正性并覆盖两端。若 variance head 可通过扩大 $\sigma^2$ 降低 mean residual penalty，训练常用 hybrid objective、detach 或其他分工；必须核对代码而非只看公式。

## 六、Analytic-DPM 的证据分层

[[S-2022-Bao-Analytic-DPM]]在指定 DPM family 中把 optimal reverse variance/KL 写成 score 的解析形式，再以 pretrained score network 和 Monte Carlo 估计，配合 bias bounds/clipping。应分为：

1. 理想 score 下的解析 identity；
2. finite network score approximation；
3. Monte Carlo estimator；
4. clipping/bounds 的算法；
5. 指定模型、步数与 metric 的经验结果。

“analytic”不表示最终数值没有估计误差；“optimal”也不指任意 covariance family或感知质量。

## 七、手算例

一维 $Y|x_t$ 的真实均值 2、variance 0.25。若 model mean 为 1.5，则

$$s_*^2=0.25+(2-1.5)^2=0.5.$$

若 mean 修正为 2，则最优 variance 降回 0.25。只用 posterior-style 0.25 配错误 mean 会低估残差 uncertainty。

## 八、科学空间研读框

[[S-2022-Su-9245-最优扩散方差估计]]与[[S-2022-Su-9246-最优扩散方差估计下]]适合建立“均值之外还要估 variance”的问题意识。本节用 conditional Gaussian NLL 给最小一般推导，再把 Analytic-DPM 的 score identity 和 estimator 层分开。

## 九、图：方差选择究竟在补哪本账

先看图回答：哪一项是不可约 conditional variance，哪一项来自 model mean error，哪个论文式 estimator 还增加 score/Monte Carlo 误差？

![[00-知识库管理/_assets/figures/generative-models/fig-ddpm-reverse-variance-ledger-v1.svg|900]]

> [!figure] 图 50.6-05　Posterior variance、reverse mixture、mean error 与 variance estimator
> 左侧分三个 conditional 对象，中间给 Gaussian NLL optimum，右侧拆 Analytic-DPM 的 identity—estimate—clip—experiment。来源：依据 conditional MSE 分解和相关论文独立绘制。

**怎样读图**：先确认 conditioning variables，再判断 variance 是 fixed、learned 还是 estimated。mean error 进入最优 residual variance，却不等于被 variance“修好了”。

**图没有证明什么**：图不证明 isotropic Gaussian 足够，不证明 learned variance 必然改善 FID，也不证明 Analytic-DPM 在任意 score error/步数下最优。

## 十、本节回顾与训练

- $\beta_t,\tilde\beta_t,\sigma^2_{\theta,t}$ 属于不同条件分布；
- 给定 mean 的 Gaussian NLL 最优方差是平均条件平方残差；
- mean error 会增大 NLL-optimal variance；
- analytic identity 与 finite score/Monte Carlo estimate 必须分层；
- [[习题 - 反向均值、固定方差、学习方差与 Analytic-DPM]]
- [[解答 - 反向均值、固定方差、学习方差与 Analytic-DPM]]

