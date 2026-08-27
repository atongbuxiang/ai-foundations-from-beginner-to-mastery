---
type: derivation
status: verified
area: [generative-models, diffusion, variational-inference]
node_id: GEN-42
prerequisites: ["[[DDPM 前向 Markov 加噪与闭式边缘]]", "[[变分推断、ELBO 与证据分解]]", "[[多元高斯分布]]"]
related: ["[[数据、噪声、速度与 Score 参数化]]", "[[反向均值、固定方差、学习方差与 Analytic-DPM]]"]
sources: ["[[S-2022-Su-9152-DDPM自回归式VAE]]", "[[S-2022-Su-9164-DDPM贝叶斯去噪]]", "[[S-2020-Ho-DDPM]]"]
exercises: ["[[习题 - DDPM 反向后验、ELBO 与逐步 KL]]"]
solutions: ["[[解答 - DDPM 反向后验、ELBO 与逐步 KL]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-ddpm-posterior-elbo-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# DDPM 反向后验、ELBO 与逐步 KL

> [!abstract] 一句话结论
> 给定 $x_0$ 后，$q(x_{t-1}\mid x_t,x_0)$ 是两个 Gaussian 信息源的乘积，因此均值和方差闭式可算。DDPM 把它作为训练 reverse kernel 的 teacher，并把整条 latent chain 的负 ELBO 拆成终端 prior KL、逐步 denoising KL 和数据重构项。

## 一、先分清两个 reverse 对象

1. $q(x_{t-1}\mid x_t,x_0)$：训练时 $x_0$ 已知，Gaussian 闭式；
2. $q(x_{t-1}\mid x_t)$：需对未知 $x_0\mid x_t$ 混合，一般不是单 Gaussian，也不可直接算。

模型用

$$p_\theta(x_{t-1}\mid x_t)=
\mathcal N(x_{t-1};\mu_\theta(x_t,t),\Sigma_\theta(x_t,t))$$

近似第二个对象，但训练 KL 可借第一个对象构造。

## 二、Gaussian Bayes 推 posterior

由 Markov 性，

$$
q(x_{t-1}\mid x_t,x_0)
\propto q(x_t\mid x_{t-1})q(x_{t-1}\mid x_0).
$$

两项分别是

$$
\mathcal N(x_t;\sqrt{\alpha_t}x_{t-1},\beta_tI),
\quad
\mathcal N(x_{t-1};\sqrt{\bar\alpha_{t-1}}x_0,(1-\bar\alpha_{t-1})I).
$$

把关于 $x_{t-1}$ 的二次项配方，precision 相加：

$$
\tilde\beta_t^{-1}
=\frac{\alpha_t}{\beta_t}+\frac1{1-\bar\alpha_{t-1}}.
$$

化简得

$$
\boxed{\tilde\beta_t=
\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t.}
$$

线性项乘 posterior variance，得到

$$
\boxed{\tilde\mu_t(x_t,x_0)=
\frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1-\bar\alpha_t}x_0
+\frac{\sqrt{\alpha_t}(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}x_t.}
$$

## 三、换成噪声参数的均值

由 $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$，

$$x_0=\frac{x_t-\sqrt{1-\bar\alpha_t}\epsilon}{\sqrt{\bar\alpha_t}}.$$

代入并整理可得

$$
\boxed{\tilde\mu_t(x_t,x_0)=
\frac1{\sqrt{\alpha_t}}
\left(x_t-
\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon\right).}
$$

用网络 $\epsilon_\theta(x_t,t)$ 替换真实噪声，就得到常见 reverse mean parameterization。

## 四、完整手算：$t=2$

沿用 $\beta_1=0.1,\beta_2=0.2$，故 $\bar\alpha_1=0.9,\bar\alpha_2=0.72$：

$$\tilde\beta_2=\frac{0.1}{0.28}\cdot0.2=\frac1{14}\approx0.07143.$$

均值权重为

$$c_0=\frac{\sqrt{0.9}\,0.2}{0.28}\approx0.6776,
\qquad
c_t=\frac{\sqrt{0.8}\,0.1}{0.28}\approx0.3194.$$

它们不需要相加为 1，因为作用于不同噪声尺度的 $x_0,x_t$，不能把它当普通 convex combination。

## 五、整条生成模型与 ELBO

定义 reverse joint

$$
p_\theta(x_{0:T})=p(x_T)\prod_{t=1}^Tp_\theta(x_{t-1}\mid x_t),
\qquad p(x_T)=N(0,I).
$$

forward variational distribution

$$q(x_{1:T}\mid x_0)=\prod_{t=1}^Tq(x_t\mid x_{t-1}).$$

Jensen 给

$$
\log p_\theta(x_0)\ge
E_q\left[\log p_\theta(x_{0:T})-\log q(x_{1:T}\mid x_0)\right].
$$

利用 Bayes 重排 Markov factors，负 ELBO 可写成

$$
\boxed{
L_{VLB}=
E_q\left[
D_{KL}(q(x_T\mid x_0)\|p(x_T))
+\sum_{t=2}^T D_{KL}(q(x_{t-1}\mid x_t,x_0)\|p_\theta(x_{t-1}\mid x_t))
-\log p_\theta(x_0\mid x_1)
\right].}
$$

三类项分别叫 $L_T$、$L_{t-1}$ 和 $L_0$。索引名称在不同代码中可能平移；公式对象比变量名更可靠。

## 六、Gaussian KL 为什么变成加权 MSE

若 $p_\theta$ variance 固定为 $\sigma_t^2I$，teacher posterior covariance 与 $\theta$ 无关，则 KL 中与 mean 有关的部分是

$$
\frac1{2\sigma_t^2}
\|\tilde\mu_t(x_t,x_0)-\mu_\theta(x_t,t)\|^2.
$$

把两种 mean 都写成 noise parameterization，得到

$$L_{t-1}=E[w_t\|\epsilon-\epsilon_\theta(x_t,t)\|^2]+C_t,$$

其中 $w_t$ 由 $\alpha_t,\beta_t,\bar\alpha_t,\sigma_t^2$ 决定。原 DDPM 的 simplified loss 把这类权重重排/删除；不能说它逐项等于 VLB。

## 七、层次 VAE 视角的准确边界

[[S-2022-Su-9152-DDPM自回归式VAE]]把 $x_{1:T}$ 看作层次 latents，很适合解释 ELBO。但 DDPM 有固定 forward encoder、Markov Gaussian steps、强参数共享和特定 terminal prior；它不是 token autoregression，也不是任意 hierarchical VAE 的别名。

## 八、图：posterior teacher 如何进入逐步 ELBO

先看图回答：训练时哪一条虚线使用了 $x_0$，部署采样时为什么不能使用它？

![[00-知识库管理/_assets/figures/generative-models/fig-ddpm-posterior-elbo-v1.svg|900]]

> [!figure] 图 50.6-02　Forward posterior teacher、learned reverse kernel 与 ELBO 三类项
> 左侧由 $x_0,x_t$ 得 closed-form posterior，中间比较 $p_\theta$，右侧列 terminal/prior、denoising KL 和 reconstruction。来源：据 DDPM variational derivation 独立绘制。

**怎样读图**：训练时 $x_0$ 来自数据，可构造 teacher posterior；生成时只有 $x_t$，网络必须用 $x_t,t$ 预测 mean/variance。逐步 KL 的 teacher 与真实 reverse marginal 不应混名。

**图没有证明什么**：图不证明 Gaussian reverse family 完全包含真实 reverse conditional，不证明 simplified MSE 等于 VLB，也不证明每步 KL 小就保证有限步样本语义好。

## 九、本节回顾与训练

- posterior closed form 依赖同时条件化 $x_t,x_0$；
- precision 相加比死背均值公式更可靠；
- ELBO 拆成 terminal、denoising KL、reconstruction；
- fixed variance 下逐步 KL 的 mean 部分变成加权 MSE；
- [[习题 - DDPM 反向后验、ELBO 与逐步 KL]]
- [[解答 - DDPM 反向后验、ELBO 与逐步 KL]]

