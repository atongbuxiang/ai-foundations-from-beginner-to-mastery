---
type: concept
status: verified
area: [generative-models, gan, optimal-transport]
node_id: GEN-20
prerequisites: ["[[饱和、非饱和生成器损失与 f-GAN]]", "[[弱对偶、强对偶与 Slater 条件]]"]
related: ["[[Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]]", "[[Minimax 动力学、旋转、阻尼与局部收敛]]"]
sources: ["[[S-2019-Su-6280-Wasserstein距离与WGAN]]", "[[S-2021-Su-8244-WGAN成功与距离近似]]", "[[S-2017-Arjovsky-WGAN]]"]
exercises: ["[[习题 - IPM、Wasserstein-1 与 Kantorovich 对偶]]"]
solutions: ["[[解答 - IPM、Wasserstein-1 与 Kantorovich 对偶]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-gan-js-wasserstein-pointmass-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# IPM、Wasserstein-1 与 Kantorovich 对偶

> [!abstract] 本节主问题
> IPM 用一类 test functions 的期望差比较分布；$W_1$ 选择 1-Lipschitz functions，并等价于最小运输成本。它对 support 的空间距离敏感，因此在低维 support 平移时比 JS 更连续。但实践 neural critic 只近似 dual，训练成功不证明精确 $W_1$ 是唯一机制。

## 一、Integral Probability Metric

给函数类 $\mathcal F$：

$$
\gamma_{\mathcal F}(P,Q)
=\sup_{f\in\mathcal F}|E_Pf-E_Qf|.
$$

选择不同 $\mathcal F$：

- 所有 $\|f\|_\infty\le1$：与 total variation 常数倍相关；
- RKHS unit ball：MMD；
- 1-Lipschitz functions：$W_1$；
- neural critic class：neural IPM，依赖 architecture。

所以“critic loss”不是脱离函数类的唯一距离。

## 二、Wasserstein primal

在 metric space $(\mathcal X,d)$：

$$
W_1(P,Q)=\inf_{\pi\in\Pi(P,Q)}
\int d(x,y)\,d\pi(x,y).
$$

$\Pi(P,Q)$ 是所有边缘分别为 $P,Q$ 的 coupling。它问怎样把质量从 $P$ 搬到 $Q$，最少平均成本是多少。

## 三、Kantorovich–Rubinstein dual

在适当 Polish/finite-first-moment 条件下：

$$
\boxed{
W_1(P,Q)=
\sup_{\|f\|_{Lip}\le1}
\{E_Pf-E_Qf\}.}
$$

$f$ 是 Kantorovich potential/critic，不是概率分类器；可加任意常数而不改期望差。WGAN 通常最大化 empirical restricted version。

## 四、点质量反例：拓扑差异一眼看清

令 $P=\delta_0,Q_\theta=\delta_\theta$，ground metric 为绝对值。

若 $\theta\ne0$，supports 分离：

$$
JS(P,Q_\theta)=\log2,
$$

而

$$
W_1(P,Q_\theta)=|\theta|.
$$

当 $\theta\to0$，$Q_\theta$ 弱收敛到 $P$；$W_1\to0$，JS 却从 $\log2$ 在 $\theta=0$ 突跳到 0。这解释 $W_1$ 对空间邻近更敏感。

## 五、连续不等于平滑、可优化或好估计

$W_1(P_\theta,P_*)$ 对 $\theta$ 连续仍不保证：

- differentiable；
- finite neural critic 达到 dual optimum；
- empirical estimate sample-efficient；
- alternating optimizer 稳定；
- generator 不 collapse。

这些分别属于 analysis、approximation、statistics、dynamics 与 model capacity。

## 六、四层 WGAN objective

$$
W_1(P_*,P_\theta)
\quad\to\quad
\sup_{f\in\mathcal F_{Lip}}
\quad\to\quad
\sup_{\psi\in\Psi_{reg}}
\widehat E_{real}f_\psi-\widehat E_{fake}f_\psi
\quad\to\quad
f_{\psi_t}.
$$

weight clipping/GP/SN 定义的 $\Psi_{reg}$ 不同，有限 sample 与 finite updates 再引入 gap。

## 七、科学空间研读框

[[S-2019-Su-6280-Wasserstein距离与WGAN]]提供 coupling、dual 与 Lipschitz 的中文推导入口；[[S-2021-Su-8244-WGAN成功与距离近似]]提醒实际成功可能来自 regularization 与 training field，而不等于准确估计 population $W_1$。与[[S-2017-Arjovsky-WGAN]]对照后，本节采纳两者的交集：$W_1$ 的 topology 是定理，WGAN 工程因果需要消融。

## 八、图：点质量移动时两种差异

先看图回答：$\theta$ 从 1 连续移到 0 时，JS 和 $W_1$ 的曲线为何不同？哪一个需要 ground metric？

![[00-知识库管理/_assets/figures/generative-models/fig-gan-js-wasserstein-pointmass-v1.svg|900]]

> [!figure] 图 50.3-04　点质量平移下 JS 饱和与 $W_1$ 连续
> 左侧展示 disjoint supports；右侧给出 $JS(\delta_0,\delta_\theta)$ 与 $W_1(\delta_0,\delta_\theta)$。来源：依据定义独立计算并绘制。

**怎样读图**：JS 只看分布质量是否重叠，$W_1$ 还读取 ground distance。$\theta=0$ 是 JS 的跳点，却是 $W_1$ 的连续终点。

**图没有证明什么**：一维反例不证明所有 WGAN 实现稳定、sample-efficient 或优于其他 GAN；它只证明两种 topology 的差别。

## 九、本节回顾

- IPM 由 test-function class 决定；
- $W_1$ 同时有 coupling primal 与 1-Lipschitz dual；
- 点质量平移下 JS 饱和、$W_1=|\theta|$；
- metric continuity 不自动给 differentiability、estimation 或 game convergence；
- 实际 WGAN critic objective 是 population $W_1$ 的多层近似。

## 十、练习与独立详解

- [[习题 - IPM、Wasserstein-1 与 Kantorovich 对偶]]
- [[解答 - IPM、Wasserstein-1 与 Kantorovich 对偶]]
