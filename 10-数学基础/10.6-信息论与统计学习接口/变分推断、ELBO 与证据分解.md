---
type: concept
status: draft
area: [math/information-theory, math/statistics, ai/generative-models, ai/probabilistic-modeling]
aliases: [变分推断, ELBO, Evidence Lower Bound, Variational Inference]
prerequisites: ["[[交叉熵与 KL 散度]]", "[[Bayesian 推断与后验预测]]", "[[Monte Carlo、重要性采样与方差缩减]]", "[[随机变量变换与密度换元]]"]
related: ["[[信息论与统计学习接口 MOC]]", "[[最大熵原理与指数族]]", "[[MCMC 与随机模拟诊断]]", "[[率失真、信息瓶颈与最小描述长度]]"]
sources: ["Blei-Kucukelbir-McAuliffe-2017-Variational-Inference", "Wainwright-Jordan-2008-Exponential-Families-Variational-Inference", "Kingma-Welling-2014-AEVB", "Rezende-Mohamed-Wierstra-2014-Stochastic-Backprop", "Burda-Grosse-Salakhutdinov-2016-IWAE", "Su-5253-VAE-I", "Su-5343-VAE-Bayesian", "Su-5383-VAE-Reparameterization", "Su-8791-VAE-Density"]
created: 2026-08-19
updated: 2026-08-27
---

# 变分推断、ELBO 与证据分解

> [!abstract] 本章主问题
> 对 latent-variable model $p_\theta(x,z)$ 和任意合法近似 $q(z)$，log evidence 有精确分解：$\log p_\theta(x)=\operatorname{ELBO}(q)+D_{\rm KL}(q(z)\|p_\theta(z\mid x))$。ELBO 是下界，因为 gap 是 nonnegative reverse KL；最大化 ELBO 同时近似 posterior 并学习 model parameters。真正的误差不只有“variational family 太简单”，还包括 optimization、amortization、Monte Carlo、model misspecification 与 evaluation gap。VAE 是 amortized stochastic VI 的一个实例，不是 ELBO 的定义本身。

## 学习目标

完成本节后，你应当能够：

1. 区分 joint、prior、likelihood、evidence、model posterior 与 variational distribution；
2. 用 Jensen 推导 ELBO lower bound；
3. 逐行证明 evidence = ELBO + posterior KL gap；
4. 解释为什么标准 VI 最小化 $D(q\|p)$ 而非 $D(p\|q)$；
5. 推导 mean-field coordinate update；
6. 写出 VAE reconstruction–KL decomposition；
7. 根据 likelihood 判断 MSE、BCE、categorical CE 的常数与尺度；
8. 推导 score-function 与 pathwise gradient estimator；
9. 区分 approximation、optimization 与 amortization gap；
10. 解释 posterior collapse、inactive latent 与 powerful decoder；
11. 判断 $\beta$-VAE、free bits、KL annealing 是否仍是标准 ELBO；
12. 推导 IWAE bound 并审计 importance-weight variance；
13. 连接 VI、EM、MCMC 与 predictive checking；
14. 审计 train ELBO、held-out likelihood estimate 与 sample quality 的边界。

> [!question] 初学者读完必须能回答
> 1. prior、likelihood、joint、evidence、model posterior 与 variational $q_\phi$ 分别由谁定义？
> 2. Jensen 推导 ELBO 需要怎样的 support 条件，等号何时成立？
> 3. 为什么 $\log p_\theta(x)=\operatorname{ELBO}+D_{\rm KL}(q\|p_\theta(z\mid x))$ 是恒等式而非近似？
> 4. 标准 VI 为什么出现 reverse KL $D(q\|p)$，它的方向与近似族会怎样影响解？
> 5. VAE 的 reconstruction 与 prior-KL 怎样由 ELBO 得到，observation likelihood 如何决定尺度和常数？
> 6. family、amortization、optimization 与 Monte Carlo gap/error 如何严格区分？
> 7. posterior collapse、$\beta$-VAE、IWAE 与 held-out evaluation 为什么不能只用 train ELBO 一个数判断？

## 阅读前检查

- [[Bayesian 推断与后验预测]]：joint、evidence、posterior 与 predictive；
- [[交叉熵与 KL 散度]]：KL 方向、支撑和 Gaussian closed form；
- [[Monte Carlo、重要性采样与方差缩减]]：importance weights、ESS 与 log-average bias；
- [[随机变量变换与密度换元]]：Gaussian reparameterization 与 normalizing flow；
- [[最大熵原理与指数族]]：variational optimization 与 exponential-family duality。

## 零、六个对象先固定

latent-variable model：

$$
p_\theta(x,z)=p_\theta(z)p_\theta(x\mid z).
$$

evidence/marginal likelihood：

$$
p_\theta(x)=\int p_\theta(x,z)dz.
$$

model posterior：

$$
p_\theta(z\mid x)=\frac{p_\theta(x,z)}{p_\theta(x)}.
$$

当 integral/sum 难算时，引入 tractable approximation：

$$
q_\phi(z\mid x).
$$

必须区分：

| 对象 | 谁定义它 | 常见可算性 |
|---|---|---|
| prior $p_\theta(z)$ | generative model | 常可采样/算 density |
| likelihood $p_\theta(x\mid z)$ | observation model/decoder | 常可算 conditional log density |
| joint $p_\theta(x,z)$ | 两者乘积 | 常可算到 normalization |
| evidence $p_\theta(x)$ | latent marginalization | 常难算 |
| posterior $p_\theta(z\mid x)$ | Bayes 唯一决定 | 因 evidence 难而难算 |
| $q_\phi(z\mid x)$ | inference design/network | 刻意选择为 tractable |

先用下图回答一个视觉问题：**model posterior、variational $q$、ELBO 与各种训练 gap 为什么必须保持为不同对象？**

![[00-知识库管理/_assets/figures/information-theory/fig-elbo-evidence-gap-v2.svg|880]]

> [!figure] 图 10.6.8a｜变分对象、证据分解与 gap 来源
> A 从 prior/likelihood 组成 joint，区分 model posterior 与人为设计的 $q_\phi$；B 将 log evidence 拆为 ELBO 与 $D_{\rm KL}(q\|p(z\mid x))$，并给出 reconstruction–prior-KL 形式；C 分开 family、amortization、optimization 与 Monte Carlo error。来源：独立绘制；生成脚本：[[plot_information_coding_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先固定生成模型 $p_\theta$，再问 posterior 是否难算以及 $q_\phi$ 如何被选；B 把 KL gap 当作精确恒等式的非负余项，不把 ELBO 直接叫 evidence；C 沿“可表示—逐例最优—参数优化—随机估计”四层检查误差来源。

**适用边界（图没有证明什么）。** 分块宽度不代表具体模型的数值比例；恒等式要求相应 density/support 与期望定义良好；gap 为零只表示 $q$ 匹配该假设模型的 posterior，不证明模型正确、预测校准或样本质量好。VAE、mean-field、IWAE 与 $\beta$-VAE 还各有额外结构。

> [!warning] encoder 不是“真实后验的另一个名字”
> $q_\phi$ 是近似对象。只有 gap 为零时，它才与 model posterior almost everywhere 相等；而 model posterior 本身也只相对于假设的 $p_\theta$，不等于自然界的绝对真相。

## 进入正文前：先在可枚举模型里亲手看见 ELBO gap

> [!info] 课程位置
> [[最大熵原理与指数族]]构造了 Bernoulli$(1/4)$ 先验。本章把其中一个 bit 当作不可见 latent variable $Z$，只观察它经过噪声后的 $X$。小模型的 evidence 与 posterior 都能精确枚举，因此可以把 ELBO、reverse-KL gap 和 variational-family 限制逐项校准；下一章[[f-散度、Bregman 散度与概率度量]]会继续比较同一 posterior 与近似分布，但不再假装所有差异量具有同一几何。

> [!tip] 建议两遍阅读
> - **第一遍：** 固定一个观测 $X=1$，先算 joint、evidence、posterior，再让 $q_r(Z)=\operatorname{Bernoulli}(r)$ 分别取 $r=1/4$ 与 $1/2$，核对 ELBO identity。
> - **第二遍：** 再读 Jensen 支撑条件、mean-field update、VAE likelihood、重参数化、family/amortization/optimization gap、posterior collapse 与 IWAE。

> [!question] 本章的推导问题链
> 1. prior、likelihood、joint、evidence、posterior 与 variational $q$ 分别由谁定义？
> 2. 为什么 evidence 的求和/积分会让 posterior 难算，而 joint 往往仍可评价？
> 3. 在 log evidence 中乘除 $q$ 后，Jensen 怎样产生 ELBO？
> 4. 为什么 evidence 与 ELBO 的差不是模糊误差，而是精确的 $D(q\Vert p(z\mid x))$？
> 5. variational family 包含真实 posterior、优化器找到它、Monte Carlo 精确这三件事为何必须分层？

### 贯穿算例：稀有潜变量经过四分之一翻转噪声

使用自然对数。生成模型为

$$
Z\sim\operatorname{Bernoulli}\!\left(\frac14\right),
\qquad
E\sim\operatorname{Bernoulli}\!\left(\frac14\right),
\qquad
X=Z\oplus E,
\qquad
E\perp Z.
$$

其中 $Z$ 是 latent bit，$X$ 是 observation。对观测 $X=1$，两条可能的 latent paths 为：

| $Z$ | prior $p(z)$ | likelihood $p(X=1\mid z)$ | joint $p(X=1,z)$ |
|---:|---:|---:|---:|
| $0$ | $3/4$ | $1/4$ | $3/16$ |
| $1$ | $1/4$ | $3/4$ | $3/16$ |

先边缘化 latent variable：

$$
p(X=1)=\frac3{16}+\frac3{16}=\frac38,
\qquad
\ln p(X=1)=\ln\frac38\approx-0.980829.
$$

再用 Bayes 归一化：

$$
p(Z=1\mid X=1)
=\frac{3/16}{3/8}
=\frac12.
$$

所以本次观测把 latent success probability 从 prior 的 $1/4$ 更新到了 posterior 的 $1/2$。

### 用一个 Bernoulli variational family 做精确校准

令

$$
q_r(Z)=\operatorname{Bernoulli}(r).
$$

对当前观测，ELBO identity 可以直接写成

$$
\boxed{
\mathcal L(r;X=1)
=\ln\frac38
-D_{\mathrm{KL}}
\left(\operatorname{Ber}(r)\middle\Vert\operatorname{Ber}\!\left(\frac12\right)\right).}
$$

先故意取 $q$ 等于 prior，即 $r=1/4$。此时 reconstruction–prior-KL 形式中的 prior KL 为零，而

$$
\begin{aligned}
\mathcal L\!\left(\frac14;X=1\right)
&=\frac14\ln\frac34+\frac34\ln\frac14\\
&\approx-1.111641.
\end{aligned}
$$

gap 是

$$
\begin{aligned}
D_{\mathrm{KL}}
\left(\operatorname{Ber}\!\left(\frac14\right)
\middle\Vert
\operatorname{Ber}\!\left(\frac12\right)\right)
&=\frac14\ln\frac12+\frac34\ln\frac32\\
&\approx0.130812.
\end{aligned}
$$

数值恰好闭合：

$$
-0.980829
=-1.111641+0.130812.
$$

若取 $r=1/2$，$q_r$ 正好等于 model posterior，KL gap 为零，ELBO 等于 log evidence。这个例子把三种情形分开：

- **family 能表示：** Bernoulli family 包含 $r=1/2$；
- **optimization 找得到：** 仍需算法真正把 $r$ 优化到 $1/2$；
- **amortization 做得到：** 若用共享网络 $r_\phi(x)$ 服务许多 $x$，它还需对每个输入输出正确参数。

> [!note] 符号与对象账本
> | 符号 | 类型 | 在本例中的角色 |
> |---|---|---|
> | $Z$ | latent random variable | 未直接观察的稀有状态 |
> | $X$ | observed random variable | latent bit 经过噪声后的观测 |
> | $p(z)$ | prior | 看见 $X$ 之前模型对 $Z$ 的分布 |
> | $p(x\mid z)$ | likelihood | 给定 latent state 后产生观测的机制 |
> | $p(x)$ | evidence | 对 $Z$ 边缘化后的观测概率 |
> | $p(z\mid x)$ | model posterior | 由同一个生成模型和 Bayes 唯一决定 |
> | $q_r(z)$ | variational distribution | 为可计算推断而人为选择的近似 |
> | $\mathcal L(r;x)$ | 标量下界 | joint log-density 减 variational log-density 的 $q$-expectation |

> [!analysis] Evidence–ELBO 恒等式的公式七问
> | 问题 | 回答 |
> |---|---|
> | 核心公式是什么？ | $\ln p_\theta(x)=\mathcal L(q,\theta;x)+D_{\mathrm{KL}}(q(z)\Vert p_\theta(z\mid x))$。 |
> | ELBO 怎样定义？ | $\mathcal L=\mathbb E_q[\ln p_\theta(x,z)-\ln q(z)]$。 |
> | 为什么是下界？ | 余项是 nonnegative reverse KL；等价地，也可由 log 的 Jensen inequality 推出。 |
> | 等号何时成立？ | $q(z)=p_\theta(z\mid x)$ almost everywhere，且相关支撑/期望定义良好。 |
> | 为什么方向是 $D(q\Vert p)$？ | 恒等式在 tractable $q$ 下取 expectation；posterior 出现在分母，代数展开自然得到 reverse KL。 |
> | gap 为零证明了什么？ | 只证明 $q$ 匹配当前假设模型的 posterior；不证明生成模型正确、预测可靠或样本质量好。 |
> | AI 中在哪里调用？ | VAE、mean-field VI、Bayesian neural approximation 与 latent-variable learning；每次都要另报 family、amortization、optimization 与 Monte Carlo error。 |

> [!analysis] Reconstruction–prior-KL 形式的公式七问
> | 问题 | 回答 |
> |---|---|
> | 核心公式是什么？ | $\mathcal L=\mathbb E_q\ln p_\theta(x\mid z)-D_{\mathrm{KL}}(q(z\mid x)\Vert p_\theta(z))$。 |
> | 第一项是什么？ | 模型 likelihood 的期望 log score；它由 Bernoulli、Gaussian、categorical 等 observation model 决定，不是无条件的 MSE。 |
> | 第二项是什么？ | 每个 observation 的 approximate posterior 到 prior 的 KL，方向和归约尺度不能省略。 |
> | 两项为何能相加？ | 把 joint 分解为 $p(z)p(x\mid z)$，再把 $\mathbb E_q[\ln p(z)-\ln q(z)]$ 识别为负 KL。 |
> | 本例 $q=prior$ 时发生什么？ | prior KL 为零，但 posterior gap 不为零；“正则项为零”不表示推断正确。 |
> | 修改系数会怎样？ | $\beta$-VAE、free bits 或 KL annealing 通常不再是原模型的标准 ELBO，必须重新命名目标。 |
> | 怎样验收实现？ | 枚举小模型核对 evidence；再分别检查 per-sample/batch reduction、support、随机估计方差与 held-out evaluation。 |

> [!success] 第一遍停靠线
> 若你能从两条 latent paths 得到 evidence $3/8$ 与 posterior $1/2$，再分别用 $r=1/4$ 和 $r=1/2$ 得到“有 gap/零 gap”两种 ELBO，并复算 $-0.980829=-1.111641+0.130812$，就已掌握第一遍主干。VAE、重参数化、IWAE 和四类 inference gap 留到第二遍。

## 一、Jensen 推导 ELBO

对任意 $q(z)$，要求在 $q(z)>0$ 处 $p_\theta(x,z)>0$，则

$$
\begin{aligned}
\log p_\theta(x)
&=\log\int p_\theta(x,z)dz\\
&=\log\int q(z)\frac{p_\theta(x,z)}{q(z)}dz\\
&=\log E_q\left[\frac{p_\theta(x,Z)}{q(Z)}\right]\\
&\ge E_q\log\frac{p_\theta(x,Z)}{q(Z)}.
\end{aligned}
$$

定义 evidence lower bound：

$$
\boxed{
\mathcal L(q,\theta;x)
=E_q[\log p_\theta(x,Z)-\log q(Z)].
}
$$

Jensen equality 当且仅当 importance ratio

$$
\frac{p_\theta(x,z)}{q(z)}
$$

在 $q$ 下为常数；归一化后等价于

$$
q(z)=p_\theta(z\mid x).
$$

## 二、证据分解：lower bound 的精确 gap

从 posterior KL 展开：

$$
\begin{aligned}
D(q(z)\|p_\theta(z\mid x))
&=E_q\log\frac{q(z)}{p_\theta(z\mid x)}\\
&=E_q\log\frac{q(z)p_\theta(x)}{p_\theta(x,z)}\\
&=\log p_\theta(x)
-E_q\log\frac{p_\theta(x,z)}{q(z)}.
\end{aligned}
$$

所以

$$
\boxed{
\log p_\theta(x)
=\mathcal L(q,\theta;x)
+D(q(z)\|p_\theta(z\mid x)).
}
$$

由于 KL 非负：

$$
\mathcal L\le\log p_\theta(x).
$$

这比“由 Jensen 所以是下界”更有信息：gap 恰是 approximate posterior 到 model posterior 的 reverse KL。

### 2.1 support 边界

若 $q(z)>0$ 但 $p_\theta(x,z)=0$，则 ELBO 含 $\log0=-\infty$，KL gap 为 $+\infty$。若 posterior 有某些 mode 而 $q$ 对其给零质量，reverse KL 不直接惩罚那些 $q$ 从不访问的区域；这解释了常说的 mode-seeking tendency，但具体结果仍依 variational family 与 optimization。

## 三、ELBO 的 reconstruction–regularization 形式

用 joint factorization：

$$
\begin{aligned}
\mathcal L
&=E_q[\log p_\theta(x\mid z)]
+E_q[\log p_\theta(z)-\log q(z)]\\
&=\boxed{
E_q\log p_\theta(x\mid z)
-D(q(z)\|p_\theta(z)).
}
\end{aligned}
$$

第一项是 expected conditional log-likelihood，不是无条件“像素重构误差”；第二项把每个 observation 的 approximate posterior 与 prior 比较。

若 $q=q_\phi(z\mid x)$：

$$
\mathcal L_{\theta,\phi}(x)
=E_{q_\phi(z\mid x)}\log p_\theta(x\mid z)
-D(q_\phi(z\mid x)\|p_\theta(z)).
$$

## 四、为什么 VI 优化 reverse KL

固定 $p_\theta$ 与 observation $x$：

$$
\arg\max_{q\in\mathcal Q}\mathcal L(q)
=\arg\min_{q\in\mathcal Q}D(q\|p_\theta(z\mid x)).
$$

标准 VI 使用 reverse KL 不是任意偏好，而是 evidence identity 直接给出。forward KL

$$
D(p_\theta(z\mid x)\|q(z))
$$

的 expectation 在难采样/难归一化的 posterior 下，通常不可直接算。

reverse-KL 的零避让倾向：在 multimodal posterior 和 unimodal $q$ 下，覆盖两个 mode 中间的低 posterior density 会受到高代价，优化可能选择一个 mode。它不是“不确定性必然低估”的无条件定理；heavy tail、family shape、local optimum 与 parameterization 都会改变行为。

## 五、mean-field coordinate ascent

设

$$
q(z)=\prod_{j=1}^mq_j(z_j).
$$

固定 $q_{-j}$，只优化 $q_j$。ELBO 中与 $q_j$ 相关部分：

$$
\int q_j(z_j)
E_{q_{-j}}[\log p_\theta(x,z)]dz_j
-\int q_j(z_j)\log q_j(z_j)dz_j.
$$

加 normalization multiplier，functional derivative 为零：

$$
\boxed{
\log q_j^*(z_j)
=E_{q_{-j}}[\log p_\theta(x,z)]+\text{const}.
}
$$

或

$$
q_j^*(z_j)\propto
\exp\{E_{q_{-j}}\log p_\theta(x,z)\}.
$$

在 conditionally conjugate exponential-family model 中，这常保留已知 distribution form；非共轭/深度模型则需要 stochastic gradient、bounds 或 black-box VI。

> [!warning] coordinate optimum 不等于 global posterior
> 每步在单个 factor 上最优并使 ELBO 不降，但 ELBO 对所有 factors/parameters 通常不 jointly concave，可收敛到 local stationary point。

## 六、VAE：amortized VI 的标准实例

VAE 令

$$
p(z)=N(0,I),
$$

decoder likelihood 为 $p_\theta(x\mid z)$，encoder 输出

$$
q_\phi(z\mid x)
=N(\mu_\phi(x),\operatorname{diag}\sigma_\phi^2(x)).
$$

对 dataset $\{x_i\}_{i=1}^n$ 最大化

$$
\sum_{i=1}^n\mathcal L_{\theta,\phi}(x_i).
$$

同一 inference network $\phi$ 为每个 $x$ 立即输出 variational parameters，称为 amortization：用一次训练成本换取新样本上的快速 inference。

### 6.1 diagonal Gaussian KL

若 $q=N(\mu,\operatorname{diag}\sigma^2)$、$p=N(0,I)$，则

$$
\boxed{
D(q\|p)
=\frac12\sum_{j=1}^d
(\mu_j^2+\sigma_j^2-1-\log\sigma_j^2).
}
$$

实现常让 network 输出 $\ell_j=\log\sigma_j^2$：

$$
D(q\|p)
=\frac12\sum_j(\mu_j^2+e^{\ell_j}-1-\ell_j).
$$

要说明 reduction：per-example sum over latent dimensions 后，再对 batch mean/sum。

## 七、reconstruction loss 由 likelihood 决定

### 7.1 Gaussian likelihood

若

$$
p_\theta(x\mid z)=N(f_\theta(z),\sigma_x^2I),
$$

则

$$
-\log p_\theta(x\mid z)
=\frac{1}{2\sigma_x^2}\|x-f_\theta(z)\|^2
+\frac d2\log(2\pi\sigma_x^2).
$$

所以 MSE 只是固定 variance Gaussian NLL 去掉常数后的形式。改变 pixel reduction 或 $\sigma_x^2$ 就改变 reconstruction 与 KL 的相对尺度。

### 7.2 Bernoulli/categorical likelihood

binary data 可用 Bernoulli NLL/BCE；categorical token 用 conditional cross-entropy。对连续灰度像素直接套 Bernoulli 是建模近似，不是由 ELBO 自动推出。

### 7.3 learned variance

若 decoder 同时学 variance，必须保留 log-variance normalization term；只优化 residual/variance ratio 会让 variance 无约束增大。

## 八、Monte Carlo 与梯度估计

ELBO expectation 常用 samples 近似：

$$
\widehat{E_qf(Z)}=\frac1L\sum_{\ell=1}^Lf(z^{(\ell)}).
$$

### 8.1 score-function estimator

若 $f$ 不显式依赖 $\phi$：

$$
\nabla_\phi E_{q_\phi}f(Z)
=E_{q_\phi}[f(Z)\nabla_\phi\log q_\phi(Z)].
$$

它适用于 discrete/continuous distributions，但 variance 常高。减 baseline $b$ 不改 expectation：

$$
E[(f-b)\nabla\log q]=E[f\nabla\log q],
$$

因为 $E_q\nabla\log q=0$。

### 8.2 pathwise/reparameterization estimator

若

$$
Z=g_\phi(\varepsilon),
\qquad \varepsilon\sim s(\varepsilon)
$$

且 base law 不依赖 $\phi$：

$$
\nabla_\phi E_{q_\phi}f(Z)
=E_{s}\nabla_\phi f(g_\phi(\varepsilon)).
$$

Gaussian：

$$
z=\mu_\phi(x)+\sigma_\phi(x)\odot\varepsilon,
\qquad\varepsilon\sim N(0,I).
$$

微分移入 expectation 仍需 dominated convergence/regularity；“计算图能反传”不是数学条件的替代。

### 8.3 discrete latent

Gumbel–Softmax/Concrete 用 continuous relaxation，通常优化有 bias 的 relaxed objective；REINFORCE/score function 可无偏但高 variance。必须报告 temperature、straight-through 与 train/eval discrete mismatch。

## 九、inference gap 的三层拆分

令 $q_x^*$ 是对单个 $x$ 在 family $\mathcal Q$ 内的最优 distribution：

$$
q_x^*=\arg\max_{q\in\mathcal Q}\mathcal L(q;x).
$$

对 amortized output $q_\phi(\cdot\mid x)$：

$$
\begin{aligned}
\log p_\theta(x)-\mathcal L(q_\phi;x)
&=\underbrace{\log p_\theta(x)-\mathcal L(q_x^*;x)}_{\text{approximation gap}}\\
&\quad+\underbrace{\mathcal L(q_x^*;x)-\mathcal L(q_\phi;x)}_{\text{amortization + optimization gap}}.
\end{aligned}
$$

进一步可通过 per-example refinement 区分：

- family gap：即使个体最优化也无法表示 posterior；
- amortization gap：shared network mapping 不等于每个个体 optimum；
- optimization gap：训练尚未达到 parameterized objective optimum；
- Monte Carlo error：gradient/objective estimation noise。

再用实验图回答一个可复现问题：**当 exact posterior 可表示、被 family 排除、或 shared encoder 看不到 $x$ 时，gap 分别怎样出现？**

![[00-知识库管理/_assets/plots/information-theory/plot-elbo-gap-v2.svg|880]]

> [!figure] 图 10.6.8b｜二元 latent model 的 ELBO identity、family gap 与 amortization gap
> A 枚举 Bernoulli $q$，在 exact posterior $q^*=0.6585$ 处 ELBO 接触 log evidence；B 强制 $q\ge0.8$ 后最优点落在边界并留下 $0.0487$ nats approximation gap；C 强制 $x=0,1$ 共用同一 $q$，最优 shared $q=0.2432$ 仍留下平均 $0.2846$ nats gap。来源：合成二元模型精确枚举；生成脚本：[[plot_elbo_gap.py]]；无随机种子。

**怎样读图。** A 比较蓝色 ELBO 曲线与绿色 evidence 水平线的竖直差；B 只在允许的 $q\ge0.8$ 区间寻找最大值；C 将两个 per-example posterior target 与同一个 shared output 放在同一轴上，区分 representational/amortized restriction。

**适用边界（图没有证明什么）。** 这是可枚举 Bernoulli latent 教学模型，只验证当前模型中的恒等式与两种人为限制；它不量化 neural VAE 的全部 gap，不证明 reverse KL 总会选某一类 mode，也不把 train ELBO、真实数据 fit、held-out likelihood 或生成质量等同起来。

实验入口：[[实验 - ELBO 恒等式、变分族限制与摊销缺口]]。

## 十、posterior collapse 不是“KL 算错了”

若 powerful decoder 无需 $z$ 也能建模 $x$，可能出现

$$
q_\phi(z\mid x)\approx p(z),
$$

于是

$$
D(q_\phi(z\mid x)\|p(z))\approx0,
$$

latent 与 input 几乎无信息。此时 ELBO 可能仍好，因为 decoder 直接建模数据。

诊断应包括：

- per-dimension KL/active units；
- $I_q(X;Z)$ 或 aggregate-posterior diagnostics（注明 estimator）；
- reconstruction under latent permutation/ablation；
- prior vs posterior samples；
- decoder capacity、teacher forcing 和 KL schedule。

posterior collapse 是 model/objective/optimization 的 equilibrium，不是单凭把 KL weight 调小就一定解决。

## 十一、修改 ELBO 时必须重新命名

### 11.1 $\beta$-VAE

$$
\mathcal L_\beta
=E_q\log p_\theta(x\mid z)-\beta D(q\|p).
$$

- $\beta=1$：标准 ELBO；
- $\beta>1$：数值上不高于标准 ELBO，因此仍低于 evidence，但优化的是更强 compression 的 modified bound/objective；
- $0<\beta<1$：不保证仍是 evidence lower bound。

它可改变 rate–distortion trade-off，但 disentanglement 还依数据生成因素、inductive bias 与 evaluation。

### 11.2 free bits / KL floor

对每组 latent 的 KL 使用 threshold 会改变 gradient/objective；它是训练 heuristic，不再等于 canonical evidence decomposition。

### 11.3 KL annealing

训练早期改变 KL weight 是 optimization schedule。最终若回到 $\beta=1$，target 最终仍可为 ELBO；训练路径本身不等于始终优化同一个 bound。

## 十二、IWAE：更紧 bound 与更难权重问题

采样 $z_1,\ldots,z_K\sim q(z\mid x)$，importance weights

$$
w_k=\frac{p_\theta(x,z_k)}{q(z_k\mid x)}.
$$

定义

$$
\boxed{
\mathcal L_K
=E\log\left(\frac1K\sum_{k=1}^Kw_k\right).
}
$$

$K=1$ 是 ELBO；在标准条件下

$$
\mathcal L_1\le\mathcal L_2\le\cdots\le\log p_\theta(x).
$$

但：

- log of sample average 对 evidence 的 finite-$K$ estimate 有 Jensen bias；
- importance weight variance/ESS 可能极差；
- 更紧 bound 不保证 encoder gradient signal 单调更好；
- train objective 与 held-out log-likelihood estimator 要分开；
- samples 之间的依赖与 numerical logsumexp 必须审计。

## 十三、VI 与 EM、MCMC 的关系

### 13.1 EM

EM auxiliary decomposition 对任意 $q(z)$：

$$
\log p_\theta(x)=\mathcal L(q,\theta;x)+D(q\|p_\theta(z\mid x)).
$$

E-step 取当前参数的 exact posterior，使 gap 为零；M-step 固定 $q$ 增大 expected complete-data log-likelihood。VI/variational EM 用 restricted $q$ 近似 E-step；amortized VI 再用 shared network 预测 $q$。

### 13.2 MCMC

MCMC 以 asymptotically exact sampling 为目标，但有 mixing、warmup、ESS 与 multimodality 风险；VI 把 inference 变优化，通常快但有 family/objective bias。二者可结合：MCMC refine variational initialization，VI 作 proposal/control variate，或用 simulation-based calibration 检查 inference pipeline。

## 十四、ELBO 不是所有评价指标

train ELBO 上升只说明当前 stochastic objective 改善。不能直接推出：

- true data log-likelihood 提升；
- held-out evidence 提升；
- posterior calibration 改善；
- perceptual sample quality 提升；
- latent factors 可解释；
- OOD detection 可靠。

合理报告至少分开：

1. train/validation ELBO，说明 samples/reduction；
2. tighter held-out importance estimate 与 ESS/weight diagnostics；
3. posterior predictive checks；
4. reconstruction、prior samples 和 conditional samples；
5. latent usage/collapse；
6. inference refinement gap；
7. model/data misspecification 与 distribution shift。

## 十五、常见错误与纠正

| 错误 | 为什么错 | 纠正 |
|---|---|---|
| ELBO 是 log evidence 的近似等号 | gap 可能很大 | 同时报 KL/gap proxy 与 tighter estimate |
| encoder 就是 posterior | 它是 $q_\phi$ approximation | 保留 model posterior 与 variational posterior 名称 |
| reconstruction loss 随便选 | 它对应 likelihood | 从 data type/noise model 推导 |
| reverse KL 总覆盖所有 mode | reverse KL 常有 zero-avoiding 行为 | 检查 family 与 multimodal examples |
| 一次 sample 就“精确积分” | 只是 stochastic estimate | 报 variance、seed、sample count |
| KL=0 代表完美 latent | 也可能 collapse | 检查 task/representation information |
| $\beta$-VAE 都是标准 ELBO | $\beta\ne1$ 改变 decomposition | 按 modified objective 命名 |
| 更紧 IWAE bound 必然样本更好 | optimization/inference signal 可变化 | 分开 bound、gradient 与 generation |

## 十六、推导与实现审计清单

1. $p_\theta(x,z)$ 的 factorization 是什么？
2. $q_\phi$ 近似哪个 posterior？
3. support 是否满足 $q>0\Rightarrow p(x,z)>0$？
4. ELBO 用 sum、mean 还是 per-dimension reduction？
5. reconstruction 对应什么 normalized likelihood？
6. Gaussian variance 固定还是学习，常数是否保留？
7. KL 是 analytic 还是 Monte Carlo，方向是什么？
8. gradient 是 score-function 还是 pathwise，bias/variance 如何？
9. family、amortization、optimization gap 是否区分？
10. latent collapse 是否按维度与数据子群诊断？
11. objective 是否被 $\beta$/free bits/annealing 修改？
12. held-out evidence 用什么 estimator，importance ESS 如何？
13. train/test 是否共享 inference tuning？
14. predictive checks、calibration 与 distribution shift 是否评估？

## 十七、你现在应能独立重建的主链

$$
\log p_\theta(x)
=\log E_q\frac{p_\theta(x,Z)}{q(Z)}
\ge E_q\log\frac{p_\theta(x,Z)}{q(Z)}.
$$

更精确地：

$$
\boxed{
\log p_\theta(x)
=\underbrace{E_q\log p_\theta(x\mid Z)-D(q\|p_\theta(z))}_{\rm ELBO}
+\underbrace{D(q\|p_\theta(z\mid x))}_{\rm gap}.
}
$$

下一章将把 KL 放进更大的地图：$f$-divergence、Bregman geometry 与 IPM/optimal transport 对 support、geometry、topology 和 sample estimation 有完全不同的敏感性。

## 习题与解答

- [[习题 - 变分推断、ELBO 与证据分解]]：15 道 A–E 分层训练；
- [[解答 - 变分推断、ELBO 与证据分解]]：identity、mean-field、VAE、gradient、gap 与评估审计。

## 参考来源

- Blei, Kucukelbir & McAuliffe, [Variational Inference: A Review for Statisticians](https://arxiv.org/abs/1601.00670)；
- Wainwright & Jordan, [Graphical Models, Exponential Families, and Variational Inference](https://statistics.berkeley.edu/tech-reports/649)；
- Kingma & Welling, [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)；
- Rezende, Mohamed & Wierstra, *Stochastic Backpropagation and Approximate Inference in Deep Generative Models*；
- Burda, Grosse & Salakhutdinov, *Importance Weighted Autoencoders*；
- [[S-2018-Su-5253-变分自编码器一]]；
- [[S-2018-Su-5343-VAE从贝叶斯观点出发]]；
- [[S-2018-Su-5383-变分自编码器三]]；
- [[S-2021-Su-8791-VAE估计样本概率密度]]。
