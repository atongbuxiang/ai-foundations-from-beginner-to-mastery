---
type: derivation
status: verified
area: [generative-models, diffusion, probability-flow, ode]
node_id: GEN-51
prerequisites: ["[[Reverse-time SDE、时间反演与 Score Drift]]", "[[Fokker-Planck 方程与概率流 ODE]]", "[[连续性方程与守恒律]]"]
related: ["[[流映射、Liouville 公式与连续正规化流]]", "[[连续性方程、概率路径与 Flow Matching]]", "[[DDIM、非 Markov 前向族与确定性采样]]"]
sources: ["[[S-2022-Su-9228-概率流ODE]]", "[[S-2022-Su-9280-硬刚扩散ODE]]", "[[S-2021-Song-Score-SDE]]"]
exercises: ["[[习题 - Probability-flow ODE 与共享边缘分布]]"]
solutions: ["[[解答 - Probability-flow ODE 与共享边缘分布]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-probability-flow-marginal-path-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Probability-flow ODE 与共享边缘分布

> [!abstract] 一句话结论
> 对各向同性 forward SDE $dX_t=fdt+g(t)dW_t$，其密度满足 Fokker–Planck 方程。把扩散通量写成 score 驱动的确定性通量，可得 probability-flow ODE：$\dot X_t=f-\tfrac12g^2\nabla\log p_t$。在正则性和 PDE 唯一性条件下，它与 SDE 共享每个时刻的 marginal density；但 ODE 轨迹由初值确定、二次变差为零，绝不因此拥有同一 path law。

## 一、为什么还要一个确定性 ODE

GEN-50 已经给出可生成的 reverse SDE。构造 ODE 仍有价值，因为它允许：

- 使用成熟的 adaptive ODE solver；
- 在 flow 可逆且散度可计算时跟踪 likelihood；
- 研究 deterministic coupling 与 latent interpolation；
- 把 diffusion density path 接到 Continuous Normalizing Flow 和 Flow Matching。

但“deterministic”只表示给定初值后没有额外 Brownian noise，不表示无需神经网络、无需 numerical integration，也不表示轨迹更接近真实数据语义路径。

## 二、从 Fokker–Planck 方程开始

取 forward Itô SDE

$$
dX_t=f(X_t,t)dt+g(t)dW_t.
$$

其密度 $p_t$ 在适当条件下满足

$$
\boxed{
\partial_tp_t(x)
=-\nabla\cdot\bigl(f(x,t)p_t(x)\bigr)
+\frac12g(t)^2\Delta p_t(x).
}
$$

第二项看似是二阶扩散项。只要 $p_t(x)>0$ 且可微，就有

$$
\nabla p_t=p_t\nabla\log p_t,
\qquad
\Delta p_t=\nabla\cdot\bigl(p_t\nabla\log p_t\bigr).
$$

代回：

$$
\begin{aligned}
\partial_tp_t
&=-\nabla\cdot(fp_t)
+\frac12g^2\nabla\cdot(p_t\nabla\log p_t)\\
&=-\nabla\cdot\left[
p_t\left(f-\frac12g^2\nabla\log p_t\right)
\right].
\end{aligned}
$$

右侧已经是确定性连续性方程 $\partial_tp=-\nabla\cdot(pv)$。

## 三、Probability-flow ODE

因此可选择 canonical velocity

$$
\boxed{
v_{PF}(x,t)=f(x,t)-\frac12g(t)^2s_t(x),
\qquad s_t=\nabla_x\log p_t.
}
$$

并定义 ODE

$$
\boxed{\frac{dX_t}{dt}=v_{PF}(X_t,t).}
$$

若 ODE 诱导密度的连续性方程有唯一解，且起始密度与 SDE 相同，则对每个 $t$，ODE density 与 SDE density 相同。这是一个 PDE/分布层结论，不是逐路径恒等式。

### 3.1 为什么系数是 $1/2$，反向 SDE 却是 $1$

forward Fokker–Planck 的扩散通量是 $+(1/2)g^2\Delta p$。PF ODE 没有 Brownian diffusion，必须用 score velocity 独自承担这半个通量，所以系数是 $1/2$。

reverse SDE 仍有 $g\,d\bar W$。当时间方向反转时，这一随机项对密度演化贡献另一半；要得到正确 reverse density evolution，drift correction 是完整的 $g^2s_t$。只比较 drift 方括号而不比较 diffusion term，会误以为二者矛盾。

## 四、一个完全可算的 Brownian 例子

令

$$dX_t=dW_t,\qquad X_0\sim N(0,I).$$

则

$$p_t=N(0,(1+t)I),\qquad s_t(x)=-\frac{x}{1+t}.$$

PF velocity 为

$$v_{PF}(x,t)=-\frac12s_t(x)=\frac{x}{2(1+t)}.$$

ODE 是

$$\frac{dX_t}{dt}=\frac{X_t}{2(1+t)}.$$

分离变量：

$$\frac{dX_t}{X_t}=\frac{dt}{2(1+t)}$$

得到

$$
X_t=X_0\sqrt{1+t}.
$$

若 $X_0\sim N(0,I)$，则 $X_t\sim N(0,(1+t)I)$，正好与 Brownian SDE 同边缘。

但两者的 conditional law 完全不同：

$$
X_t^{SDE}\mid X_0=x_0\sim N(x_0,tI),
$$

$$
X_t^{ODE}\mid X_0=x_0=\sqrt{1+t}\,x_0
\quad\text{几乎处处确定。}
$$

这一个例子已经足以否定“same marginals 推出 same transition law”。

## 五、路径律不同的最短证明：二次变差

对非退化 SDE，典型路径有

$$[X]_t=\int_0^t g(s)^2ds>0.$$

对局部 Lipschitz ODE 的有限变差路径，

$$[X]_t=0.$$

路径二次变差是 path-law 可辨认量。只要 $g$ 非零，SDE 与 PF ODE 就不可能拥有相同路径律，即使它们每个时刻画出的直方图完全一致。

## 六、速度场不是唯一的

连续性方程只约束通量散度。若 $v$ 运输 $p_t$，并且 $w$ 满足

$$\nabla\cdot(p_tw)=0,$$

则

$$\nabla\cdot[p_t(v+w)]=\nabla\cdot(p_tv)$$

也运输同一密度路径。PF velocity 是由给定 SDE 自然选出的 canonical representative，不是“所有同边缘 ODE 中唯一的速度”。

在一维、全实线并要求边界通量为零时，自由度可能被大幅压缩；在高维，旋转型 divergence-free current 很常见。Flow Matching 的 path/coupling choice 正是在更丰富的候选中选择可学习速度。

## 七、一般扩散矩阵的公式

对

$$dX_t=a(X_t,t)dt+B(X_t,t)dW_t,\qquad D=BB^\top,$$

Fokker–Planck 是

$$
\partial_tp=-\nabla\cdot(ap)
+\frac12\sum_{i,j}\partial_{ij}(D_{ij}p).
$$

将其写成 $-\nabla\cdot(pv)$，可取

$$
v_i=a_i-\frac1{2p}\sum_j\partial_{x_j}(D_{ij}p).
$$

展开为

$$
v=a-\frac12(\nabla\cdot D)-\frac12D\nabla\log p.
$$

只有 $D=g(t)^2I$ 时才退化为 $a-(1/2)g^2s$。这与 GEN-50 的 state-dependent reverse drift 边界完全对应。

## 八、用 learned score 生成

用 $s_\theta$ 代替真实 score：

$$
\dot X_t=f(X_t,t)-\frac12g(t)^2s_\theta(X_t,t).
$$

从 $X_1\sim p_1^{prior}$ 沿 $t:1\downarrow0$ 求解。误差至少有三项：

$$
\text{terminal error}
+\text{score/model error}
+\text{ODE discretization error}.
$$

减小 solver tolerance 只能压低第三项，不能修复 prior mismatch 或 learned score 偏差。反过来，训练 loss 更低也不保证粗糙 Euler 网格准确。

## 九、Likelihood 与 CNF 接口

对 ODE $\dot X_t=v_\theta(X_t,t)$，沿轨迹有 instantaneous change of variables：

$$
\frac{d}{dt}\log p_t(X_t)
=-\nabla\cdot v_\theta(X_t,t).
$$

因此

$$
\log p_0(X_0)
=\log p_1(X_1)
+\int_0^1\nabla\cdot v_\theta(X_t,t)dt,
$$

其中正负号依赖积分方向；最安全做法是从微分式逐次积分。高维 divergence 可用 Hutchinson estimator，但会再引入 trace-estimation variance 与 ODE solver error。

注意：用 approximate score 构造的 ODE 仍是一个合法 CNF，只要流适定；但它的 density path 不再保证等于原 forward SDE 的 $p_t$。

## 十、与 DDIM 的关系边界

DDIM 展示了共享 fixed-time marginals 的非 Markov joint family，并给出确定性离散 sampler；PF ODE 展示连续时间下共享 $p_t$ 的确定性 flow。二者有紧密连续极限联系，但不能简写成“DDIM 就是任意 ODE solver”：

- DDIM update 依赖特定 diffusion parameterization 和时间网格；
- PF ODE 是由 Fokker–Planck 配平定义的连续速度；
- finite-step DDIM 与 numerical PF ODE 的局部截断误差一般不同。

## 十一、科学空间研读框

[[S-2022-Su-9228-概率流ODE]] 从 Fokker–Planck 推出同边缘 ODE，并连接 DDIM；[[S-2022-Su-9280-硬刚扩散ODE]] 则从 Jacobian/density 的小步 Taylor 展开直观进入同一连续性方程。

本节采用前者的主链、后者的问题意识，并补上：

- 一般 diffusion matrix 的 $\nabla\cdot D$ 项；
- PDE uniqueness 与 positivity/regularity 条件；
- Brownian/PF ODE 的精确 Gaussian 反例；
- quadratic variation 证明 path law 不同；
- score error 与 numerical error 分账。

一级方法来源为 [[S-2021-Song-Score-SDE]]，数学证明底座见 [[Fokker-Planck 方程与概率流 ODE]]。

## 十二、图：同一组截面，不同的路径电影

先看图回答：为什么每个时间截面的点云都一样，仍不足以说 SDE 与 ODE 是同一个随机过程？

![[00-知识库管理/_assets/figures/generative-models/fig-probability-flow-marginal-path-v1.svg|900]]

> [!figure] 图 50.7-03　SDE 与 probability-flow ODE：共享边缘，不共享 path law
> 中央列画相同时间截面，上下分别画 Brownian 随机路径和确定性 flow path；右侧用 quadratic variation 与 conditional law 做审计。来源：据 Fokker–Planck 配平和 Gaussian 特例独立绘制。

**怎样读图**：竖向比较同一个 $t$ 的分布截面，再横向沿单个样本看轨迹连接方式。截面相同只验证 E1，不验证路径层。

**图没有证明什么**：图不证明 velocity 唯一，不证明 learned PF ODE 与真实 SDE 仍同边缘，也不证明 ODE 在固定 NFE 下优于 SDE sampler。

## 十三、本节回顾与训练

- PF ODE 来自把 Fokker–Planck 写成连续性方程；
- $1/2$ 系数恰好替代 forward diffusion flux；
- same marginals 不包含 transition、coupling 或 path law；
- canonical PF velocity 不是所有同密度速度中的唯一解；
- likelihood、score approximation 和 numerical integration 都有额外条件；
- [[习题 - Probability-flow ODE 与共享边缘分布]]
- [[解答 - Probability-flow ODE 与共享边缘分布]]
