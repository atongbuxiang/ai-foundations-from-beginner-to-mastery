---
type: concept
status: verified
area: [generative-models, vae, variational-inference]
aliases: [VAE ELBO推导, 重参数化技巧]
node_id: GEN-11
prerequisites: ["[[隐变量模型的联合分布、边缘似然与后验]]", "[[变分推断、ELBO 与证据分解]]", "[[Monte Carlo、重要性采样与方差缩减]]"]
related: ["[[Gaussian VAE 的闭式 KL、解码似然与尺度合同]]", "[[IWAE、重要性权重与推断缺口]]"]
sources: ["[[S-2018-Su-5383-变分自编码器三]]", "[[S-2013-Kingma-Welling-AEVB]]", "[[S-2014-Rezende-Stochastic-Backprop]]"]
exercises: ["[[习题 - VAE 的 ELBO、变分后验与重参数化梯度]]"]
solutions: ["[[解答 - VAE 的 ELBO、变分后验与重参数化梯度]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-vae-elbo-reparameterization-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# VAE 的 ELBO、变分后验与重参数化梯度

> [!abstract] 本节主问题
> 当 $\log p_\theta(x)$ 中的 latent 积分难算时，引入 $q_\phi(z\mid x)$ 可以得到可优化下界。ELBO 既可由 Jensen 推出，也可由 exact evidence decomposition 推出；重参数化则把“分布随 $\phi$ 改变的采样”改写为“固定噪声经过可微映射”，从而得到 pathwise gradient。

## 一、目标不是 ELBO，而是 evidence

理想 maximum likelihood 对每个数据点最大化

$$
\log p_\theta(x)=\log\int p_\theta(x,z)\,dz.
$$

VAE 的 ELBO 是在难以直接优化 evidence 时采用的可计算代理。把代理误称为最终建模对象，会遮蔽 bound gap 与 inference quality。

## 二、第一条推导：Jensen 下界

取任何满足 support 条件的 $q_\phi(z\mid x)$。插入 $q/q$：

$$
\begin{aligned}
\log p_\theta(x)
&=\log\int q_\phi(z\mid x)
\frac{p_\theta(x,z)}{q_\phi(z\mid x)}\,dz\\
&=\log\mathbb E_{q_\phi(z\mid x)}
\left[\frac{p_\theta(x,z)}{q_\phi(z\mid x)}\right]\\
&\ge \mathbb E_q\left[
\log p_\theta(x,z)-\log q_\phi(z\mid x)\right]\\
&=:\mathcal L(\theta,\phi;x).
\end{aligned}
$$

不等号来自 concave $\log$ 的 Jensen。等号成立当 importance weight $p(x,z)/q(z\mid x)$ 在 $q$ 下几乎处处为常数，即 $q=p_\theta(z\mid x)$。若 $q$ 漏掉 joint 的重要 support，估计会失败，形式上的比值也可能无定义。

## 三、第二条推导：精确证据分解

从 $\log p_\theta(x,z)=\log p_\theta(z\mid x)+\log p_\theta(x)$ 出发：

$$
\begin{aligned}
\mathrm{KL}(q_\phi(z\mid x)\|p_\theta(z\mid x))
&=\mathbb E_q[\log q_\phi-\log p_\theta(z\mid x)]\\
&=\log p_\theta(x)-\mathcal L(\theta,\phi;x).
\end{aligned}
$$

因此

$$
\boxed{\log p_\theta(x)=\mathcal L(x)+
\mathrm{KL}(q_\phi(z\mid x)\|p_\theta(z\mid x)).}
$$

这说明 bound gap 非负；同一 $\theta$ 下提高 ELBO 等价于让 $q$ 更接近真后验，但同时优化 $\theta$ 时模型本身也在移动。

## 四、重构—正则形式

代入 $p_\theta(x,z)=p(z)p_\theta(x\mid z)$：

$$
\boxed{
\mathcal L(x)=
\mathbb E_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]
-\mathrm{KL}(q_\phi(z\mid x)\|p(z)).}
$$

第一项是期望 log likelihood，不是与概率模型无关的“重构相似度”；第二项同时约束条件编码携带的信息与 aggregate posterior 对 prior 的匹配，详见 GEN-14。

训练通常最小化 negative ELBO：

$$
\widehat J=-\frac1B\sum_{i=1}^B
\left[\frac1L\sum_{\ell=1}^L\log p_\theta(x_i\mid z_{i\ell})
-\mathrm{KL}(q_\phi(z\mid x_i)\|p(z))\right].
$$

batch reduction、data dimension reduction 和 dataset scaling 都是合同的一部分。

## 五、为什么不能直接“对随机样本求导”

考虑 $F(\phi)=\mathbb E_{z\sim q_\phi}[f(z)]$。样本 $z$ 的分布随 $\phi$ 变，朴素自动微分无法穿过“sample from distribution”黑箱。两类通用估计器是：

### 5.1 Score-function

$$
\nabla_\phi F=\mathbb E_{q_\phi}
[f(z)\nabla_\phi\log q_\phi(z)].
$$

适用广，但方差常高，需要 baseline/control variate。

### 5.2 Pathwise / 重参数化

若存在与 $\phi$ 无关的 $\epsilon\sim r(\epsilon)$ 和可微 $z=T_\phi(\epsilon,x)$，则

$$
F(\phi)=\mathbb E_{\epsilon\sim r}[f(T_\phi(\epsilon,x))],\qquad
\nabla_\phi F=\mathbb E_\epsilon[\nabla_\phi f(T_\phi(\epsilon,x))].
$$

Gaussian 常用

$$
\epsilon\sim\mathcal N(0,I),\qquad
z=\mu_\phi(x)+\sigma_\phi(x)\odot\epsilon.
$$

随机性被移到固定分布 $\epsilon$，梯度沿确定性 computation graph 回传。

## 六、一个一维梯度核对

设 $z=\mu+\sigma\epsilon$，$f(z)=z^2$。解析期望为

$$
F(\mu,\sigma)=\mu^2+\sigma^2,\quad
\partial_\mu F=2\mu,\quad\partial_\sigma F=2\sigma.
$$

pathwise 单样本梯度为

$$
\partial_\mu z^2=2z,\qquad
\partial_\sigma z^2=2z\epsilon.
$$

取期望分别得到 $2\mu$ 与 $2\sigma$。这验证 unbiasedness，但有限 $L$ 时仍有 Monte Carlo 方差。

## 七、训练、评价与采样是三条路径

- **训练**：$x\to q_\phi(z\mid x)\to z\to p_\theta(x\mid z)$，优化 ELBO estimator；
- **评价 evidence**：常用更强 importance estimator/IWAE，不能只报告训练 loss；
- **无条件生成**：$z\sim p(z)$，再 $x\sim p_\theta(x\mid z)$，通常不使用 encoder。

若部署时输出 decoder mean 而非从 likelihood 抽样，实际输出分布又与模型声明不同。

## 八、常见错误

1. 把 $\mathbb E_q\log p(x\mid z)$ 写成 $\log p(x\mid\mathbb E z)$；非线性下不等；
2. 把 KL 方向倒置；ELBO 是 $\mathrm{KL}(q\|p)$；
3. 忘记 support 条件，importance ratio 失效；
4. 因为 ELBO 升高就断言 test likelihood 升高；bound 与 generalization 都还需检查；
5. 认为重参数化让 estimator 没有随机误差；它通常只是降方差。

## 九、科学空间研读框

[[S-2018-Su-5383-变分自编码器三]]给出 Gaussian 参数化和噪声分离的直观解释；[[S-2013-Kingma-Welling-AEVB]]与[[S-2014-Rezende-Stochastic-Backprop]]提供原始变分与 stochastic backprop 框架。本节补上两条完整 ELBO 推导、Jensen 等号条件、support 条件及训练/评价/生成三路径。

博客公式若以“loss”写正号，本卷先还原为 maximized ELBO，再统一写 negative ELBO；符号相反不代表方法不同。

## 十、图：下界缺口与重参数化计算图

先看图回答：竖直 gap 是哪一个 KL？梯度为什么能越过 $z$ 节点？测试时从 prior 采样走哪条不同路径？

![[00-知识库管理/_assets/figures/generative-models/fig-vae-elbo-reparameterization-v1.svg|900]]

> [!figure] 图 50.2-03　ELBO identity 与 pathwise gradient
> 左侧以 evidence、ELBO 和 posterior KL 构成精确加法；右侧把随机节点改写成固定噪声到 $z$ 的可微映射。来源：依据 AEVB 与 stochastic backprop 公式独立绘制。

**怎样读图**：左图从下界向上补 posterior KL 才到 log evidence；右图沿 $\epsilon\to z\to\log p_\theta(x\mid z)$ 追踪梯度，注意 $\epsilon$ 的分布不依赖 $\phi$。

**图没有证明什么**：图不保证 variational family 足够强、gradient 方差足够小或优化找到全局最优；也不证明更高 training ELBO 必然带来更好样本。

## 十一、本节回顾

- ELBO 是 log evidence 的下界，gap 恰是真后验 KL；
- reconstruction term 是 observation log likelihood 的期望；
- 重参数化把参数依赖的随机抽样改成固定噪声加可微变换；
- training ELBO、evaluation estimator 和 ancestral sampling 必须分账。

## 十二、练习与独立详解

- [[习题 - VAE 的 ELBO、变分后验与重参数化梯度]]
- [[解答 - VAE 的 ELBO、变分后验与重参数化梯度]]
