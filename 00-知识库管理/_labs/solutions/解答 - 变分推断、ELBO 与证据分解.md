---
type: solution
status: draft
area: [math/information-theory, math/statistics, ai/generative-models]
topic: "变分推断、ELBO 与证据分解"
exercise: "[[习题 - 变分推断、ELBO 与证据分解]]"
prerequisites: ["[[变分推断、ELBO 与证据分解]]"]
related: ["[[信息论与统计学习接口 MOC]]", "[[练习与测验 MOC]]"]
sources: ["Blei-Kucukelbir-McAuliffe-2017-Variational-Inference", "Kingma-Welling-2014-AEVB", "Rezende-Mohamed-Wierstra-2014-Stochastic-Backprop", "Burda-Grosse-Salakhutdinov-2016-IWAE", "Su-5253-VAE-I", "Su-5343-VAE-Bayesian", "Su-5383-VAE-Reparameterization"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 变分推断、ELBO 与证据分解

> [!warning] 使用边界
> ELBO identity 是相对于 model $p_\theta$ 的精确等式。即使 $q$ 等于 model posterior，也只表示 inference 对该模型 exact；若 generative model 错设，仍可能离真实 data-generating mechanism 很远。

## A. 识别与复述

### INFO-VI-A01

给 generative model：

$$
p_\theta(x,z)=p_\theta(z)p_\theta(x\mid z).
$$

- prior $p_\theta(z)$：生成 latent 的 model assumption；
- likelihood $p_\theta(x\mid z)$：observation/decoder model；
- joint：二者 product；
- evidence $p_\theta(x)=\int p_\theta(x,z)dz$；
- model posterior $p_\theta(z\mid x)=p_\theta(x,z)/p_\theta(x)$；
- variational posterior $q_\phi(z\mid x)$：人为选择/训练的 tractable approximation；
- posterior predictive（global parameter Bayesian setting）还需对 parameter posterior 积分；普通 VAE point-estimates $\theta$ 时常只做 latent posterior predictive/conditional generation。

前五项由 model 与 Bayes 唯一确定；$q$ 的 family、parameterization 与 amortization 是 inference design。字母 $p,q$ 可换，角色不能换。

### INFO-VI-A02

joint-ratio form：

$$
\mathcal L(q)=E_q\log\frac{p_\theta(x,z)}{q(z)}.
$$

reconstruction–KL form：

$$
\mathcal L(q)
=E_q\log p_\theta(x\mid z)-D(q(z)\|p_\theta(z)).
$$

evidence identity：

$$
\log p_\theta(x)
=\mathcal L(q)+D(q(z)\|p_\theta(z\mid x)).
$$

equality $\mathcal L=\log p(x)$ iff $q=p(z\mid x)$ almost everywhere。若 $q$ 在 joint 为零处有正质量，ELBO 可为 $-\infty$、gap 为 $+\infty$。finite identity 还需 log ratio integrable。

### INFO-VI-A03

- approximation gap：chosen family $\mathcal Q$ 的最佳成员仍无法表示 posterior；
- amortization gap：共享 mapping $x\mapsto q_\phi$ 与逐样本 family optimum 的差；
- optimization gap：parameterized objective 尚未达到其 optimum；
- Monte Carlo error：objective/gradient/held-out estimator 的有限样本误差；
- model misspecification：$p_\theta$ family 与真实 data law 的差。

前四项位于“如何求 model posterior/优化 model objective”的计算层；misspecification 在更外层。posterior KL identity精确包含给定 $q$ 的总 inference gap，但把它归因到 family/amortization/optimization需定义相应 intermediate optima；它不测 model truth gap。

## B. 手算与构造

### INFO-VI-B01

evidence：

$$
p(x=1)=0.3(0.9)+0.7(0.2)=0.41,
$$

$$
\log p(x=1)\approx-0.891598.
$$

posterior：

$$
r=P(z=1\mid x=1)=\frac{0.27}{0.41}\approx0.658537.
$$

$q=0.8$ 时 posterior KL：

$$
\begin{aligned}
D(\operatorname{Ber}(0.8)\|\operatorname{Ber}(r))
&=0.8\log\frac{0.8}{r}
+0.2\log\frac{0.2}{1-r}\\
&\approx0.048689.
\end{aligned}
$$

joint-ratio ELBO：

$$
\begin{aligned}
\mathcal L
&=0.8\log\frac{0.3(0.9)}{0.8}
+0.2\log\frac{0.7(0.2)}{0.2}\\
&\approx-0.940287.
\end{aligned}
$$

相加：

$$
-0.940287+0.048689=-0.891598=\log0.41.
$$

### INFO-VI-B02

每维 contribution：

$$
K_j=\frac12(\mu_j^2+\sigma_j^2-1-\log\sigma_j^2).
$$

第一维：

$$
K_1=\frac12(1+0.25-1-\log0.25)
\approx0.818147.
$$

第二维：

$$
K_2=\frac12(0.25+4-1-\log4)
\approx0.931853.
$$

total KL 恰为

$$
K_1+K_2=1.75\text{ nats}.
$$

`sum latent, mean batch` 保留 per-example total KL；若 32 个例子相同，结果仍 1.75。`mean all elements` 再除 latent dimension $d=2$，结果 0.875，改变 KL 与 reconstruction 的相对权重；`sum batch` 则为 $32(1.75)=56$。

### INFO-VI-B03

mean-field update：

$$
q_1(z_1)\propto
\exp\{E_{q_2}\log r(z_1,Z_2)\}.
$$

$q_2(1)=0.5$ 时：

$$
w_0=\sqrt{0.1\cdot0.2}\approx0.141421,
$$

$$
w_1=\sqrt{0.3\cdot0.4}\approx0.346410.
$$

所以

$$
q_1(1)=\frac{w_1}{w_0+w_1}\approx0.710102.
$$

再更新 $q_2$：

$$
v_0=\exp[(1-q_1(1))\log0.1+q_1(1)\log0.3]
\approx0.218175,
$$

$$
v_1=\exp[(1-q_1(1))\log0.2+q_1(1)\log0.4]
\approx0.327184,
$$

$$
q_2(1)=\frac{v_1}{v_0+v_1}\approx0.599943.
$$

每个 update 是固定其他 factor 时的 exact coordinate maximum，所以 ELBO 不下降；它不保证一步到 posterior，也不保证 joint global optimum。

## C. 推导与证明

### INFO-VI-C01

Jensen：

$$
\log p(x)
=\log E_q\frac{p(x,Z)}q
\ge E_q\log\frac{p(x,Z)}q=\mathcal L(q).
$$

equality 要求 $p(x,z)/q(z)$ 在 $q$ 下为常数，归一化给 $q=p(z\mid x)$。

KL expansion：

$$
\begin{aligned}
D(q\|p(z\mid x))
&=E_q\log\frac{q(z)p(x)}{p(x,z)}\\
&=\log p(x)-\mathcal L(q).
\end{aligned}
$$

KL equality 同样要求 $q=p(z\mid x)$。固定 $p,x$，$\log p(x)$ 与 $q$ 无关，因此 maximizing ELBO 等价于 minimizing reverse KL $D(q\|p)$。forward direction不会从这个 decomposition 自然出现。

### INFO-VI-C02

固定 $q_{-j}$。与 $q_j$ 相关的 functional：

$$
J(q_j)=\int q_j(z_j)a(z_j)dz_j
-\int q_j(z_j)\log q_j(z_j)dz_j,
$$

其中

$$
a(z_j)=E_{q_{-j}}\log p(x,z).
$$

加 multiplier $\lambda(\int q_j-1)$。functional derivative：

$$
a(z_j)-\log q_j(z_j)-1+\lambda=0.
$$

故

$$
\log q_j^*(z_j)=a(z_j)+\text{const}.
$$

它是该 coordinate 的 global maximum，因为 entropy term对 $q_j$ concave、linear term 不改 concavity。因此替换为 $q_j^*$ 不降低 ELBO。所有 factors 的 joint landscape 和 model parameters 通常 nonconvex/multiconcave，coordinate fixed point 可以是 local optimum。

### INFO-VI-C03

对

$$
J(\phi)=\int q_\phi(z)f_\phi(z)dz
$$

微分：

$$
\nabla J
=E_q[f_\phi(Z)\nabla\log q_\phi(Z)+\nabla f_\phi(Z)].
$$

若 $f$ 不显式依赖 $\phi$，得到 score-function estimator。因为

$$
E_q\nabla\log q=\int\nabla q(z)dz=\nabla1=0,
$$

故减去与 $Z$ 无关的 baseline $b$ 不改 expectation。

若 $Z=g_\phi(\varepsilon)$、$\varepsilon\sim s$ 不依赖 $\phi$：

$$
J=E_s f_\phi(g_\phi(\varepsilon)),
$$

$$
\nabla J=E_s\nabla_\phi f_\phi(g_\phi(\varepsilon)).
$$

交换需 almost-everywhere differentiability、可积 dominating bound/Leibniz 条件和 support 处理。score estimator常无偏但高 variance；pathwise 通常低 variance，但需可重参数/可微路径。Gumbel relaxation可降低 variance，却对 discrete target 引入 relaxation/straight-through bias。

## D. 边界、反例与纠错

### INFO-VI-D01

若两个 modes 很窄且相距远，单 Gaussian $q$：

- reverse KL $D(q\|p)$ 对 $q$ 放在两峰之间的 low-density 区域惩罚大，常选择一个 mode；
- forward KL $D(p\|q)$ 在 target 两个 modes 下取 expectation，漏任一 mode 会受罚，常用一个较宽 Gaussian 覆盖两者，mean 在中间、variance 很大。

但“必然”过强：若 modes 距离、权重、variance、family constraints 或 initialization 改变，reverse-KL optimum 可覆盖多个 modes；优化也可能停在不同 stationary point。mode-seeking 是结构倾向，不是无条件结论。

### INFO-VI-D02

canonical ELBO：

$$
\mathcal L_1=E_q\log p(x\mid z)-D(q\|p)\le\log p(x).
$$

$\beta$ objective：

$$
\mathcal L_\beta
=\mathcal L_1-(\beta-1)D(q\|p).
$$

- $\beta>1$：extra term nonpositive，故 $\mathcal L_\beta\le\mathcal L_1\le\log p(x)$；仍是一个数值 lower bound，但不再满足 canonical gap 恰等于 posterior KL；
- $\beta=1$：标准 ELBO identity；
- $0<\beta<1$：加回 positive $(1-\beta)D(q\|p)$，可超过 evidence。取 $q=p(z\mid x)$ 且 posterior 与 prior 不同，则 $\mathcal L_1=\log p(x)$，而 $\mathcal L_\beta>\log p(x)$。

因此“lower bound”与“标准 evidence decomposition”必须分开。

### INFO-VI-D03

令

$$
p_\theta(x,z)=p(z)p_\theta(x),
$$

即 decoder 完全忽略 $z$。则

$$
p_\theta(z\mid x)=p(z).
$$

取 $q(z\mid x)=p(z)$：posterior gap 与 prior KL 都为 0，

$$
\mathcal L=E_q\log p_\theta(x)=\log p_\theta(x).
$$

ELBO 对 model evidence 是 tight，但 $I_q(X;Z)=0$，latent 没有 representation value。若 decoder 本身很强，reconstruction/log-likelihood 仍可好。这是“bound tight、KL small、latent useless”并存的精确例子。

## E. AI 迁移

### INFO-VI-E01

至少审计：

1. pixels 是离散 8-bit、dequantized continuous 还是缩放实数；
2. Bernoulli likelihood 是否与数据支持匹配；
3. BCE API 接受 logits 还是 probabilities；
4. per-pixel sum/mean 的单位；
5. KL 应先 sum latent 还是 mean latent；
6. batch reduction 是否一致；
7. image resolution 改变是否自动改变 reconstruction/KL 比；
8. constant terms 是否为模型比较保留；
9. decoder variance 是否固定/学习；
10. reported bits/dim 是否含 $\log2$、dequantization correction。

coherent 方案例如：

- 离散 binary pixels：Bernoulli logits likelihood，sum pixels，sum latent KL，再 mean batch；
- continuous/dequantized pixels：Gaussian/logistic-mixture likelihood，保留 scale/normalizer，同样以 per-example nats 或 bits/dim统一报告。

若坚持 mean-all KL，应显式乘回 latent dimension或把它定义为 modified weighting。

### INFO-VI-E02

公平协议：

- 同一 raw held-out data、normalization/tokenizer；
- encoder/proposal family 与 refinement budget分别报告；
- 对每模型用相同 $K$ grid，如 $1,10,100,1000,5000$；
- stable logsumexp 计算 log-average weights；
- 报 weight ESS、max normalized weight、seed/CI；
- proposal 可按模型优化，但 tuning 不用 test values；
- 区分 train objective 与 evaluation estimator；
- 相同 examples 与 compute/wall-clock budget作配对比较；
- 用更强 proposal/per-example refinement检查 inference gap；
- 不把 finite-$K$ lower-bound ordering直接称为 true evidence ordering，除非差异超过 estimator/gap uncertainty且稳定。

### INFO-VI-E03

| 方法 | 目标/梯度 | 优点 | 风险与报告 |
|---|---|---|---|
| REINFORCE | 对原 discrete expectation 的 score gradient | 原则上无偏 | 高 variance；baseline/control variate、samples、seed |
| Gumbel–Softmax | continuous relaxed categorical | pathwise、较低 variance | biased relaxed objective；temperature schedule、limit instability |
| straight-through | forward hard sample、backward relaxed gradient | train/eval form接近 | gradient 一般 biased 且不对应单一光滑 objective |

必须报告 category count、temperature/annealing、hard/soft forward、gradient estimator、control variate、sample count、variance与最终 discrete evaluation。不能只因能反传就称“无偏重参数化”。

## 完成标准

你应能从任意 $p(x,z),q(z)$ 独立写出 evidence identity，并在每个 VAE 数值旁标明 model term、inference estimate、reduction 与 gap 来源；还应能构造 KL=0 但 latent 无用的 collapse 反例。
