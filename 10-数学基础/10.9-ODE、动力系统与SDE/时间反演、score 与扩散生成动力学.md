---
type: concept
status: draft
area: [math/probability, math/stochastic-processes, math/sde, ai/generative-modeling]
aliases: [reverse-time SDE, score-based diffusion, 扩散生成模型, 反向扩散]
prerequisites: ["[[Fokker-Planck 方程与概率流 ODE]]", "[[Itô 引理与随机微分方程]]", "[[随机过程、Brownian 运动与二次变差]]", "[[条件概率、全概率与 Bayes 公式]]", "[[交叉熵与 KL 散度]]", "[[最大似然估计与 MAP]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[实验 - 反向时间、score恒等式与扩散采样误差审计]]", "[[S-2022-Su-9209-扩散模型SDE篇]]", "[[S-2022-Su-9228-概率流ODE]]", "[[S-2022-Su-9262-统一扩散模型理论篇]]"]
sources: ["Anderson-1982-Reverse-Time-Diffusion", "Hyvarinen-2005-Score-Matching", "Vincent-2011-Denoising-Score", "Sohl-Dickstein-et-al-2015-Diffusion", "Ho-et-al-2020-DDPM", "Song-Meng-Ermon-2021-DDIM", "Song-et-al-2021-Score-SDE", "Nichol-Dhariwal-2021-Improved-DDPM", "Karras-et-al-2022-EDM", "Su-9209-Diffusion-SDE", "Su-9228-Probability-Flow-ODE", "Su-9262-Unified-Diffusion-Theory", "Su-9280-Diffusion-ODE"]
created: 2026-08-19
updated: 2026-08-23
---

# 时间反演、score 与扩散生成动力学

> [!abstract] 本章主问题
> 前向扩散把复杂数据逐渐变成简单噪声；真正困难的是反向条件分布。若
> $$
> dX_t=f(t,X_t)dt+B(t,X_t)dW_t,
> \qquad D=BB^\top,
> $$
> 且密度与系数满足时间反演定理所需条件，定义正向反时钟
> $$
> Y_s=X_{T-s},\qquad 0\le s\le T,
> $$
> 则其反向漂移为
> $$
> b_{\rm rev}(s,x)
> =-f(T-s,x)
> +\frac1{p_{T-s}(x)}\nabla\cdot\!\left(D(T-s,x)p_{T-s}(x)\right).
> $$
> 当 $D=g(t)^2I$ 与空间无关时，
> $$
> b_{\rm rev}=-f+g^2\nabla_x\log p_t.
> $$
> 因而扩散生成的统计核心，是学习各噪声时刻的 score
> $$
> s_t(x)=\nabla_x\log p_t(x),
> $$
> 再用反向 SDE 或 probability-flow ODE 将近似终端先验搬回数据分布。定理中的精确 score、神经网络近似、有限步求解器和最终样本是四个不同对象。

> [!important] 本章是 10.9 的收官，不是工程配方大全
> 本章严格闭合“forward SDE → density → reverse dynamics → score training → finite-step generation”的基础链。网络架构、latent diffusion、蒸馏、专用高阶采样器和大规模训练系统只建立接口，不以经验技巧替代理论条件。

先用下图回答一个视觉问题：**Forward noising、reverse-time score correction 与 finite-step generation 怎样连接，reverse SDE 和 probability-flow ODE 为什么不能混用系数？**

![[00-知识库管理/_assets/figures/dynamics/fig-reverse-time-score-diffusion-v2.svg|880]]

> [!figure] 图 10.9.12｜Forward noising、反向 score 漂移与五道误差门
> A 从 $p_0=p_{\rm data}$ 经已知 forward SDE 搬到近似 prior $p_T$，将 terminal approximation 单列为误差；B 先定义 $s_t=\nabla\log p_t$，再区分 reverse SDE 的 full $g^2s_t$ correction 与 probability-flow ODE reverse clock 的 half $\frac12g^2s_t$，并提醒一般 $D$ 的 divergence correction 和 reverse filtration；C 串联 terminal prior、score model、guidance/parameterization、finite-step sampler 与 Monte Carlo/evaluation 五道门。来源：独立绘制；理论接口参考 reverse-time diffusion、score matching 与 score-SDE/PF-ODE theory；生成脚本：[[plot_stochastic_dynamics_v2.py]]；确定性误差地图，无随机种子。

**怎样读图。** A 先把 forward conditional law 与 terminal prior design 固定，不能只画“数据变噪声”的插图；B 再在明确的反向时钟 $s=T-t$ 下写 drift，full/half score coefficient 分别属于 reverse SDE/PF ODE，不能从“$dt<0$”直觉猜符号；C 最后逐门验收，减小 sampler step 只能减少 solver bias，不能消除 terminal、score 或 guidance bias。

**适用边界（图没有证明什么）。** 图主要显示 spatially constant isotropic diffusion 的简式；state-dependent/degenerate $D$、density zeros 和 boundary conditions 需使用一般时间反演定理。Exact reverse theorem 假设 exact score 与足够 regularity，不等于 neural approximation 或有限数据训练保证。样本指标、likelihood 与 perceptual quality 也不是同一验收量。

## 学习目标

完成本章后，应能：

1. 区分物理时间 $t$、反向时钟 $s=T-t$ 与“$dt<0$”记法；
2. 用小时间 Bayes 条件均值解释反向漂移为何出现 score；
3. 从 probability current 推导一般 state-dependent diffusion 的反向漂移；
4. 陈述反向时间定理需要的 positivity、regularity 与 nondegeneracy 边界；
5. 解释反向 SDE 中是完整 $D\nabla\log p$，概率流 ODE 中是半个；
6. 解出 variance-preserving SDE 的 conditional Gaussian law；
7. 区分 VP、VE 的漂移、噪声尺度和终端先验设计；
8. 从 Fisher divergence 推导 Hyvärinen score matching 目标；
9. 证明 denoising score matching 的 conditional-to-marginal 恒等式；
10. 推导 Gaussian corruption 下的 Tweedie posterior-mean 公式；
11. 在 score、$\varepsilon$、$x_0$ 与 $v$ 参数化之间正确换算；
12. 推导 DDPM 的 $q(x_k\mid x_0)$ 与 $q(x_{k-1}\mid x_k,x_0)$；
13. 说明 simplified noise loss 与 ELBO 的联系和差别；
14. 区分 ancestral DDPM、DDIM、reverse SDE、predictor–corrector 与 PF ODE；
15. 将 terminal、score、guidance、solver、Monte Carlo 与 evaluation error 分账。

> [!question] 初学者读完必须能回答
> 1. Forward noising 的设计对象是 conditional law、marginals 还是 sample path？
> 2. 反向时钟 $s=T-t$ 与简单写“$dt<0$”有何区别？
> 3. 为什么 reverse drift 必须出现 score $\nabla\log p_t$？
> 4. Reverse SDE 的 full score coefficient 与 PF ODE 的 half coefficient为何不同？
> 5. State-dependent diffusion 还需要哪个 $\nabla\cdot D$ correction？
> 6. DSM 的 conditional score 为什么能在期望上恢复 marginal score？
> 7. Terminal、score、guidance、solver 与 Monte Carlo/evaluation error 怎样分账？

## 零、生成问题究竟是什么

设真实数据分布为 $p_{\rm data}=p_0$。我们只有样本

$$
x_0^{(1)},\ldots,x_0^{(n)}\sim p_0,
$$

却希望构造一个能产生新样本的过程。

扩散模型把困难拆成两半：

$$
\boxed{
p_0\xrightarrow{\text{已知 forward noising}}p_T\approx\pi
}
$$

与

$$
\boxed{
\pi\xrightarrow{\text{learned reverse dynamics}}\widehat p_0.
}
$$

其中 $\pi$ 通常取容易采样的标准 Gaussian。

前向部分由我们设计，不需要学习；反向部分依赖未知的中间密度 $p_t$，这正是 score 出现的位置。

### 0.1 七个必须分开的对象

| 对象 | 记号 | 是否精确已知 | 作用 |
|---|---|---:|---|
| 数据分布 | $p_0$ | 只有样本 | 生成目标 |
| 前向转移 | $q_{t\mid0}(x_t\mid x_0)$ | 通常已知 | 制造训练对 |
| 中间边缘 | $p_t$ | 通常未知 | score 的真实目标 |
| population score | $\nabla\log p_t$ | 通常未知 | 精确反向动力学 |
| learned score | $s_\theta(x,t)$ | 训练近似 | 模型误差来源 |
| continuous reverse model | SDE 或 ODE | 给定 $s_\theta$ 后定义 | 理想部署动力学 |
| finite-step sampler | 数值数组 | 可执行 | 真正产生样本 |

> [!warning] 常见偷换
> “前向条件 Gaussian 可采样”不等于“中间边缘密度已知”；“训练 loss 很小”不等于“反向 SDE 精确”；“连续模型正确”也不等于“十步采样器正确”。

## 一、时间反演前先固定时钟

### 1.1 前向物理时间

考虑 $t\in[0,T]$ 上的 Itô SDE：

$$
dX_t=f(t,X_t)dt+B(t,X_t)dW_t.
$$

令

$$
D(t,x)=B(t,x)B(t,x)^\top.
$$

前向方向是

$$
t:0\longrightarrow T,
\qquad
p_0\longrightarrow p_T.
$$

### 1.2 反向时钟

定义新过程

$$
Y_s=X_{T-s},
\qquad s\in[0,T].
$$

此时 $s$ 仍然正常递增：

$$
s:0\longrightarrow T,
\qquad
Y_0\sim p_T,
\qquad
Y_T\sim p_0.
$$

这是最不容易出符号错误的记法。

记

$$
q_s(x)=p_{T-s}(x).
$$

所有反向 drift 中的 $p_t$，都应在

$$
t=T-s
$$

处求值。

### 1.3 为什么不能只说“把 $dt$ 改成负数”

Brownian increment 的方差按时间长度缩放：

$$
\operatorname{Var}(W_{t+h}-W_t)=|h|.
$$

反向过程使用相对于反向 filtration 的 Brownian motion $\bar W_s$。它不是把原前向 Brownian path 的数组倒序后，就继续使用同一个 adaptedness 论证。

有些论文沿用物理时间 $t$ 并写

$$
dX_t
=\left[f(t,X_t)-\nabla\cdot D(t,X_t)-D(t,X_t)\nabla\log p_t(X_t)\right]dt
+B(t,X_t)d\bar W_t,
$$

同时声明积分从 $T$ 到 $0$、即 $dt<0$。这个写法与 forward-$s$ 形式等价，但两个符号系统不可混算。

## 二、小时间 Bayes：score 为什么必然出现

先看最简单的 additive Brownian noising：

$$
dX_t=\sigma dW_t.
$$

在小时间 $h>0$ 内，前向核为

$$
q_h(x\mid y)
=\frac1{(2\pi\sigma^2h)^{d/2}}
\exp\left(-\frac{\|x-y\|^2}{2\sigma^2h}\right).
$$

但生成时需要的是 backward conditional：

$$
\mathbb P(X_{t-h}\in dy\mid X_t=x).
$$

由 Bayes 公式，

$$
r_h(y\mid x)
=\frac{q_h(x\mid y)p_{t-h}(y)}{p_t(x)}.
$$

前向 Gaussian 核只偏好 $y$ 接近 $x$；$p_{t-h}(y)$ 则告诉我们在这些邻近候选中，哪些方向更可能来自数据分布。

对 $y=x+\delta$ 展开：

$$
\log p_{t-h}(x+\delta)
=\log p_t(x)
+\nabla\log p_t(x)^\top\delta
+O(h+\|\delta\|^2).
$$

而 Gaussian 核迫使 $\delta=O(\!\sqrt h)$。完成平方后，backward increment 的条件均值满足

$$
\mathbb E[X_{t-h}-X_t\mid X_t=x]
=\sigma^2\nabla\log p_t(x)h+o(h).
$$

所以反向时钟漂移为

$$
b_{\rm rev}(s,x)
=\sigma^2\nabla\log p_{T-s}(x).
$$

### 2.1 直觉不能替代的地方

“score 指向高密度”只是局部直觉。严格对象是：

$$
\lim_{h\downarrow0}
\frac{\mathbb E[X_{t-h}-X_t\mid X_t=x]}{h}.
$$

它来自 backward conditional kernel，而不是凭几何图像添加一个 gradient。

## 三、一般反向漂移：从 probability current 推导

### 3.1 前向 current

DYN-11 已得 Fokker–Planck：

$$
\partial_t p
=-\nabla\cdot(fp)
+\frac12\sum_{i,j}\partial_{ij}(D_{ij}p).
$$

定义向量

$$
[\nabla\cdot(Dp)]_i
=\sum_j\partial_j(D_{ij}p),
$$

则

$$
\partial_t p=-\nabla\cdot J,
$$

其中

$$
J=fp-\frac12\nabla\cdot(Dp).
$$

### 3.2 反向密度的 current 必须翻转

因为 $q_s=p_{T-s}$，

$$
\partial_s q_s
=-\partial_t p_t
=\nabla\cdot J_t
=-\nabla\cdot(-J_t).
$$

因此反向过程的 current 应为

$$
J_{\rm rev}(s,x)=-J(T-s,x).
$$

若反向过程保持相同 diffusion matrix $D$，并设 drift 为 $b_{\rm rev}$，则

$$
J_{\rm rev}
=b_{\rm rev}p-\frac12\nabla\cdot(Dp).
$$

与 $-J$ 配平：

$$
b_{\rm rev}p-\frac12\nabla\cdot(Dp)
=-fp+\frac12\nabla\cdot(Dp).
$$

所以

$$
\boxed{
b_{\rm rev}
=-f+\frac1p\nabla\cdot(Dp)
}.
$$

展开乘积：

$$
\frac1p\nabla\cdot(Dp)
=\nabla\cdot D+D\nabla\log p,
$$

其中

$$
(\nabla\cdot D)_i=\sum_j\partial_jD_{ij}.
$$

因此一般公式是

$$
\boxed{
b_{\rm rev}
=-f+\nabla\cdot D+D\nabla\log p
}.
$$

### 3.3 常用 isotropic 特例

若

$$
B(t,x)=g(t)I,
\qquad
D(t,x)=g(t)^2I,
$$

则 $D$ 不依赖 $x$，所以

$$
\nabla\cdot D=0.
$$

反向时钟 SDE 化为

$$
\boxed{
dY_s
=\left[-f(t,Y_s)+g(t)^2\nabla\log p_t(Y_s)\right]ds
+g(t)d\bar W_s,
\quad t=T-s.
}
$$

> [!danger] 不能漏掉的 correction
> $-f+g^2s_t$ 只是空间齐次 isotropic diffusion 的公式。将它原样套到 $D(t,x)$ 会漏掉 $\nabla\cdot D$，目标密度一般随即改变。

## 四、Fokker–Planck 配平与真正时间反演定理的差别

上面的 current 推导证明：候选反向 SDE 的边缘密度满足所需 PDE。

但“PDE 边缘配平”与“它就是原过程的完整时间反演”仍有层级差：

| 层级 | 需要证明什么 |
|---|---|
| marginal consistency | 每个 $s$ 的 law 是 $p_{T-s}$ |
| transition reversal | backward kernel 满足 Bayes 反转 |
| path-law reversal | $(Y_{s_1},\ldots,Y_{s_k})$ 与 $(X_{T-s_1},\ldots,X_{T-s_k})$ 同 law |
| SDE representation | 反向过程相对于反向 filtration 可写成所述 SDE |

经典反向 diffusion 定理通常要求某种组合：

1. drift/diffusion 足够光滑并满足增长条件；
2. diffusion 非退化或满足可替代的 hypoelliptic 条件；
3. $p_t(x)>0$ 且具有足够空间正则性；
4. $D p_t$ 的导数存在并可积；
5. nonexplosion 与边界行为受控；
6. transition density 与反向 filtration 定义良好。

退化 diffusion、反射边界、流形状态空间、奇异初始分布或低正则系数需要专门版本，不能仅凭形式公式处理。

## 五、为什么反向 SDE 是完整 score，而概率流 ODE 是一半

### 5.1 反向 SDE

反向 SDE 仍保留 diffusion current：

$$
J_{\rm rev}
=b_{\rm rev}p-\frac12\nabla\cdot(Dp).
$$

为使 $J_{\rm rev}=-J$，drift 中必须出现完整的

$$
\frac1p\nabla\cdot(Dp).
$$

### 5.2 反向 probability-flow ODE

前向 probability-flow velocity 是

$$
v_{\rm PF}
=f-\frac1{2p}\nabla\cdot(Dp).
$$

反向时钟只需取负速度：

$$
b_{\rm PF,rev}
=-v_{\rm PF}
=-f+\frac1{2p}\nabla\cdot(Dp).
$$

空间齐次 isotropic 情形：

$$
\boxed{
\frac{dY_s}{ds}
=-f(t,Y_s)+\frac12g(t)^2\nabla\log p_t(Y_s)
}.
$$

两者的差别不是约定，而是 diffusion 是否仍贡献一半二阶通量：

| 生成器 | score 系数 | 随机项 |
|---|---:|---:|
| reverse SDE | $g^2$ | 有 |
| reverse PF ODE | $g^2/2$ | 无 |

> [!danger] 高频实现错误
> 在保留 $g\,d\bar W$ 的 reverse SDE 中使用半个 score，会同时保留完整扩散噪声和错误漂移；减小步长只会精确求解这个错误模型。

## 六、VP SDE：从数据到标准 Gaussian 的连续模型

### 6.1 定义

Variance-preserving SDE：

$$
dX_t
=-\frac12\beta(t)X_tdt
+\sqrt{\beta(t)}dW_t,
\qquad \beta(t)\ge0.
$$

定义

$$
\alpha(t)
=\exp\left(-\frac12\int_0^t\beta(r)dr\right).
$$

### 6.2 用 integrating factor 求解

令 $A_t=1/\alpha(t)$。Itô product rule 中 $A_t$ 是确定性有限变差函数，因此无 quadratic covariation：

$$
d(A_tX_t)
=A_t\sqrt{\beta(t)}dW_t.
$$

积分得

$$
X_t
=\alpha(t)X_0
+\alpha(t)\int_0^t\frac{\sqrt{\beta(r)}}{\alpha(r)}dW_r.
$$

随机积分是零均值 Gaussian，其方差为

$$
\alpha(t)^2
\int_0^t\frac{\beta(r)}{\alpha(r)^2}dr
=1-\alpha(t)^2.
$$

记

$$
\sigma(t)^2=1-\alpha(t)^2,
$$

则 conditional noising law 为

$$
\boxed{
X_t\mid X_0=x_0
\sim\mathcal N(\alpha(t)x_0,\sigma(t)^2I)
}.
$$

等价的 fixed-time reparameterization 是

$$
X_t=\alpha(t)X_0+\sigma(t)\varepsilon,
\qquad
\varepsilon\sim\mathcal N(0,I).
$$

这条式子足以生成训练样本，但单独看它仍不定义跨时间 Brownian coupling；过程级定义来自 SDE。

### 6.3 为什么叫 variance-preserving

若 $X_0$ 每个坐标零均值、方差为1，则

$$
\operatorname{Var}(X_t)
=\alpha(t)^2+\sigma(t)^2
=1.
$$

对一般数据，方差逐渐趋向1，而不是每个时刻都严格保持原数据方差。

当

$$
\int_0^T\beta(r)dr
$$

足够大时，$\alpha(T)$ 很小，故 $p_T$ 接近标准 Gaussian；有限 $T$ 下一般只是近似，不是恒等。

## 七、VE SDE：保持信号中心，增加噪声尺度

Variance-exploding 形式可写为

$$
dX_t=g(t)dW_t.
$$

于是

$$
X_t
=X_0+\int_0^tg(r)dW_r.
$$

若定义

$$
\sigma(t)^2
=\sigma(0)^2+\int_0^tg(r)^2dr,
$$

则常见 conditional law 是

$$
X_t\mid X_0=x_0
\sim\mathcal N(x_0,[\sigma(t)^2-\sigma(0)^2]I).
$$

在从零噪声开始的理想写法中，简化为

$$
X_t=X_0+\sigma(t)\varepsilon,
\qquad
g(t)^2=\frac d{dt}\sigma(t)^2.
$$

### 7.1 VP 与 VE 不能只按名字比较

| 维度 | VP | VE |
|---|---|---|
| drift | $-\beta x/2$ | 0 |
| conditional mean | $\alpha x_0$ | $x_0$ |
| noise variance | $1-\alpha^2$ | 随 schedule 增长 |
| 常见 terminal scale | 约标准 Gaussian | 大方差 Gaussian |
| score target | $-(x_t-\alpha x_0)/\sigma^2$ | $-(x_t-x_0)/\sigma^2$ |

比较 sampler 或 loss 时，必须先统一数据缩放、time/noise parameterization、终端分布和 NFE。

## 八、score 是什么，不是什么

对正密度 $p$，score 定义为

$$
s_p(x)=\nabla_x\log p(x)
=\frac{\nabla p(x)}{p(x)}.
$$

### 8.1 score 的三个性质

1. 它是定义在样本空间的向量场，不是模型参数梯度；
2. 归一化常数消失：若 $p(x)=\tilde p(x)/Z$，则
   $$
   \nabla_x\log p(x)=\nabla_x\log\tilde p(x);
   $$
3. 在 regularity/tail 条件下，
   $$
   \mathbb E_p[s_p(X)]=0.
   $$

### 8.2 score 不直接给 density 值

score 只给局部 log-density gradient。若定义域单连通且向量场确为梯度场，可以沿路径积分恢复 log density 到一个常数；归一化常数仍需额外确定。

神经网络输出一个任意向量场时，也不保证 curl-free，未必等于某个全局 density 的精确 score。

## 九、直接 score matching：消掉未知数据 score

设网络 $s_\theta(x)$ 试图逼近 $s_p(x)$。最直接的 Fisher divergence 是

$$
\mathcal J_F(\theta)
=\frac12\mathbb E_p
\|s_\theta(X)-s_p(X)\|^2.
$$

展开：

$$
\mathcal J_F
=\frac12\mathbb E_p\|s_\theta\|^2
-\mathbb E_p[s_\theta^\top s_p]
+C_p.
$$

交叉项为

$$
\mathbb E_p[s_\theta^\top s_p]
=\int s_\theta(x)^\top\nabla p(x)dx.
$$

若边界项消失，分部积分得到

$$
\int s_\theta^\top\nabla p,dx
=-\int(\nabla\cdot s_\theta)p,dx.
$$

因此忽略与 $\theta$ 无关的常数：

$$
\boxed{
\mathcal J_{\rm SM}(\theta)
=\mathbb E_p\left[
\frac12\|s_\theta(X)\|^2
+\nabla\cdot s_\theta(X)
\right].
}
$$

### 9.1 理论责任

这个等价需要：

- $p$ 与 $s_\theta$ 足够可微；
- 积分有限；
- whole-space tail 或 domain boundary term 消失；
- 数据相对于 Lebesgue 测度有密度。

若真实数据集中在低维流形上，$p_0$ 的 ambient-space score 可能根本不存在。这也是在 $t>0$ 加 Gaussian noise 的数学意义之一。

## 十、Denoising score matching：用已知条件 score 训练未知边缘 score

### 10.1 条件 corruption 可采样

给定 $X_0$，我们能采样

$$
X_t\sim q_{t\mid0}(\cdot\mid X_0).
$$

其边缘密度是

$$
p_t(x)
=\int q_{t\mid0}(x\mid x_0)p_0(x_0)dx_0.
$$

虽然 $p_t$ 通常不可计算，但 conditional score

$$
\nabla_x\log q_{t\mid0}(x\mid x_0)
$$

常有闭式。

### 10.2 conditional-to-marginal score 恒等式

对边缘密度求导：

$$
\nabla_xp_t(x)
=\int \nabla_xq_{t\mid0}(x\mid x_0)p_0(x_0)dx_0.
$$

用

$$
\nabla q=q\nabla\log q
$$

改写：

$$
\nabla_xp_t(x)
=\int q(x\mid x_0)p_0(x_0)
\nabla_x\log q(x\mid x_0)dx_0.
$$

除以 $p_t(x)$：

$$
\boxed{
\nabla_x\log p_t(x)
=\mathbb E\left[
\nabla_x\log q_{t\mid0}(X_t\mid X_0)
\mid X_t=x
\right].
}
$$

### 10.3 为什么平方损失会学到条件期望

令随机 target

$$
U=\nabla_{x_t}\log q_{t\mid0}(X_t\mid X_0).
$$

平方损失满足正交分解：

$$
\mathbb E\|s(X_t)-U\|^2
=\mathbb E\|s(X_t)-\mathbb E[U\mid X_t]\|^2
+\mathbb E\|U-\mathbb E[U\mid X_t]\|^2.
$$

第二项与 $s$ 无关，所以 population minimizer 是

$$
s^\star(x,t)=\mathbb E[U\mid X_t=x]=\nabla\log p_t(x).
$$

这条结论只说明无限函数类、population objective 的最优解。有限数据、有限网络、优化不完全和权重选择仍会造成误差。

### 10.4 Gaussian corruption target

若

$$
X_t=\alpha_tX_0+\sigma_t\varepsilon,
\qquad \varepsilon\sim\mathcal N(0,I),
$$

则

$$
q_{t\mid0}(x_t\mid x_0)
=\mathcal N(\alpha_tx_0,\sigma_t^2I),
$$

故

$$
\nabla_{x_t}\log q_{t\mid0}(x_t\mid x_0)
=-\frac{x_t-\alpha_tx_0}{\sigma_t^2}
=-\frac\varepsilon{\sigma_t}.
$$

训练时不需要计算 $p_t$，只需采样 $(x_0,t,\varepsilon)$。

## 十一、Tweedie 公式：score 就是最优去噪位移

由上一节，

$$
\nabla\log p_t(x)
=\mathbb E\left[
-\frac{x-\alpha_tX_0}{\sigma_t^2}
\mid X_t=x
\right].
$$

将确定的 $x$ 移出条件期望：

$$
\nabla\log p_t(x)
=-\frac{x-\alpha_t\mathbb E[X_0\mid X_t=x]}{\sigma_t^2}.
$$

整理得到

$$
\boxed{
\mathbb E[X_0\mid X_t=x]
=\frac{x+\sigma_t^2\nabla\log p_t(x)}{\alpha_t}
}.
$$

在 additive noise $X_t=X_0+\sigma_t\varepsilon$ 中，$\alpha_t=1$：

$$
\mathbb E[X_0\mid X_t=x]
=x+\sigma_t^2\nabla\log p_t(x).
$$

所以 score 不是“直接指向某个最近训练样本”，而是给出 posterior mean denoising correction。

### 11.1 多峰分布中的意义

若 noisy observation 位于两个 mode 中间，posterior mean 可能落在低密度区域。Tweedie 给的是平方损失下的条件均值，不自动等于 MAP、mode 或一条真实 clean sample。

## 十二、score、noise、$x_0$ 与 $v$ 参数化

令

$$
x_t=\alpha_tx_0+\sigma_t\varepsilon.
$$

### 12.1 score prediction

网络直接输出

$$
s_\theta(x_t,t)\approx\nabla\log p_t(x_t).
$$

条件训练 target 是

$$
-\varepsilon/\sigma_t.
$$

### 12.2 noise prediction

网络输出 $\varepsilon_\theta$，并定义

$$
\boxed{
s_\theta(x_t,t)
=-\frac{\varepsilon_\theta(x_t,t)}{\sigma_t}.
}
$$

### 12.3 clean-data prediction

网络输出 $\widehat x_{0,\theta}$。由 Tweedie relation：

$$
\boxed{
s_\theta(x_t,t)
=\frac{\alpha_t\widehat x_{0,\theta}(x_t,t)-x_t}{\sigma_t^2}.
}
$$

### 12.4 $v$ prediction

在 VP normalization

$$
\alpha_t^2+\sigma_t^2=1
$$

下，定义

$$
v=\alpha_t\varepsilon-\sigma_tx_0.
$$

于是

$$
\begin{bmatrix}x_t\\v\end{bmatrix}
=
\begin{bmatrix}
\alpha_t&\sigma_t\\
-\sigma_t&\alpha_t
\end{bmatrix}
\begin{bmatrix}x_0\\\varepsilon\end{bmatrix}.
$$

该矩阵正交，逆变换为

$$
\boxed{
x_0=\alpha_tx_t-\sigma_tv,
\qquad
\varepsilon=\sigma_tx_t+\alpha_tv.
}
$$

### 12.5 参数化等价不代表训练问题等价

考虑带权 score loss：

$$
\mathcal L_s
=\mathbb E\left[
\lambda(t)
\left\|s_\theta(X_t,t)+\frac\varepsilon{\sigma_t}\right\|^2
\right].
$$

代入 $s_\theta=-\varepsilon_\theta/\sigma_t$：

$$
\mathcal L_s
=\mathbb E\left[
\frac{\lambda(t)}{\sigma_t^2}
\|\varepsilon_\theta-\varepsilon\|^2
\right].
$$

因此 unweighted noise MSE 对应的是 $\lambda(t)=\sigma_t^2$ 的 score weighting，而不是所有噪声时刻等权的 Fisher loss。

类似地，$x_0$ prediction 的 score error 权重会出现

$$
\frac{\alpha_t^2}{\sigma_t^4}.
$$

参数化转换、loss weighting、network preconditioning 和 sampler conversion 必须作为一个整体声明。

## 十三、连续时间训练目标

典型 denoising score objective：

$$
\mathcal L(\theta)
=\mathbb E_{t\sim\rho}
\mathbb E_{X_0,\varepsilon}
\left[
\lambda(t)
\left\|
s_\theta(\alpha_tX_0+\sigma_t\varepsilon,t)
+\frac\varepsilon{\sigma_t}
\right\|^2
\right].
$$

### 13.1 三种权重不要混为一个符号

| 权重 | 作用 |
|---|---|
| time sampling density $\rho(t)$ | 哪些时刻更常出现 |
| explicit loss weight $\lambda(t)$ | 每个样本的损失尺度 |
| parameterization-induced factor | score/epsilon/$x_0$ 换算产生 |

实际有效权重是三者乘积。

### 13.2 小噪声端为何困难

Gaussian conditional target 的尺度是

$$
\|\varepsilon/\sigma_t\|.
$$

当 $\sigma_t\to0$ 时，其方差会爆炸。常见处理包括：

- 截断到 $t\ge\varepsilon>0$；
- 改用 noise/$v$ 参数化；
- 改变 time sampling 与 loss weighting；
- 对网络输入输出做 preconditioning。

这些选择改变统计与数值条件，必须写入训练合同。

## 十四、离散 DDPM 的前向 Markov 链

为避免与连续 $\alpha(t)$ 混淆，本节记

$$
a_k=1-\beta_k,
\qquad
\bar a_k=\prod_{j=1}^ka_j.
$$

### 14.1 单步前向核

$$
q(x_k\mid x_{k-1})
=\mathcal N(\sqrt{a_k}x_{k-1},\beta_kI).
$$

可重参数化为

$$
x_k=\sqrt{a_k}x_{k-1}+\sqrt{\beta_k}z_k.
$$

### 14.2 闭式 $k$ 步条件分布

递推展开：

$$
x_k
=\sqrt{\bar a_k}x_0
+\sum_{j=1}^k
\sqrt{\beta_j}
\left(\prod_{\ell=j+1}^k\sqrt{a_\ell}\right)z_j.
$$

随机项为独立 Gaussian 之和，方差递推：

$$
1-\bar a_k
=a_k(1-\bar a_{k-1})+\beta_k.
$$

因此

$$
\boxed{
q(x_k\mid x_0)
=\mathcal N(
\sqrt{\bar a_k}x_0,
(1-\bar a_k)I
).
}
$$

训练时可直接跳到任意 $k$：

$$
x_k
=\sqrt{\bar a_k}x_0
+\sqrt{1-\bar a_k}\varepsilon.
$$

### 14.3 离散链仍需要共同过程定义

直接抽一个 $k$ 和一份 $\varepsilon$ 足以估计训练 loss；它不等于已经模拟了整个 Markov path。路径级实验需要共享单步噪声或明确的 coupling。

## 十五、精确 posterior $q(x_{k-1}\mid x_k,x_0)$

由 Bayes：

$$
q(x_{k-1}\mid x_k,x_0)
\propto
q(x_k\mid x_{k-1})
q(x_{k-1}\mid x_0).
$$

两项均为 Gaussian：

$$
q(x_k\mid x_{k-1})
\propto
\exp\left[-\frac{
\|x_k-\sqrt{a_k}x_{k-1}\|^2
}{2\beta_k}\right],
$$

$$
q(x_{k-1}\mid x_0)
\propto
\exp\left[-\frac{
\|x_{k-1}-\sqrt{\bar a_{k-1}}x_0\|^2
}{2(1-\bar a_{k-1})}\right].
$$

收集关于 $x_{k-1}$ 的二次项，posterior precision 为

$$
\frac{a_k}{\beta_k}
+\frac1{1-\bar a_{k-1}}
=\frac{1-\bar a_k}
{\beta_k(1-\bar a_{k-1})}.
$$

所以 posterior variance：

$$
\boxed{
\widetilde\beta_k
=\frac{1-\bar a_{k-1}}{1-\bar a_k}\beta_k.
}
$$

线性项给 posterior mean：

$$
\boxed{
\widetilde\mu_k(x_k,x_0)
=
\frac{\sqrt{\bar a_{k-1}}\beta_k}{1-\bar a_k}x_0
+
\frac{\sqrt{a_k}(1-\bar a_{k-1})}{1-\bar a_k}x_k.
}
$$

因此

$$
q(x_{k-1}\mid x_k,x_0)
=\mathcal N(\widetilde\mu_k,\widetilde\beta_kI).
$$

### 15.1 为什么这还不能直接生成

生成时只有 $x_k$，没有真实 $x_0$。网络的任务是用 $x_k,k$ 预测与 $x_0$ 等价的信息：noise、clean data、score 或 $v$。

## 十六、从 noise prediction 得到 DDPM reverse mean

由

$$
x_k
=\sqrt{\bar a_k}x_0
+\sqrt{1-\bar a_k}\varepsilon,
$$

可估计

$$
\widehat x_{0,\theta}
=\frac{x_k-\sqrt{1-\bar a_k}\varepsilon_\theta(x_k,k)}
{\sqrt{\bar a_k}}.
$$

代入 $\widetilde\mu_k$ 并整理，得到常用 mean：

$$
\boxed{
\mu_\theta(x_k,k)
=\frac1{\sqrt{a_k}}
\left(
x_k
-\frac{\beta_k}{\sqrt{1-\bar a_k}}
\varepsilon_\theta(x_k,k)
\right).
}
$$

ancestral sampling：

$$
x_{k-1}
=\mu_\theta(x_k,k)+\sigma_kz,
\qquad z\sim\mathcal N(0,I).
$$

$\sigma_k^2$ 可以固定为 $\widetilde\beta_k$、采用其他 prescribed variance，或由模型学习；不同选择不是同一个生成链。

## 十七、ELBO 与 simplified noise loss

生成模型写成

$$
p_\theta(x_{0:K})
=p(x_K)\prod_{k=1}^Kp_\theta(x_{k-1}\mid x_k).
$$

以固定 forward chain $q(x_{1:K}\mid x_0)$ 作为 variational posterior，可得 negative log-likelihood upper bound：

$$
-\log p_\theta(x_0)
\le
\operatorname{KL}(q(x_K\mid x_0)\|p(x_K))
$$

$$
+\sum_{k=2}^K
\mathbb E_q
\operatorname{KL}
\left(
q(x_{k-1}\mid x_k,x_0)
\|p_\theta(x_{k-1}\mid x_k)
\right)
$$

$$
-\mathbb E_q\log p_\theta(x_0\mid x_1).
$$

若 reverse variance 固定，两个 Gaussian KL 对 mean error 是加权二次损失；使用 $\varepsilon_\theta$ 参数化后可化为

$$
\mathbb E_{k,x_0,\varepsilon}
[w_k\|\varepsilon-\varepsilon_\theta(x_k,k)\|^2]
+\text{constants}.
$$

DDPM 常用 simplified objective：

$$
\mathcal L_{\rm simple}
=\mathbb E\|\varepsilon-\varepsilon_\theta(x_k,k)\|^2,
$$

即移除了原 ELBO 的特定 $w_k$。

> [!warning] 必须如实表述
> simplified noise MSE 与 ELBO 密切相关，但一般不等于原始、逐项同权的 maximum-likelihood objective。它重新加权了不同噪声时刻，可能改善样本训练，却改变 likelihood 目标。

## 十八、离散 DDPM 与连续 VP SDE 的对应

令时间步 $\Delta t$ 很小，并取

$$
\beta_k\approx\beta(t_k)\Delta t.
$$

则

$$
\sqrt{1-\beta_k}
=1-\frac12\beta(t_k)\Delta t+O(\Delta t^2).
$$

前向更新

$$
x_k
=\sqrt{1-\beta_k}x_{k-1}
+\sqrt{\beta_k}z_k
$$

成为

$$
x_k-x_{k-1}
=-\frac12\beta(t_k)x_{k-1}\Delta t
+\sqrt{\beta(t_k)}\sqrt{\Delta t}z_k
+O(\Delta t^2),
$$

正是 VP SDE 的 Euler–Maruyama 结构。

同时

$$
\bar a_k
=\prod_{j=1}^k(1-\beta_j)
$$

满足

$$
\log\bar a_k
\approx-\sum_j\beta(t_j)\Delta t
\longrightarrow-\int_0^t\beta(r)dr.
$$

故

$$
\sqrt{\bar a_k}
\longrightarrow
\exp\left(-\frac12\int_0^t\beta(r)dr\right)
=\alpha(t).
$$

### 18.1 对应不等于完全相同

连续 SDE 是极限模型；给定有限 schedule 的 DDPM 是具体 Markov chain。有限 $K$、variance choice、reverse parameterization 和 sampler skipping 都可能产生与连续模型不同的误差。

## 十九、五类采样器的对象区别

### 19.1 DDPM ancestral sampler

按 learned reverse Gaussian kernel 逐步采样：

$$
x_{k-1}=\mu_\theta(x_k,k)+\sigma_kz_k.
$$

它是离散 stochastic Markov chain。

### 19.2 Reverse-SDE Euler–Maruyama

对反向时钟

$$
dY_s=b_\theta(s,Y_s)ds+g(T-s)d\bar W_s
$$

做

$$
Y_{n+1}
=Y_n+b_\theta(s_n,Y_n)h
+g(T-s_n)\sqrt h\,Z_n.
$$

它近似连续 reverse SDE；strong/weak error 与 Brownian coupling 规则见 DYN-10。

### 19.3 Probability-flow ODE sampler

求解

$$
\frac{dY_s}{ds}
=-f(t,Y_s)+\frac12g(t)^2s_\theta(Y_s,t).
$$

它是确定性 map。精确 score 与精确积分时，one-time marginals 与 reverse SDE 对齐；有限网络与有限步下不保证样本误差排序。

### 19.4 Predictor–corrector

predictor 推进 reverse SDE；corrector 在固定噪声时刻做近似 Langevin 更新：

$$
x\leftarrow x+\eta s_\theta(x,t)+\sqrt{2\eta}z.
$$

corrector 的目标是更贴近当时 $p_t$，但有限 $\eta$、有限步、错误 score 都会改变 stationary behavior。

### 19.5 DDIM

由 $\varepsilon_\theta$ 得

$$
\widehat x_0
=\frac{x_k-\sqrt{1-\bar a_k}\varepsilon_\theta}{\sqrt{\bar a_k}}.
$$

定义

$$
\sigma_k(\eta)
=\eta
\sqrt{\frac{1-\bar a_{k-1}}{1-\bar a_k}}
\sqrt{1-\frac{\bar a_k}{\bar a_{k-1}}}.
$$

更新

$$
x_{k-1}
=\sqrt{\bar a_{k-1}}\widehat x_0
+\sqrt{1-\bar a_{k-1}-\sigma_k(\eta)^2}\,
\varepsilon_\theta
+\sigma_k(\eta)z.
$$

- $\eta=0$：deterministic DDIM path；
- 合适的 $\eta>0$：加入 stochasticity；
- 它可复用 DDPM 的训练目标，但不意味着与 DDPM 拥有同一 path law。

## 二十、条件生成与 guidance

### 20.1 条件 score 的 Bayes 分解

$$
\log p_t(x\mid y)
=\log p_t(x)+\log p_t(y\mid x)-\log p_t(y).
$$

对 $x$ 求梯度：

$$
\boxed{
\nabla_x\log p_t(x\mid y)
=\nabla_x\log p_t(x)
+\nabla_x\log p_t(y\mid x).
}
$$

classifier guidance 用 noise-conditioned classifier 估计第二项。

若乘 guidance scale $\gamma$：

$$
s_{\rm guided}
=s_{\rm uncond}+\gamma\nabla_x\log p_t(y\mid x),
$$

固定时刻下对应未经归一化的 tempered density

$$
p_t(x)p_t(y\mid x)^\gamma.
$$

$\gamma\ne1$ 不再是原条件分布本身。

### 20.2 Classifier-free guidance

同一网络通过随机丢弃 condition 学习 conditional 与 unconditional prediction。用 score 记号，一种常见 convention 是

$$
s_{\rm cfg}
=s_{\rm uncond}
+w(s_{\rm cond}-s_{\rm uncond}).
$$

- $w=0$：unconditional；
- $w=1$：conditional；
- $w>1$：extrapolation。

另一种文献写成 $s_{\rm cond}+\gamma(s_{\rm cond}-s_{\rm uncond})$；两者只差参数 convention，报告时必须说明。

即使两支都是精确 score，$w>1$ 也改变目标 density，并可能牺牲 mode coverage 换取条件一致性；网络误差、condition dropout 与采样时 extrapolation 还会进一步造成分布偏移。

## 二十一、Probability-flow likelihood

前向 probability-flow ODE：

$$
\dot x_t=v_\theta(t,x_t),
\qquad
v_\theta=f-\frac12g^2s_\theta.
$$

若 flow 适定，沿轨迹有

$$
\frac d{dt}\log p_t(x_t)
=-\nabla\cdot v_\theta(t,x_t).
$$

从 $0$ 积到 $T$：

$$
\log p_T(x_T)-\log p_0(x_0)
=-\int_0^T\nabla\cdot v_\theta(t,x_t)dt.
$$

故

$$
\boxed{
\log p_0(x_0)
=\log p_T(x_T)
+\int_0^T\nabla\cdot v_\theta(t,x_t)dt.
}
$$

高维中可用 Hutchinson estimator 近似 divergence：

$$
\nabla\cdot v
=\operatorname{tr}(J_xv)
=\mathbb E_z[z^\top J_xv,z].
$$

### 21.1 “精确 likelihood”需要限定对象

给定 learned vector field，数值上足够精确地积分 state 与 log-density，可评估这个 CNF/ODE 模型的 likelihood。它不自动等于：

- 真实数据 likelihood；
- learned reverse SDE 的 path likelihood；
- 有限容差下无误差的数值值；
- 训练用 simplified MSE 的直接优化目标。

## 二十二、端点与数据流形问题

### 22.1 数据端 $t=0$

经验数据分布是有限点质量；自然数据也可能集中在低维集合上。此时 ambient density $p_0$ 或 $\nabla\log p_0$ 可能不存在。

对任意 $t>0$，非退化 Gaussian smoothing 往往产生光滑正密度 $p_t$。因此实际训练常取

$$
t\in[\varepsilon,T]
$$

而非真的到0。

代价是 sampler 首先恢复 $p_\varepsilon$；从 $\varepsilon$ 到 clean data 的最后一步可能使用 denoiser、projection 或离散 decoder。这些都是模型定义的一部分。

### 22.2 噪声端 $t=T$

有限时间下通常只有

$$
p_T\approx\pi,
$$

而非相等。若生成从 $\pi$ 启动，存在 terminal prior mismatch。

增加 $T$ 或总噪声可减小这项误差，但会加重：

- 动态范围；
- time-conditioning；
- 低 SNR 学习；
- 求解成本；
- endpoint stiffness/parameterization 问题。

没有免费的“无限加噪”。

## 二十三、完整误差账本

设理想数据分布为 $p_0$，实际生成结果为 $\widehat p_{0,h,\theta}$。至少分开：

### 23.1 Terminal error

$$
p_T\ne\pi.
$$

即使 score 与 solver 精确，从错误初始 law 出发也可能残留偏差。

### 23.2 Statistical/approximation score error

$$
s_\theta(x,t)-\nabla\log p_t(x).
$$

来源包括有限数据、函数类限制、优化误差、time weighting 与 distribution shift。

### 23.3 Continuous-model choice

reverse SDE、PF ODE、DDIM path 和 guided dynamics 不是同一个 path law；在 approximate score 下也未必共享 marginal。

### 23.4 Numerical discretization

$$
h>0,
$$

包括 truncation、adaptive tolerance、stochastic strong/weak error、Brownian coupling 与 endpoint grid。

### 23.5 Parameterization/conversion error

score、noise、$x_0$、$v$ 与 preconditioned output 的尺度若转换不一致，得到的是系统性模型错误，不是普通 roundoff。

### 23.6 Guidance/conditioning error

condition dropout、classifier calibration、guidance scale 与 extrapolation 改变 target law。

### 23.7 Monte Carlo 与 evaluation error

有限样本 FID、precision/recall、likelihood estimator、random seeds 与 data preprocessing 都有独立不确定性。

> [!check] 最关键的诊断实验
> 固定 score 并做 $h\to0$ refinement。如果误差消失，主要是 solver error；如果收敛到非零地板，应检查 score、terminal、coefficient、guidance 或目标定义。不能用“更多步没有改善”直接断言 ODE/SDE 理论失败。

## 二十四、完整手算：Gaussian 数据上的 VP 反演

设一维 constant-$\beta$ VP：

$$
dX_t=-\frac\beta2X_tdt+\sqrt\beta dW_t,
$$

且

$$
X_0\sim\mathcal N(m_0,v_0).
$$

### 24.1 前向 moments

$$
m_t=e^{-\beta t/2}m_0,
$$

$$
v_t
=e^{-\beta t}v_0+(1-e^{-\beta t})
=1+(v_0-1)e^{-\beta t}.
$$

因此

$$
p_t=\mathcal N(m_t,v_t),
\qquad
s_t(x)=-\frac{x-m_t}{v_t}.
$$

### 24.2 反向 SDE drift

在 $s$ 时钟、$t=T-s$ 下：

$$
b_{\rm rev}(s,x)
=\frac\beta2x+\beta s_t(x).
$$

代入 Gaussian score：

$$
b_{\rm rev}(s,x)
=\beta\left(\frac12-\frac1{v_t}\right)x
+\beta\frac{m_t}{v_t}.
$$

所以反向过程仍是线性 Gaussian diffusion。

### 24.3 反向 PF ODE

$$
\frac{dY_s}{ds}
=\frac\beta2Y_s+\frac\beta2s_t(Y_s)
$$

即

$$
\frac{dY_s}{ds}
=\frac\beta2\left(1-\frac1{v_t}\right)Y_s
+\frac\beta2\frac{m_t}{v_t}.
$$

反向 SDE 与 PF ODE 都恢复 $m_0,v_0$ 的边缘，但前者有 quadratic variation，后者没有。

### 24.4 Euler moment recursion

若线性 reverse SDE 写成

$$
dY_s=(A_sY_s+c_s)ds+\sqrt\beta d\bar W_s,
$$

Euler–Maruyama 为

$$
Y_{n+1}=(1+A_nh)Y_n+c_nh+\sqrt{\beta h}Z_n.
$$

其 moments 精确满足离散递推：

$$
\mu_{n+1}
=(1+A_nh)\mu_n+c_nh,
$$

$$
V_{n+1}
=(1+A_nh)^2V_n+\beta h.
$$

这使我们无需 Monte Carlo 噪声，就能单独测量 weak moment discretization error。

配套实验正是用这条递推分离 solver 与 model bias。

## 二十五、研究与实现验收清单

### 25.1 Forward process card

- state space 与 data scaling；
- $f,B,D$ 或 discrete $\beta_k$；
- $q(x_t\mid x_0)$；
- time/noise/SNR parameterization；
- $p_T$ 与 chosen prior 的差距。

### 25.2 Training card

- score/noise/$x_0$/$v$ 哪种输出；
- $t$ sampling density；
- loss weighting；
- condition dropout 与 guidance convention；
- small-noise cutoff；
- EMA、precision 与 data preprocessing。

### 25.3 Sampler card

- reverse SDE、PF ODE、DDPM、DDIM 或其他；
- score coefficient 是1还是1/2；
- time grid、NFE、step/tolerance；
- stochastic seed/Brownian coupling；
- final denoising；
- guidance scale 和 clipping/thresholding。

### 25.4 Evaluation card

- 样本量与随机种子；
- metric implementation 与 feature extractor；
- likelihood estimator/tolerance；
- compute、wall time 与 NFE；
- solver refinement；
- terminal/score/solver ablation。

## 二十六、常见错误总表

| 错误 | 为什么错 | 修正 |
|---|---|---|
| 反向就是 $dt\mapsto-dt$ | filtration 与 conditional drift 改变 | 显式定义 $Y_s=X_{T-s}$ |
| reverse drift 只有 $D\,score$ | 漏掉 $-f$ | 从 current 或 Bayes 推导 |
| 一般 diffusion 仍写 $-f+Dscore$ | 漏掉 $\nabla\cdot D$ | 用 $p^{-1}\nabla\cdot(Dp)$ |
| reverse SDE 使用半个 score | 半系数属于无噪 PF ODE | 检查生成器是否保留 noise |
| conditional score 就是 marginal score | 单个 target 含 $X_0$ | 取 $\mathbb E[\cdot\mid X_t]$ |
| $\varepsilon$ MSE 与等权 score MSE 相同 | 差 $1/\sigma_t^2$ | 明确 effective weighting |
| DDPM fixed-time sampler 等于整条 path | 缺少跨时 coupling | 声明 Markov increments |
| DDIM deterministic 所以与 DDPM 同 path | 只复用训练/边缘结构 | 区分 path law |
| $p_T$ 就是标准 Gaussian | 有限 $T$ 通常仅近似 | 测 terminal mismatch |
| 增加步数能修复错误 score | refinement只修 solver | 做 error-floor 实验 |
| guidance 只提高质量不改分布 | $w\ne1$ 改变目标 | 同时报 coverage/fidelity |
| 数据 score 在 $t=0$ 总存在 | 数据可奇异/在流形上 | 从 $t>0$ smoothing 开始 |

## 二十七、配套学习闭环

- 分层题：[[习题 - 时间反演、score 与扩散生成动力学]]；
- 独立详解：[[解答 - 时间反演、score 与扩散生成动力学]]；
- 复现实验：[[实验 - 反向时间、score恒等式与扩散采样误差审计]]；
- 分卷入口：[[ODE、动力系统与 SDE MOC]]。

> [!check] 当前状态
> 正文、机制图、15道 A—E 题、逐题详解和三轨实验均按 composed 标准建立；尚无学习者首次闭卷答案、独立改参复现与间隔复测，因此保持 `draft`，不记为 mastered。

## 二十八、来源分工与科学空间入口

- [Anderson, *Reverse-time diffusion equation models*](https://doi.org/10.1016/0304-4149(82)90051-5)：reverse diffusion 的原始定理来源；
- [Hyvärinen, *Estimation of Non-Normalized Statistical Models by Score Matching*](https://www.jmlr.org/papers/volume6/hyvarinen05a/hyvarinen05a.pdf)：Fisher divergence 与 integration-by-parts score matching；
- [Vincent, *A Connection Between Score Matching and Denoising Autoencoders*](https://direct.mit.edu/neco/article-pdf/23/7/1661/851298/neco_a_00142.pdf)：denoising 与 score matching 的经典联系；
- [Sohl-Dickstein et al., *Deep Unsupervised Learning using Nonequilibrium Thermodynamics*](https://proceedings.mlr.press/v37/sohl-dickstein15.html)：forward diffusion/reverse generative chain；
- [Ho et al., *Denoising Diffusion Probabilistic Models*](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)：DDPM posterior、noise parameterization 与 simplified training；
- [Song, Meng & Ermon, *Denoising Diffusion Implicit Models*](https://openreview.net/pdf?id=St1giarCHLP)：DDIM 与非 Markov/deterministic generative paths；
- [Song et al., *Score-Based Generative Modeling through SDEs*](https://openreview.net/pdf?id=PxTIG12RRHS)：reverse SDE、probability-flow ODE 与 predictor–corrector 的统一框架；
- [Nichol & Dhariwal, *Improved DDPM*](https://proceedings.mlr.press/v139/nichol21a.html)：learned variance、likelihood与少步采样接口；
- [Karras et al., *Elucidating the Design Space of Diffusion-Based Generative Models*](https://proceedings.neurips.cc/paper_files/paper/2022/hash/a98846e9d9cc01cfb87eb694d946ce6b-Abstract-Conference.html)：noise parameterization、preconditioning、训练与采样设计分离；
- [[S-2022-Su-9209-扩散模型SDE篇]]：连续扩散 SDE 与 score 主线中文入口；
- [[S-2022-Su-9228-概率流ODE]]：Fokker–Planck 与同边缘 ODE 中文入口；
- [[S-2022-Su-9262-统一扩散模型理论篇]]：条件核、边缘一致性与离散反向生成中文入口；
- [[S-2022-Su-9280-硬刚扩散ODE]]：扩散 ODE 与有限步问题入口。

正式 time reversal、score matching、DDPM posterior 与连续/离散框架由原始论文承担；科学空间负责中文问题意识。本章自行补齐时钟符号、state-dependent correction、current 配平层级、DSM 条件期望证明、Tweedie、四参数化权重、误差地板和可复现实验合同。
