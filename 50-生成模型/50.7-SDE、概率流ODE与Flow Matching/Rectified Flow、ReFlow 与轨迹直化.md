---
type: derivation
status: verified
area: [generative-models, rectified-flow, reflow, ode]
node_id: GEN-55
prerequisites: ["[[Conditional Flow Matching、Coupling 与最优传输路径]]", "[[Euler、Runge-Kutta 与离散化误差]]", "[[流映射、Liouville 公式与连续正规化流]]"]
related: ["[[连续性方程、概率路径与 Flow Matching]]", "[[Diffusion、Flow、速度参数化与统一证据地图]]", "[[Euler、Runge-Kutta 与离散化误差]]"]
sources: ["[[S-2023-Su-9497-构建ODE一般步骤下]]", "[[S-2022-Liu-Rectified-Flow]]", "[[S-2024-Tong-Conditional-Flow-Matching]]"]
exercises: ["[[习题 - Rectified Flow、ReFlow 与轨迹直化]]"]
solutions: ["[[解答 - Rectified Flow、ReFlow 与轨迹直化]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-rectified-reflow-straightening-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Rectified Flow、ReFlow 与轨迹直化

> [!abstract] 一句话结论
> Rectified Flow 用端点 coupling 的直线插值 $X_t=(1-t)X_0+tX_1$ 和常量 target $X_1-X_0$ 训练 velocity field；population field 是同一位置处这些位移的条件平均，因此 learned ODE trajectory 仍可能弯曲。Rectification 把原 coupling 转成保持端点边缘的确定性 coupling，并在理论条件下不增加 convex transport costs；ReFlow 用当前模型 coupling 重新配对、再训练，旨在减少交叉和曲率，但“一步 Euler 精确”始终是额外条件或经验结果。

## 一、统一方向：本卷为什么从数据走向噪声

Rectified Flow 可连接任意两分布。为与前六个节点一致，本卷固定

$$X_0\sim p_{data},\qquad X_1\sim p_{ref},$$

训练 path 从数据 $t=0$ 走向 reference $t=1$，生成从 $1$ 反向积分到 $0$。许多代码/论文以 noise 为 $t=0$、data 为 $t=1$；那只是整体交换端点和 velocity 符号，不是不同算法。

## 二、Rectified Flow 的最小目标

先从某个 coupling $\pi(X_0,X_1)$ 采端点对，定义直线 interpolation

$$
\boxed{X_t=(1-t)X_0+tX_1.}
$$

逐对路径导数为常量

$$
\boxed{U_t=\frac{dX_t}{dt}=X_1-X_0.}
$$

训练非线性最小二乘

$$
\boxed{
L_{RF}(\theta)
=\mathbb E_{t,(X_0,X_1)\sim\pi}
\|v_\theta(X_t,t)-(X_1-X_0)\|^2.
}
$$

它不需要在训练内解 ODE，也不需要计算 likelihood/Jacobian determinant。训练完成后，生成仍需解

$$\frac{dZ_t}{dt}=v_\theta(Z_t,t),\qquad t:1\downarrow0.$$

## 三、直线 teacher path 为什么不等于直线 model path

population 最优场是

$$
v^*(x,t)=\mathbb E[X_1-X_0\mid X_t=x,t].
$$

对每一端点对，$X_1-X_0$ 沿 teacher line 恒定；但若多条 line 在相近位置交叉，$v^*$ 是多方向平均。模型 ODE 从某个初值出发时，每一时刻都重新读取当前位置的平均场，未必继续沿某一条原 teacher segment。

沿 exact ODE trajectory 的加速度是

$$
\boxed{
\frac{d^2Z_t}{dt^2}
=\partial_tv(Z_t,t)+J_xv(Z_t,t)v(Z_t,t).
}
$$

只有这个 material derivative 接近零，trajectory 才近似直线。训练 target 对每条 conditional line 的导数为常数，并不直接约束上式在 learned trajectory 上为零。

## 四、Rectification 在总体层做了什么

设 $v^*$ 是当前 straight-path regression 的理想 population field，解其 ODE 得到 flow map。把原端点中的一端经 flow 映到另一端，会诱导一个新的 deterministic coupling，称为 rectified coupling。

在 Rectified Flow 原论文的条件下，这个 procedure：

1. 保持两个 endpoint marginals；
2. 把一般随机 coupling 转成由 ODE flow 诱导的 deterministic coupling；
3. 对一类 convex transport costs 不增加平均 cost；
4. 可递归应用，得到越来越适合粗时间离散的 flow。

“不增加 convex cost”不等于“一次后达到 population OT optimum”；“deterministic coupling”也不等于“每条轨迹严格直线”。

## 五、ReFlow 的训练循环

以第 $k$ 轮模型 $v^{(k)}$ 为例：

1. 采 $Z_1\sim p_{ref}$；
2. 用 $v^{(k)}$ 从 $t=1$ 积到 $0$，得到 $Z_0$；
3. 保存模型诱导的 paired endpoints $(Z_0,Z_1)$；
4. 对新直线 $\widetilde Z_t=(1-t)Z_0+tZ_1$ 回归 target $Z_1-Z_0$；
5. 得到 $v^{(k+1)}$，再评估曲率与有限 NFE 误差。

这叫 ReFlow/recursive rectification。与初始 independent coupling 相比，模型 coupling 往往减少路径交叉，因为每个 reference sample 已由同一 deterministic flow 对应到一个 generated data sample。

但需要分账：

- $Z_0$ 是当前模型样本，不是真实训练样本；
- teacher ODE 的 solver error 会写入 pairing；
- 反复 self-training 可能保留或放大 model bias；
- 生成质量、曲率和 convex cost 应分别测量。

## 六、为什么直化有利于少步采样

对一步 Euler，从 $t=1$ 反向到 $0$：

$$
\widehat Z_0=Z_1-v_\theta(Z_1,1).
$$

exact 解为

$$
Z_0=Z_1-\int_0^1v(Z_t,t)dt.
$$

两者之差来自 velocity 沿真实轨迹的变化：

$$
Z_0-\widehat Z_0
=\int_0^1[v(Z_1,1)-v(Z_t,t)]dt.
$$

若 material derivative 小，$v(Z_t,t)$ 近常量，粗 Euler 更准。ReFlow 的目标不是神奇地删除积分，而是改变 coupling/训练分布，使 velocity 更接近这种状态。

## 七、“一 Euler 步总是精确”的反例

考虑一维 ODE

$$\frac{dZ_t}{dt}=tZ_t.$$

exact flow 是

$$Z_1=e^{1/2}Z_0,$$

所以从 $Z_1$ 反推

$$Z_0=e^{-1/2}Z_1.$$

一步反向 Euler 却给

$$\widehat Z_0=Z_1-v(Z_1,1)=Z_1-Z_1=0.$$

除 $Z_1=0$ 外完全错误。这个例子不是说 Rectified Flow 会学到 $tZ$，而是说明“ODE 是确定性的”或“训练用了直线 segment”都不足以推出 one-step exactness；必须检查 learned field 沿实际 trajectory 是否近常量。

## 八、三种“直”的指标不要混用

| 指标 | 定义 | 测量对象 |
|---|---|---|
| conditional straightness | teacher $\partial_t^2\phi_t=0$ | 构造的端点线段 |
| trajectory curvature | $\|\partial_tv+J_vv\|$ 或几何曲率 | learned ODE path |
| finite-step consistency | 粗 solver 与精 solver/teacher endpoint 的误差 | 数值程序 |

另可测 path length ratio

$$
R_{len}=\frac{\int_0^1\|\dot Z_t\|dt}{\|Z_1-Z_0\|}\ge1.
$$

$R_{len}\approx1$ 表示几何接近直线，但若 velocity 随时间剧烈改变，Euler error 仍可能不小；反之某些曲线路径可被高阶 solver 低 NFE 准确积分。

## 九、与 OT 的精确关系

Rectification 的 convex-cost non-increase 给出 transport 改善方向，但并不自动解出 quadratic population OT。需要区分：

- 初始 coupling 是否 independent、minibatch OT 或其他 plan；
- rectified deterministic coupling 的 cost；
- 真正 population OT minimum；
- learned finite network 与 exact population field 的差；
- solver 产生的 empirical coupling。

若只报告平均 $\|X_1-X_0\|^2$ 降低，最多支持 endpoint cost 改善；不能据此断言整个 density path 是 Wasserstein geodesic。

## 十、最小实验协议

一个可信的 ReFlow 实验至少应报告：

1. 初始 coupling 与端点方向；
2. 每轮 ReFlow 的 pairing solver、NFE 和 tolerance；
3. teacher endpoints 是真实数据还是模型生成；
4. population loss proxy 与 held-out CFM loss；
5. path length ratio、material acceleration、1/2/4/8-step endpoint error；
6. 最终质量/覆盖指标和 equal-NFE wall time；
7. 多 seed 误差条。

只展示几条看起来更直的二维轨迹属于直觉证据，不足以证明高维生成质量或 transport theorem 的有限实现版本。

## 十一、科学空间研读框

[[S-2023-Su-9497-构建ODE一般步骤下]] 用“端点联合分布—插值—路径导数回归”非常直接地进入 Rectified Flow，并明确指出群体轨迹可能弯曲。课程保留这一关键提醒，再用：

- conditional expectation 写出 population field；
- material derivative 定义 model trajectory 的弯曲；
- 一步 Euler 反例拆除错误推论；
- [[S-2022-Liu-Rectified-Flow]] 约束 convex-cost 与 rectification theorem；
- [[S-2024-Tong-Conditional-Flow-Matching]] 区分 OT-CFM/minibatch coupling。

## 十二、图：ReFlow 直化的是哪一层

先看图回答：第一次训练的直线 target、模型生成的弯曲轨迹、第二轮重新配对后的新直线，三者为何不是同一条线？

![[00-知识库管理/_assets/figures/generative-models/fig-rectified-reflow-straightening-v1.svg|900]]

> [!figure] 图 50.7-07　Rectified Flow/ReFlow 的 coupling 更新、轨迹曲率与有限步误差
> 左栏画初始端点直线与交叉，中栏画 learned flow 诱导的新 pairing，右栏画 ReFlow 重训后曲率/NFE 审计。来源：据 Rectified Flow procedure 与 material derivative 独立绘制。

**怎样读图**：沿轮次而非单条线阅读：原 coupling 产生回归场，回归场产生新 deterministic coupling，新 coupling 再定义直线监督。直化是递归改变 pairing 的结果。

**图没有证明什么**：图不证明一轮 ReFlow 达到 OT，不证明 finite network 保持 convex-cost theorem，也不证明一 Euler 步在所有样本上精确。

## 十三、本节回顾与训练

- RF 的 conditional target 直线，不保证 learned ODE trajectory 直线；
- trajectory curvature 由 material derivative 决定；
- rectification 保持端点边缘，并在条件下不增加 convex transport cost；
- ReFlow 用当前模型 coupling 重新配对，包含 teacher/solver/model bias；
- 少步生成必须用 finite-NFE endpoint error 实测；
- [[习题 - Rectified Flow、ReFlow 与轨迹直化]]
- [[解答 - Rectified Flow、ReFlow 与轨迹直化]]
