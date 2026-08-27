---
type: theorem
status: draft
area: [learning-theory/deep-generalization, mean-field, feature-learning]
aliases: [Mean-Field Neural Networks, Feature Learning Regime, Distributional Dynamics]
node_id: LT-83
prerequisites: ["[[NTK、Lazy Training 与 Kernel Regime]]", "[[连续性方程与守恒律]]", "[[Fokker-Planck 方程与概率流 ODE]]"]
related: ["[[表示学习的任务、表示与下游风险]]", "[[流映射、Liouville 公式与连续正规化流]]", "[[深度泛化证据地图与开放问题]]"]
sources: ["[[S-2018-Mei-Mean-Field]]", "[[S-2019-Chizat-Lazy-Training]]", "[[S-2021-Yang-Hu-Feature-Learning]]"]
exercises: ["[[习题 - Mean-Field、Feature Learning 与训练 Regime]]"]
solutions: ["[[解答 - Mean-Field、Feature Learning 与训练 Regime]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-mean-field-feature-learning-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Mean-Field、Feature Learning 与训练 Regime

> [!abstract] 本章主问题
> 宽度趋于无穷时，神经网络是否只能退化为固定核？不是。另一类 scaling 把大量 neuron 看成相互作用粒子，有限维权重的经验分布演化为确定性的 measure-valued dynamics；此时特征可以发生 order-one 的集体重排。但“mean-field”是一种极限对象，不是“网络真的理解了数据”的同义词。

## 一、学习目标

完成本章后，应能：

1. 把两层网络重写为参数经验测度的积分；
2. 从粒子 gradient flow 得到 continuity/PDE 形式；
3. 解释为何 mean-field dynamics 对分布是非线性的；
4. 区分 $1/m$ mean-field 与 $1/\sqrt m$ tangent scaling；
5. 说明 learning-rate/time rescaling 如何决定非平凡极限；
6. 区分 fixed random features、NTK 与 feature-learning regimes；
7. 说明 propagation-of-chaos/finite-width approximation 的角色；
8. 识别 mean-field global convergence theorem 的强假设；
9. 设计 kernel drift 与 feature movement 的多证据诊断；
10. 把 infinite-width theorem 谨慎连接到现代深网。

## 二、两层网络作为粒子系统

考虑宽度为 $m$ 的两层网络：

$$
f_m(x)=\frac1m\sum_{j=1}^m a_j\sigma(w_j^\top x).
$$

把一个 neuron 的参数写成 $\vartheta_j=(a_j,w_j)$，基本特征写成

$$
\phi(x;\vartheta)=a\sigma(w^\top x).
$$

定义参数经验测度

$$
\boxed{
\rho_m=\frac1m\sum_{j=1}^m\delta_{\vartheta_j}.
}
$$

那么网络恰好是

$$
\boxed{
f_{\rho_m}(x)=\int\phi(x;\vartheta)\,\rho_m(d\vartheta).
}
$$

这一步把“越来越长的参数向量”换成“概率测度空间中的一个点”。宽度极限研究 $\rho_m\Rightarrow\rho$，而非让坐标数继续显式增长。

## 三、风险是测度的函数

以平方损失为例：

$$
\mathcal R(\rho)
=\frac12\mathbb E_{(x,y)}
\left(f_\rho(x)-y\right)^2.
$$

对单个粒子位置的 first variation/势函数可写为

$$
\Psi(\vartheta;\rho)
=\mathbb E_{(x,y)}
\left[(f_\rho(x)-y)\phi(x;\vartheta)\right],
$$

忽略与 $\vartheta$ 无关项。它依赖全体分布 $\rho$，因为每个 neuron 感受到由当前总预测产生的 residual。

## 四、从粒子 ODE 到 Continuity PDE

在适当的学习率/时间尺度下，particle gradient flow 具有形式

$$
\dot\vartheta_j(t)
=-\nabla_\vartheta\Psi(\vartheta_j(t);\rho_{m,t}).
$$

令速度场

$$
v_t(\vartheta)=-\nabla_\vartheta\Psi(\vartheta;\rho_t).
$$

粒子数趋于无穷时，质量由速度场搬运，满足 continuity equation：

$$
\boxed{
\partial_t\rho_t+\nabla_\vartheta\cdot(\rho_tv_t)=0,
}
$$

等价地

$$
\boxed{
\partial_t\rho_t
=\nabla_\vartheta\cdot
\bigl(\rho_t\nabla_\vartheta\Psi(\vartheta;\rho_t)\bigr).
}
$$

若 SGD 噪声在极限中保留，还可能出现 diffusion 项，形成 nonlinear Fokker–Planck equation。符号与温度取决于具体 scaling。

## 五、为什么这是 Feature Learning

在 random-feature/kernel regime，feature $\phi(x;\vartheta_j(0))$ 基本固定，只学习组合系数或初始化 tangent features。mean-field dynamics 则搬运 $w_j$ 的分布，因而

$$
x\mapsto\sigma(w_j(t)^\top x)

$$

本身改变。对应的 time-dependent tangent kernel、feature covariance、activation partition 都可以产生 order-one 变化。这是“learned representation”的数学入口。

但 feature movement 不保证 movement 有用：它可能对训练集过拟合、学习 spurious correlation 或在 shift 下失效。泛化仍需数据与风险桥。

## 六、Mean-Field 与 NTK Scaling 的区别

最常见的两种表示为

$$
f_m^{\rm MF}(x)=\frac1m\sum_{j=1}^m\phi(x;\vartheta_j),
\qquad
f_m^{\rm NTK}(x)=\frac1{\sqrt m}\sum_{j=1}^m\phi(x;\vartheta_j).
$$

不能只看前因子下结论，还要同时指定初始化方差、learning rate 和 time scaling。粗略对比为：

| 方面 | NTK/lazy | Mean-field/feature |
|---|---|---|
| 极限状态 | 初始化 tangent kernel | 参数分布 $\rho_t$ |
| 训练方程 | 近似线性、固定核 | 非线性 measure dynamics |
| 个体移动 | 通常相对小 | 分布可 order-one 演化 |
| feature | 近似固定 | 随 $\rho_t$ 改变 |
| 数学工具 | kernel spectral theory | transport/Wasserstein/PDE |

它们是更大 regime 空间中的两个端点，而不是所有有限网络必须二选一的标签。

## 七、极限顺序不可省略

以下极限一般不可随意交换：

$$
m\to\infty,\qquad t\to\infty,
\qquad \eta\to0,\qquad n\to\infty.
$$

例如，先让 $m\to\infty$ 可能得到固定时间上的 PDE 近似；再让 $t\to\infty$ 需要额外 compactness/convergence。若训练时间随 $m$ 增长，有限宽误差可能积累。若先把步长固定再扩大宽度，离散 dynamics 也未必收敛到同一个 flow。

每个“infinite-width” claim 都应写成带顺序的句子，而不是一个无条件标签。

## 八、Finite Width Bridge：Propagation of Chaos

若初始化粒子 i.i.d.，交互通过经验分布平均化，常可证明对有限时间窗：

$$
\rho_{m,t}\approx\rho_t,

$$

并且任意固定有限组粒子渐近独立、共享同一 marginal law。这类 propagation-of-chaos 结论把 PDE 接回真实有限 $m$ 网络。

所需条件可能包括 Lipschitz/bounded gradients、moment control、光滑激活、有限时间；ReLU 非光滑、深层共享依赖、adaptive optimization 与长时间训练都需要额外工作。

## 九、Landscape 与 Global Convergence 要怎样读

一些两层 mean-field 结果在充分表达、初始化有足够支持、势函数 regularity、特定噪声或同质性条件下证明 distributional dynamics 接近 global optimum。这不是“所有宽深网没有坏局部极小值”。必须列出：

1. population 还是 empirical risk；
2. 两层还是多层；
3. 哪种 activation 与参数约束；
4. 初始化 support；
5. 是否加入 entropy/noise；
6. 收敛的是 risk、measure 还是参数；
7. 是否 uniform in time/width。

## 十、怎样测量 Feature Learning

单一指标容易受 parameterization 欺骗，建议建立联合面板：

- relative kernel drift $\|K_t-K_0\|/\|K_0\|$；
- activation/feature covariance eigenspace drift；
- centered kernel alignment 或 CKA（注明其 invariance）；
- linear probe 与 frozen-feature transfer；
- tangent alignment：真实更新与初始化 tangent subspace 的距离；
- controlled task：随机 features 不能完成、可学习 features 才能迁移的任务。

parameter displacement 只作辅助，因为同一函数可通过重缩放获得不同 raw movement。

## 十一、图：粒子云怎样变成表示动力学

先看图回答：为什么 mean-field PDE 是非线性的，即使 predictor 对 $\rho$ 是线性的？

![[00-知识库管理/_assets/figures/learning-theory/fig-mean-field-feature-learning-v2.svg|900]]

> [!figure] 图 20.10-07　从 neuron 粒子到 measure dynamics，再到训练 regime 诊断
> 左栏把有限宽网络写成经验测度；中栏展示 residual-dependent velocity 搬运参数分布；右栏对比 fixed-kernel、feature-learning 与有限宽混合区。来源：依据 Mei–Montanari–Nguyen、Chizat–Oyallon–Bach 与 Yang–Hu 独立绘制；由 [[plot_deep_generalization_part2_v2.py]] 确定性生成。

**怎样读图**：先固定网络归一化和时间尺度，再观察 $\rho_t$/features 是否移动，最后才为有限网络贴 regime 标签。

**图没有证明什么**：图没有证明所有深层 Transformer 都服从两层 mean-field PDE，也没有证明 feature movement 必然带来更好泛化。

## 十二、AI 接口

- pretraining/transfer：是 fixed random feature 与 learned representation 的关键分水岭；
- representation collapse：可研究 measure 是否集中到退化支持，但需接下游充分性；
- mixture-of-experts：粒子/分布视角可描述 expert population，但 routing 会增加耦合；
- μP/maximal update：展示 parameterization 可在无限宽极限保留 feature learning；
- finite-width networks：常处于 kernel 与 rich regimes 之间，training phase 也可发生转换；
- data augmentation：改变 population risk 势函数，进而改变粒子 transport，而不只是加噪。

## 十三、常见错误

1. 把 mean-field 当成“平均激活”的模糊比喻；
2. 只写 $1/m$，不写学习率/时间尺度；
3. 把参数移动等同于有用 feature learning；
4. 把两层 PDE theorem 外推到任意深网；
5. 忽略 finite-time 与 long-time 的差别；
6. 把 global risk convergence 当 test generalization；
7. 认为 NTK 与 mean-field 覆盖了全部有限宽动力学；
8. 忘记数据 law 决定势函数。

## 十四、最小记忆与掌握标准

> [!summary]
> - $\rho_m=m^{-1}\sum_j\delta_{\vartheta_j}$ 把宽网变成经验测度；
> - $f_\rho=\int\phi\,d\rho$，但速度依赖 residual 和 $\rho$，故 dynamics 非线性；
> - $\partial_t\rho=\nabla\cdot(\rho\nabla\Psi)$ 是 transport/gradient-flow 骨架；
> - scaling、学习率、时间与极限顺序共同定义 regime；
> - feature learning 要用 kernel/representation/transfer 多证据验证。

能把粒子和测度互换（A）、手算离散经验测度（B）、由弱形式重建 continuity equation（C）、审计过度外推（D），并设计 feature-learning regime 实验（E）。

## 十五、练习与独立详解

- [[习题 - Mean-Field、Feature Learning 与训练 Regime]]
- [[解答 - Mean-Field、Feature Learning 与训练 Regime]]

## 参考来源

- [[S-2018-Mei-Mean-Field]]
- [[S-2019-Chizat-Lazy-Training]]
- [[S-2021-Yang-Hu-Feature-Learning]]

