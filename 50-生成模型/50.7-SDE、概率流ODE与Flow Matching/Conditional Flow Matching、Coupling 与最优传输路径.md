---
type: derivation
status: verified
area: [generative-models, conditional-flow-matching, coupling, optimal-transport]
node_id: GEN-54
prerequisites: ["[[连续性方程、概率路径与 Flow Matching]]", "[[IPM、Wasserstein-1 与 Kantorovich 对偶]]", "[[联合分布、边缘分布与独立性]]"]
related: ["[[Rectified Flow、ReFlow 与轨迹直化]]", "[[IPM、Wasserstein-1 与 Kantorovich 对偶]]", "[[Diffusion、Flow、速度参数化与统一证据地图]]"]
sources: ["[[S-2022-Su-9379-构建ODE一般步骤中]]", "[[S-2023-Su-9497-构建ODE一般步骤下]]", "[[S-2023-Lipman-Flow-Matching]]", "[[S-2024-Tong-Conditional-Flow-Matching]]"]
exercises: ["[[习题 - Conditional Flow Matching、Coupling 与最优传输路径]]"]
solutions: ["[[解答 - Conditional Flow Matching、Coupling 与最优传输路径]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-cfm-coupling-ot-crossing-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Conditional Flow Matching、Coupling 与最优传输路径

> [!abstract] 一句话结论
> Conditional Flow Matching 的 endpoint coupling 不是无关紧要的采样细节：它决定哪些 source/target 被配对，进而决定 conditional displacement、路径交叉和不可约回归方差。Independent coupling 最容易采样；population OT coupling 在平方成本与适当正则条件下给 displacement interpolation；minibatch OT 只是批内近似，不能直接称为真实 OT plan。

## 一、Coupling 到底是什么

给定两个端点分布

$$X_0\sim p_0=p_{data},\qquad X_1\sim p_1=p_{ref},$$

coupling $\pi(x_0,x_1)$ 是一个联合分布，其两个边缘分别是 $p_0,p_1$：

$$
\int\pi(x_0,x_1)dx_1=p_0(x_0),
\qquad
\int\pi(x_0,x_1)dx_0=p_1(x_1).
$$

边缘只说“起点集合”和“终点集合”，coupling 还说“谁和谁配对”。最简单的是独立 coupling

$$\pi_{ind}(x_0,x_1)=p_0(x_0)p_1(x_1).$$

它不需要求解配对问题，但可能产生很长、互相交叉的路径。

## 二、从 coupling 到 conditional path

给定 $(X_0,X_1)\sim\pi$，选择可微插值

$$X_t=\phi_t(X_0,X_1,Z),$$

其中 $Z$ 可是附加噪声。要求端点满足

$$\phi_0=X_0,\qquad\phi_1=X_1$$

（可为 almost sure 或 distributional endpoint）。conditional velocity 是

$$U_t=\partial_t\phi_t(X_0,X_1,Z).$$

CFM 回归

$$
L_{CFM}(\theta)=
\mathbb E\|v_\theta(X_t,t)-U_t\|^2.
$$

population target 为

$$v_t(x)=\mathbb E[U_t\mid X_t=x,t].$$

coupling 改变 $(X_t,U_t)$ 的联合分布，所以即使端点边缘不变，target field 和训练方差都可能改变。

## 三、直线插值并不消除 coupling 的影响

最常用 conditional path 是

$$
X_t=(1-t)X_0+tX_1,
\qquad U_t=X_1-X_0.
$$

$U_t$ 对每一对端点恒定，看起来非常简单。但网络看不到端点对，只看到 $(X_t,t)$。当多条线段在同一位置相交，条件平均会把不同方向混合。

### 3.1 两点 coupling 反例

令 $p_0=p_1$ 都是在 $\{-1,+1\}$ 上均匀的分布。存在两种合法 coupling：

**恒等 coupling**：$X_1=X_0$。则所有路径静止，$U_t=0$，不可约方差为零。

**交换 coupling**：$X_1=-X_0$。则两条路径

$$-1\to+1,\qquad+1\to-1$$

在 $t=1/2$ 都经过 $X_t=0$，但速度分别为 $+2,-2$。因此

$$
v_{1/2}(0)=\mathbb E[U\mid X_{1/2}=0]=0,
$$

$$
\operatorname{Var}(U\mid X_{1/2}=0)=4.
$$

两个 coupling 的 endpoint marginals 完全相同，训练难度却天差地别。这也说明边缘 equality 无法识别 pairing。

## 四、Coupling 怎样进入 SGD 方差

CFM 与 marginal FM 的常数差是

$$
C_\pi=\mathbb E\|U_t-\mathbb E[U_t\mid X_t,t]\|^2.
$$

它依赖 coupling $\pi$ 和 conditional path $\phi_t$。$C_\pi$ 不改变 population minimizer，但会影响：

- 单样本 target variance；
- minibatch gradient variance；
- network 需要拟合的局部多模态方向；
- finite capacity 下的平滑/平均偏差；
- learned field 的 Jacobian 与 solver 难度。

因此“目标相差常数”并不意味着所有 coupling 的训练过程一样。

## 五、平方成本的最优传输 coupling

静态 quadratic OT 寻找

$$
\pi^*\in\arg\min_{\pi\in\Pi(p_0,p_1)}
\mathbb E_\pi\|X_1-X_0\|^2.
$$

它直接最小化平均平方 displacement。若分布满足适当绝对连续性等条件，Brenier map 给出 deterministic optimal coupling，直线 displacement interpolation

$$X_t=(1-t)X_0+tT(X_0)$$

对应 $W_2$ geodesic，并最小化 Benamou–Brenier 动能

$$
\int_0^1\int\|v_t(x)\|^2p_t(x)dxdt.
$$

这些是带假设的最优传输结论，不是任何“把批内距离最小化”的配对都自动满足。

## 六、OT path 可能带来什么，又不保证什么

合理的 OT-style coupling 常能：

- 减少平均 endpoint displacement；
- 减少明显交叉；
- 降低某些 conditional velocity variance；
- 产生较低 kinetic energy 的 density path。

但它不自动保证：

- 在高维语义度量下配对合理；
- neural velocity 更容易逼近；
- Jacobian 更小或 ODE 不刚性；
- finite NFE 误差必然更低；
- likelihood、FID 和 wall time 同时改善。

Euclidean pixel cost 可能偏离感知/语义距离；换 cost 就换了 OT 问题。

## 七、Minibatch OT 不是 population OT

实践中从两个 batch 各采 $B$ 个点，构造 cost matrix

$$C_{ij}=\|x_0^{(i)}-x_1^{(j)}\|^2,$$

再求 batch 内 assignment 或 entropic transport plan。这给出 minibatch coupling。它有以下边界：

1. 配对依赖同批其他样本；
2. 小 batch 看不到全局 support；
3. batch assignment 的边缘是经验测度，不是 population density；
4. entropic regularization、unbalanced constraint 或 approximate solver 会改变 plan；
5. 随 batch size 改变，训练分布也改变。

因此应写“minibatch OT-CFM”，并报告 batch size、cost、regularization、solver tolerance 和 gradient policy；不写“我们使用了真实 OT path”除非确实有 population plan 或可证明的特殊结构。

## 八、Gaussian/随机 conditional path

为避免奇异中间分布，可构造

$$
X_t=\mu_t(X_0,X_1)+\sigma_tZ,
\qquad Z\sim N(0,I),
$$

$$
U_t=\partial_t\mu_t(X_0,X_1)+\dot\sigma_tZ.
$$

附加噪声改变 $p_t$、conditional variance 与 endpoint approximation。若 $\sigma_0$ 或 $\sigma_1$ 非零，端点只近似目标边缘；若让噪声精确归零，端点附近速度/score 可能变得尖锐。设计时需同时审计 smoothness 与 endpoint fidelity。

## 九、方向约定与条件生成

本卷用数据 $t=0$、reference $t=1$；训练 conditional path 是 noising direction，生成反向积分。很多 CFM 代码用 source noise $t=0$、target data $t=1$，则

$$\phi_t^{code}(x_{noise},x_{data})
=(1-t)x_{noise}+tx_{data}.$$

与本卷的关系是 $t_{course}=1-t_{code}$ 并交换端点。迁移公式时要同时换：

- endpoint 命名；
- velocity 符号；
- solver 时间网格；
- conditioning 写在哪一端。

## 十、科学空间研读框

[[S-2022-Su-9379-构建ODE一般步骤中]] 已清楚给出 $x_t=\mu_t(x_0)+\sigma_tx_1$ 的 conditional path 与速度回归，并提醒群体轨迹一般会弯曲；[[S-2023-Su-9497-构建ODE一般步骤下]] 进一步用 endpoint pair 与直线导数进入 Rectified Flow。

本节在这条中文主线上加入 coupling 的概率定义、两点交叉反例、population OT 与 minibatch OT 的边界。CFM 的一级定义见 [[S-2023-Lipman-Flow-Matching]]；generalized/OT-CFM 与 minibatch 方法见 [[S-2024-Tong-Conditional-Flow-Matching]]。

## 十一、图：相同端点边缘，配对决定交叉

先看图回答：为什么两组完全相同的端点点云，只改变连线方式，就会让 CFM target 从零方差变成方向冲突？

![[00-知识库管理/_assets/figures/generative-models/fig-cfm-coupling-ot-crossing-v1.svg|900]]

> [!figure] 图 50.7-06　Independent、交叉与 OT-style coupling 的路径/方差账
> 左侧保持端点边缘固定，中间比较三种配对，右侧以 $\operatorname{Var}(U\mid X_t)$ 和 batch/population OT 标签审计。来源：据 CFM 条件期望和两点反例独立绘制。

**怎样读图**：不要先看端点点云，而要沿配对线看哪些路径在同一 $(x,t)$ 相交；相交处多方向 target 的散布就是不可约回归方差。

**图没有证明什么**：图不证明 minibatch OT 收敛到 population OT，不证明较短线段必有更低 solver error，也不证明 Euclidean cost 等于语义质量。

## 十二、本节回顾与训练

- coupling 是 joint law，不由两个 endpoint marginals 唯一决定；
- 直线 conditional path 仍可因配对交叉产生高方差；
- OT displacement path 有严格条件，minibatch OT 只是有限经验近似；
- coupling 改变 target variance、场复杂度和有限训练表现；
- 时间方向和端点命名必须与代码成套转换；
- [[习题 - Conditional Flow Matching、Coupling 与最优传输路径]]
- [[解答 - Conditional Flow Matching、Coupling 与最优传输路径]]
