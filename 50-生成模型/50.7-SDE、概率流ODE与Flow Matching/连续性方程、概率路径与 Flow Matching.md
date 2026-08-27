---
type: derivation
status: verified
area: [generative-models, flow-matching, continuity-equation, cnf]
node_id: GEN-53
prerequisites: ["[[连续性方程与守恒律]]", "[[流映射、Liouville 公式与连续正规化流]]", "[[Marginal Score、Conditional Score 与去噪等价]]"]
related: ["[[Conditional Flow Matching、Coupling 与最优传输路径]]", "[[Probability-flow ODE 与共享边缘分布]]", "[[Rectified Flow、ReFlow 与轨迹直化]]"]
sources: ["[[S-2022-Su-9280-硬刚扩散ODE]]", "[[S-2022-Su-9370-构建ODE一般步骤上]]", "[[S-2022-Su-9379-构建ODE一般步骤中]]", "[[S-2023-Lipman-Flow-Matching]]"]
exercises: ["[[习题 - 连续性方程、概率路径与 Flow Matching]]"]
solutions: ["[[解答 - 连续性方程、概率路径与 Flow Matching]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-continuity-flow-matching-weak-proof-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 连续性方程、概率路径与 Flow Matching

> [!abstract] 一句话结论
> Flow Matching 先指定一条连接数据与参考分布的 probability path $p_t$，再学习满足 $\partial_tp_t+\nabla\cdot(p_tv_t)=0$ 的 velocity field。直接的 marginal velocity 往往不可得，于是为可采样的条件路径构造速度 $U_t$；其给定 $X_t=x$ 的条件均值 $v_t(x)=E[U_t\mid X_t=x]$ 自动满足同一连续性方程。平方回归因此是 simulation-free 的 CNF 训练方法，但生成仍要数值求解 ODE。

## 一、先区分三个对象

初学 Flow Matching 最容易把“路径”一词混成一件事。本节固定：

| 对象 | 记号 | 含义 |
|---|---|---|
| 概率路径 | $(p_t)_{t\in[0,1]}$ | 每个时间截面的分布 |
| 样本轨迹 | $t\mapsto X_t(\omega)$ | 某个随机样本如何随时间移动 |
| 速度场 | $v_t(x)$ | ODE 到达位置 $x$ 时的瞬时方向 |

同一概率路径可由许多不同 trajectory couplings 和 velocity fields 实现。指定 $p_0,p_1$ 更不够；还要选中间 $p_t$，并决定用什么可训练结构产生它。

本卷统一以 $p_0=p_{data}$、$p_1=p_{ref}$ 讨论 forward path；生成从 $t=1$ 反向积分到 $t=0$。部分 Flow Matching 文献用相反端点，阅读时先做方向翻译。

## 二、从粒子 ODE 到连续性方程

假设粒子满足

$$
\frac{dX_t}{dt}=v_t(X_t),
$$

并且 $X_t$ 的密度为 $p_t$。取光滑紧支撑 test function $\varphi$，链式法则给

$$
\frac{d}{dt}\varphi(X_t)=\nabla\varphi(X_t)^\top v_t(X_t).
$$

取期望：

$$
\frac{d}{dt}\int\varphi(x)p_t(x)dx
=\int\nabla\varphi(x)^\top v_t(x)p_t(x)dx.
$$

若边界通量消失，分部积分：

$$
\int\nabla\varphi^\top(p_tv_t)dx
=-\int\varphi\,\nabla\cdot(p_tv_t)dx.
$$

另一方面，左侧为 $\int\varphi\,\partial_tp_tdx$。因此对所有 test function，

$$
\boxed{\partial_tp_t+\nabla\cdot(p_tv_t)=0.}
$$

这叫连续性方程。用 test function 推导有两个优点：

1. 不必先假设每处都有 classical derivative，可在 weak sense 讨论；
2. 清楚显示需要处理 integrability、边界通量和交换导数/期望。

## 三、只给 $p_t$，速度一般不唯一

连续性方程只给一个标量约束，却要求解 $d$ 个速度分量。若 $w_t$ 满足

$$\nabla\cdot(p_tw_t)=0,$$

则 $v_t+w_t$ 与 $v_t$ 运输同一个 $p_t$。高维中可以加入旋转 current 而不改变 density snapshots。

因此 Flow Matching 的完整设计不是“任取 $p_t$ 然后自动得到唯一 $v_t$”，而是：

1. 选择 endpoint coupling/latent；
2. 选择易采样 conditional probability path；
3. 得到相应 conditional velocity；
4. 通过条件平均选出一个 marginal velocity。

## 四、Conditional path 怎样产生 marginal path

令 $Z$ 汇总训练时可观察的 latent 信息，例如端点对 $(X_0,X_1)$ 和额外噪声。给定 $Z=z$，构造一条可微 conditional trajectory

$$X_t=\phi_t(z),$$

其瞬时条件速度为

$$U_t(z)=\partial_t\phi_t(z).$$

当 $Z$ 随训练 joint law 采样时，$X_t=\phi_t(Z)$ 诱导边缘 $p_t$。定义

$$
\boxed{v_t(x)=\mathbb E[U_t(Z)\mid X_t=x].}
$$

下面不靠口号，直接证明它运输 $p_t$。

## 五、Conditional-to-marginal 的弱证明

对任意 test function $\varphi$：

$$
\begin{aligned}
\frac{d}{dt}\mathbb E[\varphi(X_t)]
&=\mathbb E[\nabla\varphi(X_t)^\top U_t]\\
&=\mathbb E\left[
\nabla\varphi(X_t)^\top
\mathbb E[U_t\mid X_t]
\right]\\
&=\mathbb E[\nabla\varphi(X_t)^\top v_t(X_t)]\\
&=\int\nabla\varphi(x)^\top v_t(x)p_t(x)dx.
\end{aligned}
$$

这正是连续性方程的弱形式。所以在所需可积、可微和边界条件下，条件平均场 $v_t$ 运输 conditional construction 所诱导的 marginal path。

证明中最关键的一步不是神经网络，而是 tower property：把训练时依赖 $Z$ 的速度投影到生成时只观察 $(X_t,t)$ 的信息上。

## 六、Flow Matching 与 Conditional Flow Matching loss

若 marginal velocity $v_t(x)$ 可得，理想 Flow Matching objective 是

$$
L_{FM}(\theta)
=\mathbb E_{t,X_t\sim p_t}
\|v_\theta(X_t,t)-v_t(X_t)\|^2.
$$

但 $v_t$ 往往需要难算的 posterior average。可采样目标是

$$
L_{CFM}(\theta)
=\mathbb E_{t,Z}
\|v_\theta(\phi_t(Z),t)-U_t(Z)\|^2.
$$

由 GEN-52 同一个 $L^2$ 投影分解：

$$
\boxed{
L_{CFM}(\theta)
=L_{FM}(\theta)
+\mathbb E\|U_t-v_t(X_t)\|^2.
}
$$

最后一项与 $\theta$ 无关。因此标准 population setting 下二者对同一模型类有相同梯度和 minimizer。注意它们的 sample loss 不相等；CFM target 的 conditional variance 会直接影响 SGD 噪声。

## 七、Gaussian conditional path 的通用公式

一种重要构造是

$$
X_t=\alpha(t)X_0+\sigma(t)\epsilon,
\qquad\epsilon\sim N(0,I).
$$

条件速度直接求导：

$$
U_t=\dot\alpha(t)X_0+\dot\sigma(t)\epsilon.
$$

所以 marginal velocity 是

$$
v_t(x)=\dot\alpha\,\mathbb E[X_0\mid X_t=x]
+\dot\sigma\,\mathbb E[\epsilon\mid X_t=x].
$$

Gaussian score identities 给

$$
\mathbb E[\epsilon\mid X_t=x]=-\sigma s_t(x),
$$

$$
\mathbb E[X_0\mid X_t=x]
=\frac{x+\sigma^2s_t(x)}{\alpha},
\qquad\alpha\neq0.
$$

代入：

$$
\boxed{
v_t(x)=
\frac{\dot\alpha}{\alpha}x
+\left(
\frac{\dot\alpha\sigma^2}{\alpha}
-\dot\sigma\sigma
\right)s_t(x).
}
$$

这说明 diffusion probability path 的 Flow Matching velocity 可以写成 score 的线性组合；反过来也可从 velocity 恢复 score，只要系数不退化。所谓统一依赖于同一 $p_t$ 与正确系数，不是把两个网络输出名字互换。

## 八、一个最小 Gaussian 检查

取 $X_0\sim N(0,I)$、$\epsilon\sim N(0,I)$ 独立，令

$$\alpha(t)=\sqrt{1-t},\qquad\sigma(t)=\sqrt t.$$

此时 $X_t\sim N(0,I)$ 对所有 $t$ 不变，所以可取 marginal velocity $v_t(x)=0$。

条件速度却是

$$
U_t=-\frac{X_0}{2\sqrt{1-t}}
+\frac{\epsilon}{2\sqrt t},
$$

通常不为零。条件于 $X_t=x$ 后两部分恰好抵消。这是最简明的反例：**conditional trajectories 在动，marginal density 可以完全不动；网络学的是条件平均场，不是逐条 teacher velocity。**

端点附近 $\dot\alpha,\dot\sigma$ 发散也提示：同一 density path 的时间 parameterization 会改变回归 target 与 solver 难度。

## 九、“Simulation-free” 的准确含义

CFM 训练每次可执行：

1. 采 $t\sim r(t)$；
2. 采 latent/端点 $Z$；
3. 直接算 $X_t=\phi_t(Z)$ 和 $U_t=\partial_t\phi_t(Z)$；
4. 回归 $v_\theta(X_t,t)$ 到 $U_t$。

无需先把 learned ODE 从端点积分到 $t$ 再计算 loss，所以称 simulation-free training。但：

- 生成仍要解 $dX/dt=v_\theta$；
- likelihood 仍要积分 divergence；
- 若 conditional path 本身来自昂贵 OT/SB solver，目标构造并不一定便宜；
- finite-NFE error 没有因训练 simulation-free 而消失。

## 十、端点与正则性边界

若真实数据集中在低维流形，$p_0$ 可能没有 Lebesgue density；某些 Gaussian path 在 $t>0$ 会平滑，但 $t\to0$ 的 score/velocity 可能变大。实践中常用 $\sigma_{min}>0$、端点截断或 time weighting。

连续性方程的弱解可以容纳较低正则性，但要由 ODE flow 逐样本生成，还需 velocity 的存在唯一性条件。仅验证训练 loss 不能自动证明全局 Lipschitz、无 blow-up 或 invertible flow。

## 十一、科学空间研读框

三篇文章形成很好的递进：

- [[S-2022-Su-9280-硬刚扩散ODE]]：从 Jacobian/density 小步变化看到 continuity；
- [[S-2022-Su-9370-构建ODE一般步骤上]]：把 density path 写成时空守恒场，并暴露 velocity 不唯一；
- [[S-2022-Su-9379-构建ODE一般步骤中]]：用 conditional path/characteristic line 构造可回归速度。

本节把这条中文主线重写成 test-function 弱证明，并与 [[S-2023-Lipman-Flow-Matching]] 的 FM/CFM 定义对齐。博客中的直线条件路径保留为训练构造，不升级为“群体 trajectory 必为直线”。

## 十二、图：从粒子路径到弱连续性方程

先看图回答：为什么对所有 test function 都成立的期望导数，足以说明条件平均 velocity 正确运输 marginal density？

![[00-知识库管理/_assets/figures/generative-models/fig-continuity-flow-matching-weak-proof-v1.svg|900]]

> [!figure] 图 50.7-05　Flow Matching 的弱证明：conditional paths → 条件平均场 → marginal transport
> 左侧画可采样 conditional paths，中间按当前位置做条件平均，右侧以 test-function identity 验证连续性方程。来源：据连续性方程弱形式和 Flow Matching 定义独立绘制。

**怎样读图**：先沿单条浅色路径读 $U_t$，再在同一位置汇总为深色 $v_t$，最后检查 test function 的期望变化只依赖深色平均场。

**图没有证明什么**：图不证明 velocity 唯一，不证明网络达到 population minimizer，也不证明有限 NFE 的轨迹精确实现所画 density path。

## 十三、本节回顾与训练

- probability path、conditional trajectory 与 marginal velocity 是三层对象；
- 连续性方程由 test-function 链式法则和分部积分得到；
- conditional average velocity 通过 tower property 运输 marginal path；
- CFM 与 FM population loss 相差不可约 conditional variance；
- simulation-free 限定训练，不取消生成时 solver；
- [[习题 - 连续性方程、概率路径与 Flow Matching]]
- [[解答 - 连续性方程、概率路径与 Flow Matching]]
