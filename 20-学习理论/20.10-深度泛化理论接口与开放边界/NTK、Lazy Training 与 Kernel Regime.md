---
type: theorem
status: draft
area: [learning-theory/deep-generalization, neural-tangent-kernel, lazy-training]
aliases: [Neural Tangent Kernel, Lazy Regime, Kernel Regime]
node_id: LT-82
prerequisites: ["[[神经网络容量与 Norm-Based Bound]]", "[[正定核、RKHS 与表示定理]]", "[[一阶最优性条件与梯度下降]]"]
related: ["[[核岭回归与 Gaussian Process 接口]]", "[[Mean-Field、Feature Learning 与训练 Regime]]", "[[隐式偏置、最大间隔与优化选择]]"]
sources: ["[[S-2018-Jacot-NTK]]", "[[S-2019-Lee-Wide-Linear]]", "[[S-2019-Chizat-Lazy-Training]]"]
exercises: ["[[习题 - NTK、Lazy Training 与 Kernel Regime]]"]
solutions: ["[[解答 - NTK、Lazy Training 与 Kernel Regime]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-ntk-lazy-kernel-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# NTK、Lazy Training 与 Kernel Regime

> [!abstract] 本章主问题
> 什么时候一个非线性神经网络在训练中等价于“初始化处固定特征上的核方法”？NTK 把梯度流写成函数值上的核动力学；lazy training 进一步要求 Jacobian/核在训练中几乎不变。它能严谨解释某些宽网的优化，却不能自动解释 feature learning 或测试泛化。

## 一、学习目标

完成本章后，应能：

1. 从参数梯度定义 empirical NTK；
2. 推导平方损失下训练预测的精确核动力学；
3. 在线性化/固定核假设下解出矩阵指数；
4. 推导 kernel interpolation 的测试点公式；
5. 区分 NNGP kernel 与 NTK；
6. 区分 infinite width、lazy training 与 mere overparameterization；
7. 说明参数化、初始化、学习率与极限顺序的重要性；
8. 用 kernel drift 检查有限宽训练是否离开 tangent regime；
9. 区分 optimization theorem 与 generalization theorem；
10. 说明 NTK 对 feature reuse/transfer 的解释边界。

## 二、从一阶线性化开始

对标量输出网络 $f_\theta(x)$，在初始化 $\theta_0$ 附近做 Taylor 展开：

$$
f_\theta(x)
=f_{\theta_0}(x)
+\nabla_\theta f_{\theta_0}(x)^\top(\theta-\theta_0)
+O(\|\theta-\theta_0\|^2).
$$

记 tangent feature

$$
\varphi_{\theta_0}(x)=\nabla_\theta f_{\theta_0}(x).
$$

若训练路径一直使高阶余项可忽略，网络就像固定 feature map $\varphi_{\theta_0}$ 上的线性模型。

## 三、Empirical Neural Tangent Kernel

任意时刻定义

$$
\boxed{
K_{\theta}(x,x')
=\left\langle\nabla_\theta f_\theta(x),
\nabla_\theta f_\theta(x')\right\rangle.
}
$$

在训练集 $X=(x_1,\ldots,x_n)$ 上，令 Jacobian $J_\theta\in\mathbb R^{n\times P}$ 的第 $i$ 行为 $\nabla_\theta f_\theta(x_i)^\top$，则 Gram matrix

$$
K_\theta(X,X)=J_\theta J_\theta^\top\succeq0.
$$

它是数据依赖、参数化依赖且通常随时间变化的核。

## 四、平方损失下的精确函数动力学

取

$$
L(\theta)=\frac12\|f_\theta(X)-y\|_2^2.
$$

gradient flow 为

$$
\dot\theta_t=-J_t^\top(f_t(X)-y).
$$

再用链式法则：

$$
\dot f_t(X)=J_t\dot\theta_t
=-J_tJ_t^\top(f_t(X)-y).
$$

所以精确地有

$$
\boxed{
\dot f_t(X)=-K_t\bigl(f_t(X)-y\bigr).
}
$$

注意：到这里尚未假定 infinite width，也没有假定 $K_t$ 固定。

## 五、Lazy Regime：固定初始化核

令 residual $r_t=f_t(X)-y$。若在训练期间

$$
K_t\approx K_0,
$$

则近似线性 ODE：

$$
\dot r_t=-K_0r_t.
$$

解为

$$
\boxed{r_t=e^{-K_0t}r_0.}
$$

若 $K_0=Q\Lambda Q^\top$，则第 $j$ 个 eigenmode 按 $e^{-\lambda_jt}$ 衰减。大 eigenvalue 模式先学，小 eigenvalue 模式慢；若 $\lambda_{\min}(K_0)>0$，

$$
\|r_t\|\le e^{-\lambda_{\min}t}\|r_0\|.
$$

这是优化收敛结论，不是 test-risk 结论。

## 六、测试点的 Kernel Interpolant

固定核时，对任意测试点 $x$：

$$
\dot f_t(x)=-k_0(x,X)r_t,
$$

其中 $k_0(x,X)=[K_0(x,x_1),\ldots,K_0(x,x_n)]$。积分得到（假设 $K_0$ 可逆）：

$$
\boxed{
f_\infty(x)=f_0(x)+k_0(x,X)K_0^{-1}(y-f_0(X)).
}
$$

若 Gram matrix 奇异，应使用 pseudoinverse，并检查 residual 是否位于可学习子空间。初始化输出 $f_0$ 不是总能随意丢弃；不同 parameterization 下它可能保留为非零 prior function。

## 七、NNGP 与 NTK 不要混淆

| 对象 | 来源 | 主要描述 |
|---|---|---|
| NNGP kernel | 随机初始化下函数值 covariance | 训练前函数分布/高斯过程极限 |
| NTK | 参数梯度的 Gram | gradient training 的 tangent dynamics |

两者对同一 architecture 可递推计算，但通常不是同一个 kernel。只说“无限宽网络等于 GP/核”而不说明是初始化分布还是训练动力学，会混合两个不同结论。

## 八、为何大宽度可稳定 Kernel

在特定 NTK parameterization、随机初始化和适当 learning-rate/time scaling 下，各 neuron 的单次变化很小，大量独立贡献使 empirical kernel 集中到 deterministic limit $K_\infty$；若训练路径不离开初始化邻域，$K_t$ 继续接近 $K_0$。

逻辑链是：

$$
\text{width concentration}
\Rightarrow K_0\approx K_\infty,
\qquad
\text{small controlled movement}
\Rightarrow K_t\approx K_0.
$$

“参数很多”本身没有推出任何一个箭头。scale factor、每层方差、learning rate、训练时间和先取 $m\to\infty$ 还是 $t\to\infty$ 都会改变极限。

## 九、何谓 Lazy，而不只是“小移动”

raw parameter displacement 会随坐标缩放改变。更直接的函数诊断包括：

$$
d_K(t)=\frac{\|K_t-K_0\|_F}{\|K_0\|_F},
$$

线性化误差

$$
e_{\rm lin}(t)=
\frac{\|f_{\theta_t}(X)-f_{\rm lin,t}(X)\|}
{\|f_{\theta_t}(X)-f_{\theta_0}(X)\|+\varepsilon},
$$

以及 feature covariance/representation similarity。$d_K$ 小而线性化误差小，才为 kernel regime 提供直接证据。

## 十、Kernel Dynamics 不自动给 Generalization

即使训练完全等于 kernel regression，测试误差仍取决于：

- target 在 kernel eigenfunctions 上的 alignment；
- eigenvalue decay 与 effective dimension；
- noise、regularization 与 early stopping；
- train/test distribution；
- $K^{-1}$ 对小 eigenvalues 的放大。

因此完整链条为

$$
\text{network dynamics}\approx\text{kernel dynamics}
\quad+\quad
\text{kernel statistical theorem}
\Longrightarrow\text{risk guarantee}.
$$

第一项不能代替第二项。

## 十一、Feature Learning 的边界

固定 tangent feature 意味着网络主要重新组合初始化特征。对需要 pretraining 后迁移、学习新的 invariance 或改变 representation geometry 的任务，这可能不够。NTK 仍可作为：

1. 可解的 optimization baseline；
2. 识别“只靠随机特征能做到多少”的对照；
3. early-training/local linearization；
4. 检查 finite network 何时发生 kernel drift 的零假设。

说“实际网络不是完全 lazy”不抹去这些价值；说“无限宽 theorem 成立”也不证明它解释了实际 representation learning。

## 十二、图：固定核如何控制训练模式

先看图回答：训练误差指数下降，为什么测试误差仍可能很差？

![[00-知识库管理/_assets/figures/learning-theory/fig-ntk-lazy-kernel-v2.svg|900]]

> [!figure] 图 20.10-06　线性化、NTK 模式衰减与 kernel-regime 审计
> 左栏从 Jacobian 构造 NTK；中栏按 kernel eigenmodes 展示 residual 衰减和插值解；右栏区分初始化集中、训练 kernel drift 与统计风险桥。来源：依据 Jacot–Gabriel–Hongler、Lee et al. 与 Chizat–Oyallon–Bach 独立绘制；由 [[plot_deep_generalization_part2_v2.py]] 确定性生成。

**怎样读图**：先从精确时变核方程出发，再额外验证 $K_t\approx K_0$，最后调用 kernel statistical theory。

**图没有证明什么**：它没有证明任意 finite-width network、任意 learning rate 或任意训练时长都处于 lazy regime。

## 十三、AI 接口

- wide MLP/CNN：比较 finite network 与 analytical/empirical NTK；
- transfer learning：若预训练表示显著改变，固定随机 tangent baseline 应落后；
- kernel regression：NTK eigen-spectrum连接样本效率与 noise amplification；
- pruning/LoRA：tangent subspace 可描述局部可训练方向，但会随适配过程漂移；
- large language models：规模大不等于已满足 infinite-width fixed-kernel scaling；
- adversarial/OOD：in-distribution kernel interpolation 不给 shift guarantee。

## 十四、常见错误

1. 把 NNGP 与 NTK 当同一核；
2. 从 $K_t$ 的精确方程跳过“固定核”假设；
3. 把 training convergence 当 generalization；
4. 忽略 $f_0$；
5. 只测 raw parameter movement；
6. 不写 parameterization 与 learning-rate scaling；
7. 把 infinite width 与 finite wide 混为一谈；
8. 用 NTK 结论解释所有 feature learning。

## 十五、最小记忆与掌握标准

> [!summary]
> - $K_\theta=J_\theta J_\theta^\top$；
> - 平方损失精确给出 $\dot f=-K_t(f-y)$；
> - lazy 假设 $K_t\approx K_0$ 后，$r_t=e^{-K_0t}r_0$；
> - eigenvalues 控制训练模式速度，不直接控制 test target alignment；
> - kernel drift、linearization error 与统计风险必须分别验收。

能定义 NTK（A）、手算两点 kernel dynamics（B）、推导矩阵指数和测试插值式（C）、审计“无限宽=泛化好”（D），并设计 lazy-vs-feature-learning 实验（E）。

## 十六、练习与独立详解

- [[习题 - NTK、Lazy Training 与 Kernel Regime]]
- [[解答 - NTK、Lazy Training 与 Kernel Regime]]

## 参考来源

- [[S-2018-Jacot-NTK]]
- [[S-2019-Lee-Wide-Linear]]
- [[S-2019-Chizat-Lazy-Training]]

