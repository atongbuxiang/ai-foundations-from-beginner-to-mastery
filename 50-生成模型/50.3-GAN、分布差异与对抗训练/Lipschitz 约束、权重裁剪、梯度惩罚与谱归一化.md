---
type: concept
status: verified
area: [generative-models, gan, lipschitz]
node_id: GEN-21
prerequisites: ["[[IPM、Wasserstein-1 与 Kantorovich 对偶]]", "[[矩阵范数]]"]
related: ["[[Minimax 动力学、旋转、阻尼与局部收敛]]", "[[Jacobian、Gradient Penalty 与 Lipschitz 正则接口]]"]
sources: ["[[S-2018-Su-6051-Lipschitz约束]]", "[[S-2017-Gulrajani-WGAN-GP]]", "[[S-2018-Miyato-Spectral-Normalization]]", "[[S-2021-Su-8244-WGAN成功与距离近似]]"]
exercises: ["[[习题 - Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]]"]
solutions: ["[[解答 - Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-gan-lipschitz-enforcement-layers-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化

> [!abstract] 本节主问题
> KR dual 要求 critic 全域 1-Lipschitz。权重裁剪、gradient penalty、R1 与 spectral normalization 都会限制或正则 critic，却不以相同方式实现该函数类。必须区分全局性质、网络上界、采样点 penalty 与优化诱导偏置。

## 一、定义与微分充分条件

$f$ 是 $K$-Lipschitz 若

$$
|f(x)-f(y)|\le K\|x-y\|\quad\forall x,y.
$$

在凸域内，若 $f$ 可微且 $\|\nabla f(x)\|_*\le K$ 对所有 $x$，由线段积分得 Lipschitz。反向由 Rademacher 定理在适当条件下几乎处处成立。只在有限点检查梯度不等于全域条件。

## 二、层谱范数上界

对网络

$$
f=W_L\sigma_{L-1}\cdots\sigma_1W_1x
$$

若激活分别 $k_\ell$-Lipschitz：

$$
\operatorname{Lip}(f)\le
\|W_L\|_{op}\prod_{\ell=1}^{L-1}
k_\ell\|W_\ell\|_{op}.
$$

这是 sufficient upper bound，可能很松。每层 spectral normalization 把估计的 $\|W_\ell\|_{op}$ 归一，但 convolution、residual addition、attention 与 power-iteration error 都需具体处理。

## 三、权重裁剪

WGAN 原始实现把参数 clip 到 $[-c,c]$。它令参数集 compact，并间接限制函数斜率，却：

- 不精确投影到 1-Lipschitz functions；
- 容易容量不足或参数在边界堆积；
- Lipschitz 常数依赖深度、宽度与架构；
- 改变 optimization geometry。

## 四、WGAN-GP

对插值

$$
\hat x=\epsilon x+(1-\epsilon)\tilde x,\quad\epsilon\sim U[0,1],
$$

加入

$$
\lambda E_{\hat x}
(\|\nabla_{\hat x}f_\psi(\hat x)\|_2-1)^2.
$$

它在采样的 real–fake chords 上鼓励 norm 接近 1。它不是：

- 全域 gradient bound；
- 所有方向 directional derivative 的逐一证书；
- 任何 network 的精确 KR projection；
- 与 R1 相同的 regularizer。

## 五、R1/R2 与 target norm

R1 常在 real samples 惩罚

$$
\frac\gamma2E_{P_*}\|\nabla_x f_\psi(x)\|^2,
$$

target 是 0，不是 1；目标是局部 game stability/regularization，而非直接复制 WGAN potential 性质。R2 类似作用于 fake。看到“gradient penalty”必须问取样分布、对象、target 与 one/two-sided。

## 六、谱归一化

令 $\bar W=W/\widehat\sigma_{\max}(W)$。它每步对层 operator norm 给可重复控制，不依赖输入 sample；但完整 network Lipschitz 还含：

- activation；
- residual path 的和；
- normalization 层与 data-dependent statistics；
- convolution operator 真谱范数；
- power iteration 近似误差。

SN 也是 optimizer reparameterization，成功可能来自 conditioning 和容量控制，不仅是满足 KR dual。

## 七、科学空间研读框

[[S-2018-Su-6051-Lipschitz约束]]提供权重/谱范数与网络 Lipschitz 的中文入口；[[S-2021-Su-8244-WGAN成功与距离近似]]提醒 regularization benefit 与 metric approximation 分账。本节再以[[S-2017-Gulrajani-WGAN-GP]]、[[S-2018-Miyato-Spectral-Normalization]]对齐具体 penalty 和 reparameterization。

## 八、图：四种约束到底约束哪里

先看图回答：全域函数类、层矩阵、插值点与 real-data 邻域分别是哪种方法的对象？哪些是证书，哪些只是经验 penalty？

![[00-知识库管理/_assets/figures/generative-models/fig-gan-lipschitz-enforcement-layers-v1.svg|900]]

> [!figure] 图 50.3-05　Lipschitz 理论条件与四种 enforcement 层级
> 图以全域函数性质为顶层，对照 weight clipping、GP、R1 与 SN 的实际作用域。来源：依据 KR dual、WGAN-GP 与 spectral normalization 独立绘制。

**怎样读图**：沿“参数/采样点→网络函数→全域类”向上看还缺哪些保证。GP 与 R1 的 target 和 sampling distribution 不同。

**图没有证明什么**：图不排名方法，也不证明 SN/GP 下 critic 恰为 1-Lipschitz 或 GAN 必收敛。

## 九、本节回顾

- 全域 Lipschitz 是任意点对的函数性质；
- layer spectral products 是上界，不一定紧；
- clipping 是参数约束，GP 是 sampled chord penalty，R1 是 zero-centered local penalty；
- SN 给层级 operator control，完整架构仍需组合；
- regularization 改善训练不等于精确估计 $W_1$。

## 十、练习与独立详解

- [[习题 - Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]]
- [[解答 - Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]]
