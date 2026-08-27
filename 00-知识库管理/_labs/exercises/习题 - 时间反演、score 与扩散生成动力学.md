---
type: exercise
status: draft
area: [math/stochastic-processes, math/sde, ai/generative-modeling]
topic: "时间反演、score 与扩散生成动力学"
prerequisites: ["[[时间反演、score 与扩散生成动力学]]"]
related: ["[[解答 - 时间反演、score 与扩散生成动力学]]", "[[实验 - 反向时间、score恒等式与扩散采样误差审计]]", "[[练习与测验 MOC]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 时间反演、score 与扩散生成动力学

> [!info] 使用方式
> 共15题，按 A—E 五层递进。先独立写出对象、时钟、条件与误差目标，再计算；不得用“扩散模型公式”替代推导。正式作答前不要打开[[解答 - 时间反演、score 与扩散生成动力学]]。

## A 组：定义、时钟与基本手算

### DYN-REV-A01　两个时钟与符号转换

给定空间齐次 diffusion

$$
dX_t=f(t,X_t)dt+g(t)dW_t,
\qquad t\in[0,T],
$$

密度为 $p_t$。

1. 定义 $Y_s=X_{T-s}$，写出 $s$ 从0增到 $T$ 时的 reverse SDE；
2. 再写成保留物理时间 $t$、积分从 $T$ 到0的形式；
3. 解释为什么反向 Brownian motion 不能只理解为把一条 forward Brownian 数组倒序；
4. 指出 reverse SDE 与 reverse probability-flow ODE 的 score 系数差别。

### DYN-REV-A02　constant-$\beta$ VP SDE

考虑

$$
dX_t=-\frac\beta2X_tdt+\sqrt\beta dW_t,
\qquad \beta>0.
$$

1. 用 integrating factor 求 $X_t$；
2. 求 $q(x_t\mid x_0)$；
3. 若 $X_0$ 均值为 $m_0$、方差为 $v_0$，求 $m_t,v_t$；
4. 说明什么意义下它“variance preserving”，以及有限 $T$ 时为何 $p_T$ 通常不等于 $\mathcal N(0,1)$。

### DYN-REV-A03　Gaussian score 与 Tweedie

设

$$
X_t=\alpha X_0+\sigma\varepsilon,
\qquad
X_0\sim\mathcal N(m_0,v_0),
\quad
\varepsilon\sim\mathcal N(0,1).
$$

1. 求 $p_t$ 与其 score；
2. 直接用 Gaussian conditioning 求 $\mathbb E[X_0\mid X_t=x]$；
3. 用 Tweedie 公式再次求同一条件均值并核对；
4. 解释 posterior mean、MAP 与“最近的 clean sample”为什么是不同对象。

## B 组：核心推导

### DYN-REV-B01　从 current 推导 state-dependent 反向漂移

对

$$
dX_t=f(t,X_t)dt+B(t,X_t)dW_t,
\qquad D=BB^\top,
$$

已知前向 current

$$
J=fp-\frac12\nabla\cdot(Dp).
$$

1. 从 $q_s=p_{T-s}$ 证明反向 current 应为 $-J$；
2. 推导 reverse drift
   $$
   b_{\rm rev}=-f+p^{-1}\nabla\cdot(Dp);
   $$
3. 展开成 $-f+\nabla\cdot D+D\nabla\log p$；
4. 在一维 $D(x)=1+x^2$、$f=0$ 时写出反向 drift；
5. 说明为什么 current 配平还不自动等于完整 path-law time-reversal theorem。

### DYN-REV-B02　Hyvärinen score matching

设 $p$ 是 $\mathbb R^d$ 上光滑正密度，$s_\theta$ 是光滑向量场。

1. 从
   $$
   \frac12\mathbb E_p\|s_\theta-\nabla\log p\|^2
   $$
   推导
   $$
   \mathbb E_p\left[\frac12\|s_\theta\|^2+\nabla\cdot s_\theta\right]+C_p;
   $$
2. 明确写出分部积分的 boundary term；
3. 给出一个 boundary term 不消失的例子或条件；
4. 解释为什么 empirical point-mass distribution 上不能直接照搬 ambient score matching。

### DYN-REV-B03　Denoising score identity

设 corruption kernel 为 $q_t(x\mid x_0)$，边缘为

$$
p_t(x)=\int q_t(x\mid x_0)p_0(x_0)dx_0.
$$

1. 证明
   $$
   \nabla\log p_t(x)
   =\mathbb E[\nabla_x\log q_t(X_t\mid X_0)\mid X_t=x];
   $$
2. 用条件期望正交分解证明 DSM population minimizer 是 marginal score；
3. 对 $X_t=\alpha_tX_0+\sigma_t\varepsilon$ 求 conditional target；
4. 列出使“population minimizer = 实际训练所得网络”失效的至少四个环节。

## C 组：离散—连续桥与参数化

### DYN-REV-C01　DDPM 的闭式 forward law 与 posterior

设

$$
q(x_k\mid x_{k-1})
=\mathcal N(\sqrt{a_k}x_{k-1},\beta_kI),
\qquad a_k=1-\beta_k,
$$

并记 $\bar a_k=\prod_{j=1}^ka_j$。

1. 用归纳法证明
   $$
   q(x_k\mid x_0)=\mathcal N(\sqrt{\bar a_k}x_0,(1-\bar a_k)I);
   $$
2. 完成平方推导 $q(x_{k-1}\mid x_k,x_0)$ 的 mean 与 variance；
3. 将真实 $x_0$ 替换为 noise predictor，推出常用 $\mu_\theta(x_k,k)$；
4. 解释为什么 fixed-time reparameterization 不等于一条已耦合的 Markov path。

### DYN-REV-C02　四种参数化与有效权重

在

$$
x_t=\alpha_tx_0+\sigma_t\varepsilon,
\qquad \alpha_t^2+\sigma_t^2=1
$$

下：

1. 推导 score、$\varepsilon$、$x_0$ 三种预测之间的换算；
2. 定义 $v=\alpha_t\varepsilon-\sigma_tx_0$，推导由 $(x_t,v)$ 恢复 $(x_0,\varepsilon)$；
3. 将带权 score MSE 写成 noise MSE 与 $x_0$ MSE，给出权重因子；
4. 说明 time sampling density、explicit loss weight 与 parameterization factor 怎样共同决定 effective weighting。

### DYN-REV-C03　Gaussian VP 的 reverse SDE 与 PF ODE

设 constant-$\beta$ VP，且

$$
X_0\sim\mathcal N(m_0,v_0).
$$

1. 写出 $p_t$ 与 score；
2. 写出 forward-$s$ reverse SDE drift；
3. 写出 reverse PF ODE drift；
4. 推导二者的 mean/variance evolution，并核对都沿 $p_{T-s}$；
5. 若在保留 diffusion 的 reverse SDE 中错误使用半个 score，写出 variance ODE，并说明为什么步长趋零也不能修复。

## D 组：生成算法与误差审计

### DYN-REV-D01　ELBO、simplified loss 与 sampler

1. 写出 DDPM joint generative model 与 variational forward chain；
2. 推导 negative log-likelihood 的 ELBO 分解；
3. 说明 fixed reverse variance 时 Gaussian KL 如何变成带权 noise MSE；
4. 解释 unweighted simplified loss 与原 ELBO 的差别；
5. 比较 ancestral DDPM、reverse-SDE EM、DDIM $\eta=0$ 与 PF ODE 的随机性、path law 和可用误差概念。

### DYN-REV-D02　双峰 Gaussian mixture 的 score 与去噪

设

$$
X_0\sim\frac12\mathcal N(-m,\tau^2)
+\frac12\mathcal N(m,\tau^2),
\qquad
X_t=\alpha X_0+\sigma\varepsilon.
$$

1. 写出 $p_t(x)$；
2. 用 posterior component responsibilities 推导 mixture score；
3. 求 $\mathbb E[X_0\mid X_t=x]$；
4. 验证 Tweedie 公式；
5. 讨论 $x=0$ 附近 posterior mean、component MAP 与 mode coverage 的差别。

### DYN-REV-D03　设计一个三轴 refinement 实验

为一维 Gaussian VP reverse sampler 设计实验，必须分别识别：

1. exact score 下的 finite-step solver error；
2. multiplicative score bias；
3. terminal prior mismatch；
4. 把 PF 半系数错误用于 noisy reverse SDE 的 coefficient error。

要求给出：控制变量、refinement 轴、理论 reference、至少两个指标、预期曲线、不能从该实验外推的结论。

## E 组：研究级审计与迁移

### DYN-REV-E01　时间反演 claim ladder

某报告写道：

> “我们让 learned reverse SDE 的 Fokker–Planck 与 forward density 反向一致，因此证明了模型就是数据过程的精确时间反演。”

请逐层审计：

1. PDE formal identity；
2. marginal PDE uniqueness；
3. transition-kernel reversal；
4. path-law reversal；
5. learned-score approximation；
6. finite-step numerical implementation；
7. degenerate diffusion、boundary 与 singular data endpoint。

为每层写出还缺少的条件或证据。

### DYN-REV-E02　Guidance 改变了哪个分布

1. 从 Bayes 推导 conditional score；
2. 若 classifier guidance 使用 scale $\gamma$，求其固定时刻对应的 unnormalized density；
3. 对
   $$
   s_{\rm cfg}=s_u+w(s_c-s_u)
   $$
   在两支 score 精确时求对应 density；
4. 解释为什么 $w>1$ 不是“更精确的 conditional score”；
5. 设计同时报告条件一致性、样本质量与 coverage 的评估协议。

### DYN-REV-E03　扩散生成研究卡

选择一个你计划研究的扩散生成系统，写一份可复核研究卡，至少包含：

- data/state/support 与 preprocessing；
- forward SDE 或 discrete chain；
- terminal prior mismatch；
- score/noise/$x_0$/$v$ 参数化与换算；
- time sampling、loss weighting 和 small-noise cutoff；
- reverse dynamics、score coefficient、solver 与 NFE；
- conditioning/guidance convention；
- terminal、score、solver、MC、evaluation 六类误差；
- exact/controlled baseline；
- 至少两个 falsification experiment；
- 不允许从有限实验升级出的三条一般结论。

## 完成标准

- A：时钟、VP 与 Gaussian score 能独立手算；
- B：reverse current、score matching 与 DSM 能从定义推导；
- C：DDPM posterior、参数化权重和 reverse/PF 系数不混淆；
- D：能把训练目标、连续模型和 sampler 分层并设计受控实验；
- E：能审计 time-reversal/guidance 声明并写出可复核研究合同。

没有真实首次作答、评分、改参复现与间隔重做前，本习题集只表示 `composed`，不构成掌握证据。
