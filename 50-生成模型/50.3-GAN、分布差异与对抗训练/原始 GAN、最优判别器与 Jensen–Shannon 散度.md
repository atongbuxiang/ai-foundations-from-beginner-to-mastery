---
type: concept
status: verified
area: [generative-models, gan, divergences]
node_id: GEN-18
prerequisites: ["[[隐式 Pushforward 分布、生成器与判别博弈]]", "[[交叉熵与 KL 散度]]"]
related: ["[[饱和、非饱和生成器损失与 f-GAN]]", "[[IPM、Wasserstein-1 与 Kantorovich 对偶]]"]
sources: ["[[S-2014-Goodfellow-GAN]]"]
exercises: ["[[习题 - 原始 GAN、最优判别器与 Jensen–Shannon 散度]]"]
solutions: ["[[解答 - 原始 GAN、最优判别器与 Jensen–Shannon 散度]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-gan-optimal-discriminator-js-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 原始 GAN、最优判别器与 Jensen–Shannon 散度

> [!abstract] 本节主问题
> 固定生成分布并允许判别器逐点自由优化时，原始 GAN 的最优判别器可闭式求出；代回 minimax value 得到 JS 散度。但这条推导是 best-response population theorem，不是实际有限步 generator gradient 的等式。

## 一、逐点优化 $D$

设 densities 为 $p,q$。固定 $G$ 后

$$
V(D)=\int[p(x)\log D(x)+q(x)\log(1-D(x))]dx.
$$

每个 $x$ 独立最大化

$$
f_x(d)=p\log d+q\log(1-d).
$$

导数与二阶导数：

$$
f_x'(d)=\frac p d-\frac q{1-d},\qquad
f_x''(d)=-\frac p{d^2}-\frac q{(1-d)^2}<0.
$$

令一阶导数为零：

$$
\boxed{D^*(x)=\frac{p(x)}{p(x)+q(x)}}.
$$

若 $p=q=0$，该点对积分无贡献，$D$ 任意。

## 二、代回得到 JS

令 $m=(p+q)/2$：

$$
\begin{aligned}
V(D^*)&=\int p\log\frac p{p+q}+q\log\frac q{p+q}\\
&=\int p\log\frac p{2m}+q\log\frac q{2m}\\
&=-2\log2+KL(P\|M)+KL(Q\|M)\\
&=-\log4+2JS(P\|Q).
\end{aligned}
$$

因此 population minimax 的全局最小值为 $-\log4$，在 $P=Q$ 时取到，此时 $D^*=1/2$。

## 三、测度版本避免 density 陷阱

取 $\mu=P+Q$，令 $p=dP/d\mu,q=dQ/d\mu$，同一推导成立。即使 $P,Q$ 各自无 ambient density，只要相对共同支配测度写 Radon–Nikodym derivative 即可。

## 四、support 分离时 JS 饱和

若 $P,Q$ 互相奇异，$M=(P+Q)/2$，则

$$
KL(P\|M)=KL(Q\|M)=\log2,\quad JS(P\|Q)=\log2.
$$

不管两个 support 在 ground space 中距离 $0.001$ 还是 $1000$，JS 都相同。它是 divergence 的事实；实际 generator 是否零梯度还取决于 critic parameterization 与 surrogate。

## 五、三个容易错用的“等号”

1. $V(D^*)=-\log4+2JS$：只在判别器对当前 $G$ 最优；
2. $P=Q$ 是全局 optimum：不保证参数空间路径能到达；
3. $D=1/2$ 在 equilibrium：训练中 $D\approx1/2$ 也可能是 underfitting、过强正则或未训练。

## 六、有限数据中的过拟合判别器

经验 real/fake 集上 100% accuracy 不代表 population supports 分离。高容量 discriminator 可以记忆有限样本；generator 随后追逐样本特定边界。必须有 held-out real/fake classification、augmentation protocol 与 generalization gap。

## 七、科学空间与原论文

本节以[[S-2014-Goodfellow-GAN]]为定理来源，并为后续[[S-2018-Su-6016-fGAN与变分散度]]提供基准。科学空间的统一 variational 视角帮助看出 JS 只是特定 proper classification/Fenchel objective；但原始 GAN 的最优 $D$、常数与等号条件必须逐式独立复算。

## 八、图：推导中的三个世界

先看图回答：逐点 concave maximization、代回 JS、实际交替 SGD 分别位于哪一层？哪条等号不能跨层搬运？

![[00-知识库管理/_assets/figures/generative-models/fig-gan-optimal-discriminator-js-v1.svg|900]]

> [!figure] 图 50.3-02　最优判别器、JS value 与实际训练的责任边界
> 图左展示逐点最优，中央展示代回后的 divergence，右侧展示有限 critic iterate。来源：依据 Goodfellow et al. 2014 独立重绘。

**怎样读图**：只有从 $D^*$ 向 JS 的箭头是 theorem；从当前 $D_{\psi_t}$ 到 $D^*$ 需要函数表达、数据、优化和动态条件。

**图没有证明什么**：图不证明 neural GAN 实际最小化精确 JS，也不证明 $D\approx1/2$ 必为成功。

## 九、本节回顾

- 固定 $G$ 的 population best response 为 $p/(p+q)$；
- 代回 minimax value 得 $-\log4+2JS$；
- support 分离时 JS 饱和为 $\log2$；
- 理论使用共同支配测度即可，不要求 ambient density；
- best-response theorem 不等于有限交替训练的 gradient field。

## 十、练习与独立详解

- [[习题 - 原始 GAN、最优判别器与 Jensen–Shannon 散度]]
- [[解答 - 原始 GAN、最优判别器与 Jensen–Shannon 散度]]

