---
type: derivation
status: verified
area: [generative-models, score-matching, denoising, conditional-expectation]
node_id: GEN-52
prerequisites: ["[[去噪 Score Matching、Tweedie 公式与条件期望]]", "[[协方差、相关性与条件期望]]", "[[从离散扩散到 VP、VE 与 sub-VP SDE]]"]
related: ["[[Reverse-time SDE、时间反演与 Score Drift]]", "[[数据、噪声、速度与 Score 参数化]]", "[[连续性方程、概率路径与 Flow Matching]]"]
sources: ["[[S-2023-Su-9509-得分匹配与条件得分匹配]]", "[[S-2011-Vincent-Denoising-Score-Matching]]", "[[S-2021-Song-Score-SDE]]", "[[S-2022-Kwon-Wasserstein-Score]]", "[[S-2023-Su-9467-W距离与得分匹配]]"]
exercises: ["[[习题 - Marginal Score、Conditional Score 与去噪等价]]"]
solutions: ["[[解答 - Marginal Score、Conditional Score 与去噪等价]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-conditional-marginal-score-projection-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Marginal Score、Conditional Score 与去噪等价

> [!abstract] 一句话结论
> 真实 reverse dynamics 需要边缘 score $\nabla_x\log p_t(x)$，但训练只需知道 corruption kernel 的 conditional score。原因是后者给定 $X_t=x$ 的条件均值恰好等于 marginal score；在标准平方损失和可测权重下，conditional objective 等于 marginal objective 加一个与模型无关的 conditional-variance 常数。二者共享 population objective 的最优点与梯度，却不逐样本相等，Monte Carlo 方差也不相同。

## 一、训练时到底缺什么

给定数据 $X_0\sim p_0$ 和 forward corruption kernel $q_t(x\mid x_0)$，边缘 noisy density 是

$$
p_t(x)=\int p_0(x_0)q_t(x\mid x_0)dx_0.
$$

reverse SDE/PF ODE 需要

$$s_t^{marg}(x)=\nabla_x\log p_t(x).$$

但 $p_t$ 是对整个未知数据分布的积分，通常不能逐点计算。相反，若 $q_t$ 是 Gaussian，

$$s_t^{cond}(x,x_0)=\nabla_x\log q_t(x\mid x_0)$$

有闭式，而且训练样本 $(x_0,x_t)$ 可直接产生。本节要证明：回归这个“带 $x_0$ 的 noisy target”，为什么最终学到只依赖 $(x_t,t)$ 的 marginal score。

## 二、Marginal score 是 conditional score 的条件均值

在可交换微分与积分、$p_t(x)>0$ 等条件下：

$$
\begin{aligned}
\nabla_xp_t(x)
&=\nabla_x\int p_0(x_0)q_t(x\mid x_0)dx_0\\
&=\int p_0(x_0)\nabla_xq_t(x\mid x_0)dx_0\\
&=\int p_0(x_0)q_t(x\mid x_0)
\nabla_x\log q_t(x\mid x_0)dx_0.
\end{aligned}
$$

两边除以 $p_t(x)$：

$$
\begin{aligned}
\nabla_x\log p_t(x)
&=\int
\frac{p_0(x_0)q_t(x\mid x_0)}{p_t(x)}
\nabla_x\log q_t(x\mid x_0)dx_0\\
&=\int p(x_0\mid x_t=x)
s_t^{cond}(x,x_0)dx_0.
\end{aligned}
$$

所以

$$
\boxed{
s_t^{marg}(x)
=\mathbb E[s_t^{cond}(X_t,X_0)\mid X_t=x].
}
$$

这是逐个 $x$ 的条件期望恒等式，不是说对同一训练样本有 $s^{cond}=s^{marg}$。

## 三、Gaussian corruption 下的 target

统一写成

$$
X_t=a_tX_0+\sigma_t\epsilon,
\qquad\epsilon\sim N(0,I),\quad\sigma_t>0.
$$

于是

$$
q_t(x\mid x_0)=N(a_tx_0,\sigma_t^2I),
$$

$$
\boxed{
s_t^{cond}(x,x_0)
=-\frac{x-a_tx_0}{\sigma_t^2}
=-\frac{\epsilon}{\sigma_t}.
}
$$

这给出三种等价 target 表达：

| 网络输出 | target | 转成 score |
|---|---|---|
| $s_\theta$ | $-\epsilon/\sigma_t$ | 已是 score |
| $\epsilon_\theta$ | $\epsilon$ | $s_\theta=-\epsilon_\theta/\sigma_t$ |
| $x_{0,\theta}$ | $x_0$ | $s_\theta=(a_tx_{0,\theta}-x_t)/\sigma_t^2$ |

“输出可以换算”不等于未加权 MSE 相同：乘除 $\sigma_t$ 会改变各时间层的 loss 权重与 gradient scale。

## 四、平方损失为什么只差常数

令

$$U=s_t^{cond}(X_t,X_0),\qquad
m(X_t,t)=\mathbb E[U\mid X_t,t]=s_t^{marg}(X_t).$$

对任意只依赖 $(X_t,t)$ 的 predictor $s_\theta$，写

$$U-s_\theta=(U-m)+(m-s_\theta).$$

平方并取期望：

$$
\begin{aligned}
\mathbb E\|U-s_\theta\|^2
&=\mathbb E\|U-m\|^2
+\mathbb E\|m-s_\theta\|^2\\
&\quad+2\mathbb E[(U-m)^\top(m-s_\theta)].
\end{aligned}
$$

交叉项为零，因为

$$
\begin{aligned}
&\mathbb E[(U-m)^\top(m-s_\theta)]\\
&=\mathbb E\left[
\mathbb E[U-m\mid X_t,t]^\top(m-s_\theta)
\right]=0.
\end{aligned}
$$

因此

$$
\boxed{
L_{cond}(\theta)=L_{marg}(\theta)+C,
\quad
C=\mathbb E\|U-m\|^2.
}
$$

$C$ 是不可约 conditional variance，与 $\theta$ 无关。于是对同一模型类，population loss 的 minimizer 和 gradient 完全相同；这不要求模型类能表示真实 score。真正不同来自 finite-sample estimator、mini-batch noise、parameterization、weighting 和 optimization path。

## 五、带权目标什么时候仍等价

若权重 $w(X_t,t)\ge0$ 只依赖模型输入，则条件正交性仍成立：

$$
\mathbb E[w\|U-s_\theta\|^2]
=\mathbb E[w\|m-s_\theta\|^2]
+\mathbb E[w\|U-m\|^2].
$$

若权重还依赖不可见的 $X_0$、target $U$、模型输出，或由同一 minibatch 做会与 target 相关的自归一化，交叉项未必为零，必须重新推导。时间采样分布 $r(t)$ 也属于总体目标定义的一部分；换 $r(t)$ 会改变共享网络在各噪声层的折中。

## 六、Gaussian 数据的常数差可以精确算出

取一维

$$X_0\sim N(0,\tau_0^2),\qquad X_t=aX_0+\sigma\epsilon.$$

边缘为 $N(0,a^2\tau_0^2+\sigma^2)$，所以

$$m(x)=-\frac{x}{a^2\tau_0^2+\sigma^2}.$$

conditional target 是 $U=-\epsilon/\sigma$。联合 Gaussian 条件方差为

$$
\operatorname{Var}(\epsilon\mid X_t)
=\frac{a^2\tau_0^2}{a^2\tau_0^2+\sigma^2}.
$$

故不可约常数

$$
\boxed{
C=\mathbb E\operatorname{Var}(U\mid X_t)
=\frac{a^2\tau_0^2}
{\sigma^2(a^2\tau_0^2+\sigma^2)}.
}
$$

当 $\sigma\to0$，conditional target 方差会爆大；即使 marginal score 很平滑，逐样本去噪 target 仍可能噪声很强。这解释了为什么时间权重、parameterization 与 sampling distribution 会显著影响训练方差。

## 七、从 score 到 denoiser：Tweedie 形式

由 score identity 可反推出 posterior mean。仍取

$$X_t=a_tX_0+\sigma_t\epsilon.$$

conditional score identity 给

$$
s_t^{marg}(x)
=\mathbb E\left[-\frac{x-a_tX_0}{\sigma_t^2}\mid X_t=x\right].
$$

整理：

$$
\boxed{
\mathbb E[X_0\mid X_t=x]
=\frac{x+\sigma_t^2s_t^{marg}(x)}{a_t},
\quad a_t\neq0.
}
$$

因此 score、posterior mean denoiser 与 noise predictor 在 Gaussian corruption 下互相换算。这里恢复的是 posterior mean，不是保证恢复产生该样本的唯一原始 $x_0$；多峰 posterior 会被平均。

## 八、为什么不直接估计 marginal score

形式上可用 batch 近似

$$
p_t(x)\approx\frac1B\sum_{i=1}^Bq_t(x\mid x_0^{(i)}),
$$

再对 log 求梯度。但这是随机分母的 ratio estimator：

$$
\frac{\sum_i\nabla q_i}{\sum_iq_i}
$$

通常有有限 batch bias，且每个 query $x$ 要与许多 $x_0^{(i)}$ 比较，成本高、在高维会有权重退化。conditional target 则每个数据样本只需一次 corruption，给出无偏 stochastic gradient（相对于标准 population objective），尽管 target variance 可能较大。

## 九、Score loss 与分布距离的边界

[[S-2022-Kwon-Wasserstein-Score]] 在明确 regularity、时间权重与 terminal 条件下建立 score error 到生成分布 $W_2$ 的上界。课程不把它缩写为

$$W_2\le L_{score}$$

这种无常数、无端点项的口号。还需区分：

1. population score error；
2. finite-data empirical loss；
3. exact continuous reverse process；
4. learned-score dynamics；
5. finite-step sampler。

[[S-2023-Su-9467-W距离与得分匹配]] 尤其值得研读：文章主动指出朴素推导中的一项控制并不成立。保留这种 proof gap 比强行补成“完整证明”更符合研究训练。

## 十、科学空间研读框

[[S-2023-Su-9509-得分匹配与条件得分匹配]] 的标题用“=”强调最佳 predictor 的一致性。逐段复核后，本节把它精确拆成：

- `[I]` marginal score 是 conditional score 的条件均值；
- `[I]` 标准平方 population loss 相差与模型无关常数；
- `[E]` 两种 Monte Carlo estimator 的偏差、方差和成本不同；
- `[boundary]` 标题等号不是逐样本相等，也不是两个 loss 数值相等。

去噪 score matching 的一级来源见 [[S-2011-Vincent-Denoising-Score-Matching]]；continuous score training 与 sampler 见 [[S-2021-Song-Score-SDE]]。

## 十一、图：条件 target 怎样投影成 marginal score

先看图回答：同一个 noisy point 可能来自多个 clean source 时，网络为什么输出箭头的平均，而不是记住某一条去噪箭头？

![[00-知识库管理/_assets/figures/generative-models/fig-conditional-marginal-score-projection-v1.svg|900]]

> [!figure] 图 50.7-04　conditional score、marginal score 与 $L^2$ 正交分解
> 左侧画同一 $x_t$ 的多条 conditional targets，中间画条件均值投影，右侧把 conditional loss 拆成 marginal loss 与不可约方差。来源：据条件期望投影恒等式独立绘制。

**怎样读图**：先看多条浅色 target 如何在固定 $x_t$ 下平均为深色 marginal arrow，再把几何正交三角形对应到平方损失三项。

**图没有证明什么**：图不证明有限 batch 梯度方差相同，不证明任意 target-dependent weighting 保持等价，也不证明 score MSE 单调决定 FID 或感知质量。

## 十二、本节回顾与训练

- conditional score 可算，marginal score 是其 posterior average；
- 标准平方目标相差常数，population gradient 相同；
- finite-sample estimator 的数值、方差与成本不相同；
- score、noise、denoiser 可换算，但 loss weighting 随尺度改变；
- 分布距离上界必须保留假设、常数、端点项和 solver 层；
- [[习题 - Marginal Score、Conditional Score 与去噪等价]]
- [[解答 - Marginal Score、Conditional Score 与去噪等价]]
