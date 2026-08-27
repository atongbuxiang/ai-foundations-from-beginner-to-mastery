---
type: derivation
status: verified
area: [generative-models, diffusion, parameterization]
node_id: GEN-43
prerequisites: ["[[DDPM 前向 Markov 加噪与闭式边缘]]", "[[去噪 Score Matching、Tweedie 公式与条件期望]]"]
related: ["[[扩散简化损失、时间加权、Schedule 与 SNR]]", "[[DDPM 反向后验、ELBO 与逐步 KL]]"]
sources: ["[[S-2022-Su-9164-DDPM贝叶斯去噪]]", "[[S-2020-Ho-DDPM]]", "[[S-2022-Salimans-Ho-Progressive-Distillation]]"]
exercises: ["[[习题 - 数据、噪声、速度与 Score 参数化]]"]
solutions: ["[[解答 - 数据、噪声、速度与 Score 参数化]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-ddpm-parameterization-rotation-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 数据、噪声、速度与 Score 参数化

> [!abstract] 一句话结论
> 在固定噪声层 $t$，$x_t=a_tx_0+\sigma_t\epsilon$ 是二维旋转/混合关系，因此预测 $x_0$、噪声 $\epsilon$、velocity $v$ 或 marginal score 可以代数互换。但换算中的 $a_t,\sigma_t$ 会重标误差；相同函数类与统一权重下的 finite optimization 并不自动等价。

## 一、统一短记号

定义

$$a_t=\sqrt{\bar\alpha_t},\qquad
\sigma_t=\sqrt{1-\bar\alpha_t},\qquad
a_t^2+\sigma_t^2=1.$$

forward sample 为

$$x_t=a_tx_0+\sigma_t\epsilon,\qquad \epsilon\sim N(0,I).$$

所有对象 $x_t,x_0,\epsilon,v$ 形状相同；$a_t,\sigma_t$ 对 batch 广播。

## 二、noise 与 data prediction

若网络预测 $\hat\epsilon$，则

$$
\boxed{\hat x_0=\frac{x_t-\sigma_t\hat\epsilon}{a_t}.}
$$

若网络预测 $\hat x_0$，则

$$
\boxed{\hat\epsilon=\frac{x_t-a_t\hat x_0}{\sigma_t}.}
$$

边界立刻可见：$a_t\to0$ 时从 noise 恢复 data 会除以小数；$\sigma_t\to0$ 时从 data 恢复 noise 会除以小数。clipping $\hat x_0$ 会使换算不再是无损线性等价。

## 三、velocity parameterization 是一个正交旋转

定义

$$
\boxed{v_t=a_t\epsilon-\sigma_tx_0.}
$$

于是

$$
\begin{pmatrix}x_t\\v_t\end{pmatrix}
=\begin{pmatrix}a_t&\sigma_t\\-\sigma_t&a_t\end{pmatrix}
\begin{pmatrix}x_0\\\epsilon\end{pmatrix}.
$$

矩阵正交，inverse 是 transpose：

$$
\boxed{x_0=a_tx_t-\sigma_tv_t,
\qquad \epsilon=\sigma_tx_t+a_tv_t.}
$$

因此在 $a_t^2+\sigma_t^2=1$ 的 VP convention 下，$(x_t,v_t)$ 与 $(x_0,\epsilon)$ 保存相同欧氏能量。[[S-2022-Salimans-Ho-Progressive-Distillation]]在少步稳定性/蒸馏语境中采用这类 parameterization。

## 四、score 与 noise 的条件期望关系

对 $q_t(x_t)=\int q(x_t\mid x_0)q_{data}(x_0)dx_0$，marginal score 为

$$s^*(x_t,t)=\nabla_{x_t}\log q_t(x_t).$$

Gaussian conditional score 是

$$\nabla_{x_t}\log q(x_t\mid x_0)
=-\frac{x_t-a_tx_0}{\sigma_t^2}=-\frac\epsilon{\sigma_t}.$$

由 conditional-score projection，

$$
\boxed{s^*(x_t,t)=-\frac{E[\epsilon\mid x_t]}{\sigma_t}.}
$$

所以训练 noise MSE 的 Bayes optimum $\epsilon^*(x_t,t)=E[\epsilon\mid x_t]$ 可换为 score。单个训练 pair 的真实 $\epsilon$ 不是 marginal score；必须经过条件期望。

## 五、四种 Bayes optimum

平方损失下：

$$x_0^*(x_t,t)=E[x_0\mid x_t],
\qquad \epsilon^*(x_t,t)=E[\epsilon\mid x_t],$$

$$v^*(x_t,t)=E[v\mid x_t],
\qquad s^*(x_t,t)=-\epsilon^*(x_t,t)/\sigma_t.$$

因为条件期望线性，它们可按上节公式换算。但这是 unrestricted population optimum 的关系；共享参数网络对所有 $t$ 训练时，loss weighting 会改变容量如何分配。

## 六、误差权重怎样变化

由

$$\hat\epsilon-\epsilon=-\frac{a_t}{\sigma_t}(\hat x_0-x_0),$$

得到

$$
\|\hat\epsilon-\epsilon\|^2
=\operatorname{SNR}_t\|\hat x_0-x_0\|^2.
$$

又因 $\hat s-s^*=-(\hat\epsilon-\epsilon)/\sigma_t$，

$$\|\hat s-s^*\|^2
=\frac1{\sigma_t^2}\|\hat\epsilon-\epsilon\|^2.$$

所以“都用 uniform timestep + unweighted MSE”时，四种 parameterization 实际强调的噪声区间不同。

## 七、标量手算

取 $a=0.8,\sigma=0.6,x_0=2,\epsilon=-1$。则 $x_t=1.0$，

$$v=0.8(-1)-0.6(2)=-2.$$

inverse 检查：

$$x_0=0.8(1)-0.6(-2)=2,
\qquad \epsilon=0.6(1)+0.8(-2)=-1.$$

score target 为 $-\epsilon/\sigma=5/3$，这是 conditional score target；marginal optimum仍需对给定 $x_t$ 的数据 posterior 平均。

## 八、科学空间研读框

[[S-2022-Su-9164-DDPM贝叶斯去噪]]用 Bayes 和 denoising 串起 $x_0/\epsilon$；本节补上 velocity 的正交旋转和 marginal score 的条件期望。博客/实现若直接把单样本 $-\epsilon/\sigma$ 叫“真实数据 score”，必须补上“DSM conditional target，其回归最优点为 marginal score”。

## 九、图：四种输出头如何共享同一统计对象

先看图回答：哪些箭头是逐样本代数恒等，哪一条箭头必须经过条件期望才到 marginal score？

![[00-知识库管理/_assets/figures/generative-models/fig-ddpm-parameterization-rotation-v1.svg|900]]

> [!figure] 图 50.6-03　$x_0$、$\epsilon$、$v$ 的正交旋转与 score 投影
> 左侧是逐样本线性换算，右侧单独标出 $E[\epsilon\mid x_t]$ 后才得到 marginal score。来源：据 VP diffusion parameterization 与 DSM identity 独立绘制。

**怎样读图**：实线表示给定 $a_t,\sigma_t,x_t$ 的代数换算；虚线表示 population regression/条件期望。靠近端点时注意小分母与 clipping。

**图没有证明什么**：图不证明四个训练 loss 有相同 gradient、conditioning 或有限网络误差，也不证明 velocity 在所有 schedule/架构上经验最优。

## 十、本节回顾与训练

- $x_t,v$ 是 $x_0,\epsilon$ 的正交旋转；
- score 等于 conditional noise 的期望再除以 $-\sigma_t$；
- algebraic equivalence、Bayes-optimum equivalence 与 training equivalence 是三层；
- 小 $a_t/\sigma_t$ 和 clipping 会破坏数值上的对称；
- [[习题 - 数据、噪声、速度与 Score 参数化]]
- [[解答 - 数据、噪声、速度与 Score 参数化]]

