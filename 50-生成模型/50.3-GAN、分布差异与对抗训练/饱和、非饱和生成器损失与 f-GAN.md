---
type: concept
status: verified
area: [generative-models, gan, f-divergence]
node_id: GEN-19
prerequisites: ["[[原始 GAN、最优判别器与 Jensen–Shannon 散度]]", "[[f-散度、Bregman 散度与概率度量]]"]
related: ["[[IPM、Wasserstein-1 与 Kantorovich 对偶]]", "[[GAN 稳定化方法、受控比较与证据地图]]"]
sources: ["[[S-2018-Su-6016-fGAN与变分散度]]", "[[S-2014-Goodfellow-GAN]]"]
exercises: ["[[习题 - 饱和、非饱和生成器损失与 f-GAN]]"]
solutions: ["[[解答 - 饱和、非饱和生成器损失与 f-GAN]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-gan-generator-loss-gradients-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 饱和、非饱和生成器损失与 f-GAN

> [!abstract] 本节主问题
> 原始 minimax generator 与常用 non-saturating generator 在理想 equilibrium 可一致，却给出不同的有限训练梯度。f-GAN 再把特定 log classification 推广到 convex-conjugate variational divergence；“目标 divergence 相同”和“训练向量场相同”必须分开。

## 一、两种 generator loss

令 discriminator logit $a=f_\psi(G_\theta(z))$，$D=\sigma(a)$。

原始 minimax/saturating generator 最小化

$$
L_G^{sat}=E_z\log(1-D(G(z))).
$$

常用 non-saturating 最小化

$$
L_G^{ns}=-E_z\log D(G(z)).
$$

二者都鼓励 $D(G(z))$ 上升，但梯度权重不同。

## 二、对 logit 求导

利用 $\partial_a\log\sigma(a)=1-\sigma(a)$：

$$
\frac{\partial}{\partial a}\log(1-\sigma(a))=-\sigma(a)=-D,
$$

$$
\frac{\partial}{\partial a}[-\log\sigma(a)]=-(1-\sigma(a))=-(1-D).
$$

当 discriminator 很确信 fake，$D\approx0$：saturating 梯度系数接近 0，non-saturating 接近 $-1$，因此后者早期信号更强。还要乘 $\nabla_xf_\psi(x)\nabla_\theta G_\theta(z)$；logit 系数不是完整 gradient norm。

## 三、相同 equilibrium 不等于相同 divergence

Non-saturating loss 是为 gradient 设计的 surrogate。把理想 $D^*$ 代入，可得到某种 density-ratio 加权 objective，但不能简单说它“仍精确最小化同一个 JS”并据此解释有限训练。equilibrium set、population scalar、parameter vector field 是三个层次。

## 四、f-GAN 的 Fenchel 形式

对 convex $f$、$f(1)=0$：

$$
D_f(P\|Q)=E_Q f\!\left(\frac{p}{q}\right).
$$

Fenchel conjugate $f^*(t)=\sup_u\{tu-f(u)\}$ 给

$$
f(u)=\sup_t\{tu-f^*(t)\},
$$

从而

$$
D_f(P\|Q)\ge
\sup_{T\in\mathcal T}
\{E_PT(X)-E_Qf^*(T(X))\}.
$$

若允许适当全函数类并满足正则条件，supremum 取到真实 divergence；neural $\mathcal T$ 只给受限 lower bound。

## 五、函数域与 output activation

不同 $f$ 的 conjugate domain 不同。f-GAN 常令 $T=g_f(V_\psi)$ 以满足 domain。若忘记 activation/domain，objective 可能无界或不再对应目标 $f$。generator surrogate 的选取又是第二层决定。

## 六、density ratio 与梯度支持

很多 $f$-divergence 在 support 不重叠时饱和或无穷；variational lower bound 的 critic 也可能在有限 class 下平滑。训练有信号可能来自 function restriction/regularization，而非真实 divergence 的理想梯度。这正是科学空间“生产车间”直觉需要补的边界。

## 七、科学空间研读框

[[S-2018-Su-6016-fGAN与变分散度]]清楚展示 convex conjugate 如何制造 critic objective。本节采用其推导入口，并强制记录：$f$ 的方向、conjugate domain、critic transform、受限函数类、generator surrogate 与实际 optimizer。原始 GAN 是其中一个特例，但 non-saturating 更新不应被机械贴回 exact JS。

## 八、图：同一 critic 下两种梯度权重

先看图回答：当 $D(fake)\to0$，两条 generator 曲线的 logit slope 怎样变化？f-GAN 的 $f$、critic objective 与 generator surrogate 又分别在哪一层选择？

![[00-知识库管理/_assets/figures/generative-models/fig-gan-generator-loss-gradients-v1.svg|900]]

> [!figure] 图 50.3-03　saturating/non-saturating 梯度与 f-GAN 选择树
> 左侧画 logit 梯度系数，右侧分开 divergence、variational critic 与 generator surrogate。来源：依据 logistic derivative 与 f-GAN Fenchel form 独立绘制。

**怎样读图**：先看 $D$ 接近 0/1 时的局部系数，再沿 chain rule 补 critic/input 与 generator Jacobian；右侧每个选择都可能改变训练场。

**图没有证明什么**：图不证明 non-saturating 在所有阶段都更好，也不证明任意 $f$ 的 neural estimator 都一致或稳定。

## 九、本节回顾

- saturating 与 non-saturating 共享方向意图但梯度权重不同；
- $D\approx0$ 时 non-saturating 避免 logistic 系数消失；
- equilibrium、population divergence 与 finite vector field 不同；
- f-GAN 用 Fenchel conjugate 把 divergence 写成 sample expectation；
- neural critic、domain transform 与 generator surrogate 各引入新责任。

## 十、练习与独立详解

- [[习题 - 饱和、非饱和生成器损失与 f-GAN]]
- [[解答 - 饱和、非饱和生成器损失与 f-GAN]]

