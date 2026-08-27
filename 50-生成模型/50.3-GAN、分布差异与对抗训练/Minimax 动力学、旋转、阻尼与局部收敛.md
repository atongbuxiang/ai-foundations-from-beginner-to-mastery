---
type: concept
status: verified
area: [generative-models, gan, game-dynamics]
node_id: GEN-22
prerequisites: ["[[Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]]", "[[非凸优化、鞍点与深度网络损失地形]]", "[[相图、平衡点与局部稳定性]]"]
related: ["[[GAN 稳定化方法、受控比较与证据地图]]", "[[Mode Collapse、模式覆盖与生成器熵]]"]
sources: ["[[S-2018-Mescheder-GAN-Convergence]]", "[[S-2017-Heusel-TTUR]]", "[[S-2016-Metz-Unrolled-GAN]]"]
exercises: ["[[习题 - Minimax 动力学、旋转、阻尼与局部收敛]]"]
solutions: ["[[解答 - Minimax 动力学、旋转、阻尼与局部收敛]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-gan-bilinear-rotation-damping-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Minimax 动力学、旋转、阻尼与局部收敛

> [!abstract] 本节主问题
> GAN 是两个参数块的 game，不是把所有 loss 相加后做普通最小化。即使最简单 bilinear game 只有一个 Nash 点，同步梯度下降—上升也会绕圈并离散发散。稳定化方法常通过改变向量场的旋转/阻尼，而不只是换一个“更好距离”。

## 一、向量场而非单目标梯度

对 $\min_\theta\max_\psi V(\theta,\psi)$，定义

$$
F(\theta,\psi)=
\begin{bmatrix}
\nabla_\theta V\\
-\nabla_\psi V
\end{bmatrix}.
$$

求解是找 $F=0$ 并满足相应局部 Nash/monotonicity 条件。$F$ 的 Jacobian 一般不对称，含 rotational component；通常不存在一个 scalar potential 使 $F=\nabla U$。

## 二、bilinear game 手算

考虑

$$
\min_x\max_y xy.
$$

同步 GDA：

$$
x_{t+1}=x_t-\eta y_t,\qquad
y_{t+1}=y_t+\eta x_t.
$$

矩阵

$$
\begin{bmatrix}x_{t+1}\\y_{t+1}\end{bmatrix}
=
\begin{bmatrix}1&-\eta\\\eta&1\end{bmatrix}
\begin{bmatrix}x_t\\y_t\end{bmatrix}.
$$

特征值 $1\pm i\eta$，模为 $\sqrt{1+\eta^2}>1$：任何固定正步长都向外螺旋。连续 ODE $\dot x=-y,\dot y=x$ 则守恒 $x^2+y^2$，只绕圈不收敛。

## 三、stationary、Nash、stable 不同

- stationary：$F=0$；
- local Nash：固定对手的小邻域内各自不可改善；
- dynamic stable：指定更新算法的扰动会回到点；
- global convergence：从广泛初值到目标集合。

一个点可以 stationary 却非 Nash，也可 Nash 却在某离散算法下不稳定。

## 四、阻尼与 look-ahead

Extragradient 先预测一步，再在预测点算修正 gradient；bilinear 情形可引入 inward component。Optimistic gradient、consensus optimization、R1/zero-centered penalty 与 unrolling 也会改变 Jacobian 的对称/反对称部分。

不能把它们统一说成“优化更准”：有些近似 best response，有些加阻尼，有些直接改变 game。

## 五、two time scales

TTUR 令生成器与 discriminator 使用不同 step-size sequences，使一方在另一方眼中近似快速平衡。理论需要 stochastic approximation 的步长、噪声、有界与局部稳定假设；工程中的 5 critic steps 或两个 Adam learning rates不自动满足全部条件。

## 六、局部理论的诚实外推

[[S-2018-Mescheder-GAN-Convergence]]展示低维/流形 support 下未正则 game 和有限 critic-update WGAN-GP 的反例，并给特定 zero-centered penalty 的局部收敛结论。它不能证明所有深层 GAN 全局收敛；但足以否定“用了 WGAN-GP 就总会收敛”。

## 七、诊断训练轨迹

至少记录：

- $F$ 的两块 gradient norm 与夹角；
- update-to-parameter norm；
- loss/critic gap 与 held-out classifier；
- generator/critic Jacobian 局部 eigenvalue 或 toy probe；
- 多 seed failure time、collapse/recovery；
- optimizer state、update ratio 与 EMA。

loss 平稳可能是极限环、饱和或双方停止学习。

## 八、图：旋转与阻尼

先看图回答：continuous bilinear flow 为什么不靠近原点？同步 Euler 为何越转越远？加入阻尼后 eigenvalue 实部/模发生什么？

![[00-知识库管理/_assets/figures/generative-models/fig-gan-bilinear-rotation-damping-v1.svg|900]]

> [!figure] 图 50.3-06　bilinear game 的旋转、离散发散与阻尼
> 图比较连续轨道、simultaneous GDA 螺旋和带 look-ahead/regularization 的 inward field。来源：依据线性 game 矩阵独立计算绘制。

**怎样读图**：先看向量场反对称部分产生旋转，再看 Euler 特征值模大于 1；阻尼必须对应指定算法和步长，不是抽象美化。

**图没有证明什么**：toy game 不证明某个 optimizer 在深网中全局收敛；它提供最小反例与局部诊断语言。

## 九、本节回顾

- game vector field 一般不是 scalar objective 的梯度；
- bilinear continuous flow 绕圈，同步 GDA 固定步长向外发散；
- stationary、Nash 与算法稳定性不同；
- extragradient、penalty、unrolling 和 TTUR 改变不同机制；
- 局部/简化模型定理不能外推为深网全局保证。

## 十、练习与独立详解

- [[习题 - Minimax 动力学、旋转、阻尼与局部收敛]]
- [[解答 - Minimax 动力学、旋转、阻尼与局部收敛]]
