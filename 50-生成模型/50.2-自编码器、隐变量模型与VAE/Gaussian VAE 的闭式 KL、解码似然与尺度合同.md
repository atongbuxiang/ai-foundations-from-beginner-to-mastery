---
type: concept
status: verified
area: [generative-models, vae, gaussian]
aliases: [Gaussian VAE实现, VAE重构损失尺度]
node_id: GEN-12
prerequisites: ["[[VAE 的 ELBO、变分后验与重参数化梯度]]", "[[多元高斯分布]]", "[[最大似然估计与 MAP]]"]
related: ["[[离散似然、连续似然、Dequantization 与 Bits-per-dim]]", "[[Posterior Collapse、率失真与解码器容量]]"]
sources: ["[[S-2018-Su-5253-变分自编码器一]]", "[[S-2018-Su-5383-变分自编码器三]]", "[[S-2013-Kingma-Welling-AEVB]]"]
exercises: ["[[习题 - Gaussian VAE 的闭式 KL、解码似然与尺度合同]]"]
solutions: ["[[解答 - Gaussian VAE 的闭式 KL、解码似然与尺度合同]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-vae-gaussian-loss-ledger-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Gaussian VAE 的闭式 KL、解码似然与尺度合同

> [!abstract] 本节主问题
> 最常见的 VAE 令 $q_\phi(z\mid x)$ 为 diagonal Gaussian、$p(z)=\mathcal N(0,I)$。这让 KL 有闭式，但“重构 loss”仍取决于 observation model。MSE、BCE 和 categorical CE 不是可随意互换的画质指标，而是不同 likelihood 假设及尺度合同。

## 一、编码器到底输出什么

对 $d_z$ 维 latent，encoder 通常输出

$$
\mu_\phi(x)\in\mathbb R^{d_z},\qquad
\ell_\phi(x)=\log\sigma_\phi^2(x)\in\mathbb R^{d_z}.
$$

于是

$$
q_\phi(z\mid x)=\mathcal N\!\left(z;\mu,\operatorname{diag}(e^\ell)\right),
\qquad z=\mu+e^{\ell/2}\odot\epsilon.
$$

网络输出 log-variance 是为保证方差为正并改善数值范围。实现时对 $\ell$ clip 是额外优化决定，会改变 variational family 的可达范围。

## 二、从一般 Gaussian KL 推到标准正态

一维 $q=\mathcal N(\mu,\sigma^2)$、$p=\mathcal N(0,1)$：

$$
\log\frac{q(z)}{p(z)}
=-\log\sigma-\frac{(z-\mu)^2}{2\sigma^2}+\frac{z^2}{2}.
$$

在 $q$ 下取期望，使用

$$
\mathbb E_q[(Z-\mu)^2]=\sigma^2,\qquad
\mathbb E_q[Z^2]=\mu^2+\sigma^2,
$$

得到

$$
\mathrm{KL}(q\|p)=\frac12(\mu^2+\sigma^2-\log\sigma^2-1).
$$

diagonal 情形因坐标独立而相加：

$$
\boxed{\mathrm{KL}(q_\phi(z\mid x)\|\mathcal N(0,I))
=\frac12\sum_{j=1}^{d_z}
(\mu_j^2+e^{\ell_j}-\ell_j-1).}
$$

每项非负可由 $u-\log u-1\ge0$ 与 $\mu^2\ge0$ 看出；等号当且仅当 $\mu_j=0,\sigma_j^2=1$。

## 三、Gaussian decoder：MSE 的完整来源

设数据维数 $D$，且

$$
p_\theta(x\mid z)=\mathcal N(x;m_\theta(z),\tau^2I).
$$

则

$$
-\log p_\theta(x\mid z)
=\frac D2\log(2\pi\tau^2)
+\frac{1}{2\tau^2}\|x-m_\theta(z)\|_2^2.
$$

只有当固定 $\tau^2$ 且只比较 $\theta$ 时，第一项才是可省常数。若框架使用 mean squared error

$$
\operatorname{MSE}_{mean}=D^{-1}\|x-m\|^2,
$$

那么正确 NLL 系数是 $D/(2\tau^2)$，不是 1。改图像分辨率或 sum/mean 会改变 reconstruction 与 KL 的相对权重。

若学习 $\tau(z)$，则 log-scale 项不能删除；无限增大或缩小方差都受两项共同约束。

## 四、Bernoulli decoder 与 BCE

对 $x_j\in\{0,1\}$，若

$$
p_\theta(x\mid z)=\prod_j\pi_j(z)^{x_j}(1-\pi_j(z))^{1-x_j},
$$

则 negative log likelihood 是逐维 binary cross-entropy：

$$
-\log p_\theta(x\mid z)
=-\sum_j[x_j\log\pi_j+(1-x_j)\log(1-\pi_j)].
$$

把连续灰度 $x\in[0,1]$ 直接塞入 BCE 可解释为二值像素的期望或 soft-target 目标，却不是自然的连续 density；若原数据是 uint8，还要处理 discrete likelihood/dequantization 合同。

## 五、Categorical、logistic mixture 与文本

- uint8 像素可用 256-way categorical；
- discretized logistic mixture 对每个 bin 积分连续 CDF 差；
- token decoder 使用 vocabulary categorical，NLL 对位置求和；
- 文本若以 token mean 而 KL 以 sample sum，相对权重随序列长度改变。

“VAE 的重构是 MSE，所以模糊”最多描述某个 Gaussian mean decoder 与显示协议；它不是 VAE 家族定理。更强 likelihood、hierarchy 和 architecture 能显著改变样本，NVAE 是后续反例案例。

## 六、$\beta$、free bits 与尺度不可分

常见 objective

$$
J=\text{reconstruction NLL}+\beta\,\mathrm{KL}
$$

只有在 reconstruction 的单位、维度 reduction、batch reduction 固定时，$\beta$ 才可比较。若一份代码按像素求和、另一份求平均，同样 $\beta=1$ 实际 trade-off 可差 $D$ 倍。

free bits 常形如

$$
\sum_j\max(\lambda,\mathrm{KL}_j),
$$

其 gradient 与原 ELBO 不同；它是 anti-collapse heuristic 或约束近似，不应继续称为 exact standard ELBO。

## 七、数值稳定清单

1. 用 logits 版本 BCE/CE，避免先 sigmoid 再 log；
2. 记录 log-variance 范围与 clamp；
3. 明确 KL 是 per-dimension、per-sample、batch mean 还是 total；
4. 明确 reconstruction 是 sum/mean 及数据尺度 $[0,1]$、$[-1,1]$ 或 uint8；
5. 报告 nats、bits、bits/dim 的换算；
6. 检查 $\sigma\to0$ 时 KL 发散和 decoder variance 的退化行为。

## 八、手算一次完整 loss

取 $d_z=2$，$\mu=(1,0)$，$\sigma^2=(1,4)$：

$$
\mathrm{KL}=\frac12[(1+1-0-1)+(0+4-\log4-1)]
=\frac12(4-\log4)\approx1.3069.
$$

若 $D=4,\tau^2=0.25$ 且平方误差为 $0.5$，Gaussian NLL 为

$$
2\log(2\pi\cdot0.25)+\frac{0.5}{0.5}
\approx1.9032.
$$

negative ELBO 的这次 latent sample 估计约 $3.2101$ nats。仅报告“MSE=0.125，KL=1.307”会遗漏系数和常数，不能与其他实现直接比。

## 九、科学空间研读框

[[S-2018-Su-5253-变分自编码器一]]和[[S-2018-Su-5383-变分自编码器三]]给出 Gaussian 编码与 KL 的中文直觉；本节与 [[S-2013-Kingma-Welling-AEVB]] 对齐标准记号，并补齐 observation likelihood、variance、dimension/reduction 和单位合同。博客中的“重构误差”在本卷一律先问它对应哪个 $p_\theta(x\mid z)$。

## 十、图：一份 loss 的尺度总账

先看图回答：从 decoder 输出到 NLL 之间还缺哪三个选择？为什么同样写 MSE + KL 的两份代码可能优化完全不同的 trade-off？

![[00-知识库管理/_assets/figures/generative-models/fig-vae-gaussian-loss-ledger-v1.svg|900]]

> [!figure] 图 50.2-04　Gaussian KL 与 observation likelihood 尺度合同
> 图左展示逐维 KL 的均值、方差和 log-variance 贡献；图右把 likelihood family、variance、维度 reduction 与最终 loss 系数串成账本。来源：依据 Gaussian NLL 与 KL 闭式独立绘制。

**怎样读图**：先沿模型假设选择 Bernoulli/Gaussian/categorical，再检查 sum/mean 与数据单位，最后才与 KL 合并。任何中间选择变化都可能改变有效 $\beta$。

**图没有证明什么**：图不证明 Gaussian 或 Bernoulli 是数据的正确模型，也不证明某个 loss scale 会带来最佳感知质量；它只保证概率与实现口径可追溯。

## 十一、本节回顾

- diagonal Gaussian KL 可逐维闭式计算；
- MSE 是固定方差 Gaussian NLL 的一部分，系数由 $D$、$\tau^2$ 和 reduction 决定；
- BCE 对应 Bernoulli 质量函数，不是任意连续图像 density；
- $\beta$ 只有在完整尺度合同固定后才有可比意义；
- “VAE 必然模糊”不是由 ELBO 形式推出的定理。

## 十二、练习与独立详解

- [[习题 - Gaussian VAE 的闭式 KL、解码似然与尺度合同]]
- [[解答 - Gaussian VAE 的闭式 KL、解码似然与尺度合同]]
