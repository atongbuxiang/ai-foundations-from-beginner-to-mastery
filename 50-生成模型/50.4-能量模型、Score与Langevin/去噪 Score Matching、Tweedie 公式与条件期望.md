---
type: concept
status: verified
area: [generative-models, score-matching, denoising, conditional-expectation]
node_id: GEN-28
prerequisites: ["[[Score Matching、分部积分与配分函数消去]]", "[[协方差、相关性与条件期望]]"]
related: ["[[多噪声尺度、退火去噪与 Score 网络]]", "[[时间反演、score 与扩散生成动力学]]"]
sources: ["[[S-2019-Su-7038-从去噪自编码器到生成模型]]", "[[S-2023-Su-9509-得分匹配与条件得分匹配]]", "[[S-2011-Vincent-Denoising-Score-Matching]]"]
exercises: ["[[习题 - 去噪 Score Matching、Tweedie 公式与条件期望]]"]
solutions: ["[[解答 - 去噪 Score Matching、Tweedie 公式与条件期望]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-dsm-tweedie-projection-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 去噪 Score Matching、Tweedie 公式与条件期望

> [!abstract] 本节主问题
> 给干净数据加已知 Gaussian noise 后，conditional score 有解析式。它对 noisy observation 的条件期望恰是 marginal noisy-density score；因此用 conditional target 做平方回归，与直接学习未知 marginal score 有相同的总体最优 predictor。最优去噪器又等于 noisy input 加 $\sigma^2$ 倍 score，这就是 Tweedie 公式。

## 一、高斯加噪合同

令

$$
X\sim p_0,\qquad
Y=X+\sigma\varepsilon,\qquad
\varepsilon\sim\mathcal N(0,I_d),
$$

则条件密度

$$
q_\sigma(y\mid x)
=(2\pi\sigma^2)^{-d/2}
\exp\left(-\frac{\|y-x\|^2}{2\sigma^2}\right),
$$

边缘 noisy density 是卷积

$$
p_\sigma(y)=\int p_0(x)q_\sigma(y\mid x)dx.
$$

即便 $p_0$ 集中在低维流形，$\sigma>0$ 时 $p_\sigma$ 通常在全空间光滑且为正。

## 二、Conditional score 可直接计算

对 $y$ 求导：

$$
\boxed{
\nabla_y\log q_\sigma(y\mid x)
=-\frac{y-x}{\sigma^2}
=-\frac{\varepsilon}{\sigma}.}
$$

因此训练样本 $(x,\varepsilon,y)$ 一旦生成，target 就已知，不需要估计 $p_\sigma(y)$。

## 三、Marginal score 是 conditional score 的条件均值

在可交换梯度与积分时：

$$
\begin{aligned}
\nabla_y\log p_\sigma(y)
&=\frac{\int p_0(x)\nabla_yq_\sigma(y\mid x)dx}{p_\sigma(y)}\\
&=\int p(x\mid y)\nabla_y\log q_\sigma(y\mid x)dx\\
&=E\!\left[-\frac{Y-X}{\sigma^2}\middle|Y=y\right].
\end{aligned}
$$

记 $U=\nabla_Y\log q_\sigma(Y\mid X)$，则 $E[U\mid Y]=s_\sigma(Y)$。

## 四、为什么两个 MSE 有相同最优解

对任意 predictor $s(Y)$，条件期望的正交投影给

$$
\boxed{
E\|U-s(Y)\|^2
=E\|U-E[U\mid Y]\|^2
+E\|s_\sigma(Y)-s(Y)\|^2.}
$$

第一项与 $s$ 无关。所以 DSM objective

$$
E\left\|s_\theta(Y,\sigma)+\frac{Y-X}{\sigma^2}\right\|^2
$$

与 marginal score MSE 具有同一 population minimizer。两者的 loss 数值并不相等，而是相差不可约 conditional variance。

## 五、Tweedie 公式

由

$$
s_\sigma(y)=\frac{E[X\mid Y=y]-y}{\sigma^2}
$$

立即得到

$$
\boxed{E[X\mid Y=y]=y+\sigma^2s_\sigma(y).}
$$

平方误差去噪器的最优解正是 posterior mean，所以

$$
r^*(y)=y+\sigma^2s_\sigma(y).
$$

这不是说 $r^*(Y)$ 等于真实 $X$；posterior 有不确定性时，条件均值仍可能平滑或落在多个解释之间。

## 六、Score、噪声与干净样本参数化互换

在 Gaussian corruption 下：

$$
s_\theta(y,\sigma)
=-\frac{\varepsilon_\theta(y,\sigma)}{\sigma},
\qquad
\hat x_\theta(y,\sigma)
=y+\sigma^2s_\theta(y,\sigma)
=y-\sigma\varepsilon_\theta(y,\sigma).
$$

函数映射简单，但训练 loss 的权重、网络 preconditioning 与有限模型优化并不因重参数化自动等价。必须把 target scaling 与 $\lambda(\sigma)$ 一起比较。

## 七、一般协方差版本

若 $Y=X+\eta$、$\eta\sim N(0,\Sigma)$ 且 $\Sigma\succ0$，则

$$
E[X\mid Y=y]
=y+\Sigma\nabla_y\log p_Y(y).
$$

所以“乘 $\sigma^2$”来自 isotropic covariance，不是任意 corruption 的通式。

## 八、科学空间研读框

[[S-2019-Su-7038-从去噪自编码器到生成模型]]提供 denoiser—score—Langevin 的形象桥；[[S-2023-Su-9509-得分匹配与条件得分匹配]]强调两种 score loss 的关系。本节用 $L^2$ 投影补严标题中的等号：相同 minimizer，不是逐样本 target 相同，也不是有限训练表现必然相同。

## 九、图：条件目标如何投影成 marginal score

先看图回答：同一个 noisy point $y$ 可能来自多个 $x$；网络无法知道本次是哪一个，它的 MSE 最优输出是什么？

![[00-知识库管理/_assets/figures/generative-models/fig-dsm-tweedie-projection-v1.svg|900]]

> [!figure] 图 50.4-04　Gaussian corruption、条件期望投影与 Tweedie 去噪
> 左侧展示多个 clean ancestors 生成同一区域 noisy observation；中间把 conditional scores 平均成 marginal score；右侧沿 $\sigma^2s_\sigma(y)$ 得到 posterior-mean denoiser。来源：依据 Gaussian score 与条件期望恒等式独立绘制。

**怎样读图**：细箭头是每个潜在 clean source 的 conditional score，粗箭头是给定 $Y=y$ 后的 posterior 加权平均。去噪终点是条件均值，不保证落到任一真实 ancestor。

**图没有证明什么**：图不证明单次去噪恢复真实样本，不证明非 Gaussian corruption 仍乘 $\sigma^2$，也不证明有限网络同时在所有噪声尺度达到总体最优。

## 十、本节回顾

- Gaussian conditional score 是 $-(y-x)/\sigma^2$；
- marginal score 是 conditional score 给定 noisy observation 的条件均值；
- DSM 与 marginal score MSE 相差 predictor-independent 常数；
- Tweedie 公式把 posterior-mean denoiser 与 score 相连；
- score/noise/clean 参数化必须连同 loss weighting 一起审计。

## 十一、练习与独立详解

- [[习题 - 去噪 Score Matching、Tweedie 公式与条件期望]]
- [[解答 - 去噪 Score Matching、Tweedie 公式与条件期望]]
