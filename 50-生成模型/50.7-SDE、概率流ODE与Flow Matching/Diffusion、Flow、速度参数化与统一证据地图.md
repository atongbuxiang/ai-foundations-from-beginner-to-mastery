---
type: synthesis
status: verified
area: [generative-models, diffusion, flow-matching, stochastic-interpolants, evidence]
node_id: GEN-56
prerequisites: ["[[Probability-flow ODE 与共享边缘分布]]", "[[Marginal Score、Conditional Score 与去噪等价]]", "[[Rectified Flow、ReFlow 与轨迹直化]]"]
related: ["[[数据、噪声、速度与 Score 参数化]]", "[[EBM、Score、GAN 与 Diffusion 的接口和证据地图]]", "[[生成模型完整课程地图与掌握标准]]"]
sources: ["[[S-2021-Song-Score-SDE]]", "[[S-2023-Lipman-Flow-Matching]]", "[[S-2022-Liu-Rectified-Flow]]", "[[S-2025-Albergo-Stochastic-Interpolants]]", "[[S-2022-Su-9305-万有引力到扩散模型]]", "[[S-2023-Su-9467-W距离与得分匹配]]"]
exercises: ["[[习题 - Diffusion、Flow、速度参数化与统一证据地图]]"]
solutions: ["[[解答 - Diffusion、Flow、速度参数化与统一证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-diffusion-flow-equivalence-evidence-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Diffusion、Flow、速度参数化与统一证据地图

> [!abstract] 一句话结论
> Diffusion SDE、probability-flow ODE、Flow Matching、Rectified Flow 与 stochastic interpolant 可以共享一条 density path、一个条件期望投影结构或可换算的 score/velocity；但它们通常不共享 path law、endpoint coupling、训练 target、Monte Carlo 方差和 finite-NFE 程序。真正的统一不是说“都一样”，而是为每一对方法标清在哪一层等价、依赖哪些假设、误差在哪一层进入。

## 一、统一前先列对象

任何连续生成方法至少包含七个对象：

1. 端点分布 $p_0,p_1$；
2. 中间 probability path $(p_t)$；
3. endpoint/trajectory coupling；
4. conditional target；
5. marginal score 或 velocity；
6. parameterized network 与 training estimator；
7. numerical sampler 与 evaluation protocol。

不同方法可能只在其中一两项上相同。若一句“本质等价”没有指出对象，几乎一定省略了关键边界。

## 二、从一条 density path 构造 ODE 与 SDE 家族

设 $p_t>0$ 满足 transport equation

$$
\partial_tp_t=-\nabla\cdot(p_tv_t),
\qquad s_t=\nabla\log p_t.
$$

给定任意非负噪声率 $\varepsilon(t)$，考虑 forward SDE

$$
\boxed{
dX_t=[v_t(X_t)+\varepsilon(t)s_t(X_t)]dt
+\sqrt{2\varepsilon(t)}dW_t.
}
$$

它的 Fokker–Planck 右侧是

$$
\begin{aligned}
&-\nabla\cdot[p_t(v_t+\varepsilon s_t)]
+\varepsilon\Delta p_t\\
&=-\nabla\cdot(p_tv_t)
-\varepsilon\nabla\cdot(p_ts_t)
+\varepsilon\Delta p_t\\
&=-\nabla\cdot(p_tv_t),
\end{aligned}
$$

因为 $p_ts_t=\nabla p_t$。所以它与 ODE $\dot X_t=v_t(X_t)$ 共享 $p_t$。令 $\varepsilon=0$ 得 ODE；取正 $\varepsilon$ 得一族 stochastic dynamics。

这正是现代 stochastic-interpolant 统一视角的一部分：噪声强度可以改变 path law，同时由 score correction 保持 density path。结论仍依赖 SDE/PDE 的适定性与相同初始 law。

## 三、Score-SDE 是上述公式的特例

对 forward diffusion

$$dX_t=fdt+g(t)dW_t,$$

PF velocity 是

$$v_t=f-\frac12g^2s_t.$$

令

$$\varepsilon(t)=\frac12g(t)^2,$$

则

$$v_t+\varepsilon s_t=f.$$

所以原 forward SDE 恰好落入上一族。反向时钟中 score correction 改变符号，得到 GEN-50 的 reverse-time SDE。这里的统一是 **同一 density equation 的代数恒等式**，不是 SDE 路径和 PF ODE 路径相同。

## 四、Flow Matching 怎样进入同一坐标系

Flow Matching 先通过 conditional interpolant $X_t=\phi_t(Z)$ 定义 $p_t$，再令

$$v_t(x)=\mathbb E[\partial_t\phi_t(Z)\mid X_t=x].$$

GEN-53 已证明它满足 transport equation。若还能得到 $s_t=\nabla\log p_t$，则可按上一节为同一 $p_t$ 构造 stochastic SDE family。

反过来，给定 diffusion path 的 Gaussian marginal，也能把 PF velocity 当作 Flow Matching target。两条路线的起点不同：

- score diffusion：先定 SDE/corruption，再由 score 构造 reverse SDE/PF ODE；
- Flow Matching：先定 conditional probability path，再回归 velocity；
- stochastic interpolant：同时组织 path、velocity、score 与可调 diffusion。

共享 density path 不等于共享 training estimator。

## 五、Gaussian path 的四种预测量

令

$$X_t=\alpha_tX_0+\sigma_t\epsilon.$$

网络常预测：

| 名称 | 理想对象 | 与其他量的关系 |
|---|---|---|
| data prediction | $\widehat X_0$ | $(X_t-\sigma_t\widehat\epsilon)/\alpha_t$ |
| noise prediction | $\widehat\epsilon$ | $-\sigma_t\widehat s_t$ |
| score prediction | $\widehat s_t$ | $(\alpha_t\widehat X_0-X_t)/\sigma_t^2$ |
| instantaneous velocity | $\widehat u_t$ | $\dot\alpha_t\widehat X_0+\dot\sigma_t\widehat\epsilon$ |

最后一行的导数系数至关重要。扩散文献还常定义

$$
v^{diff}=\alpha_t\epsilon-\sigma_tX_0.
$$

它何时恰好是 path velocity？若用角度参数 $\phi$，令

$$\alpha=\cos\phi,\qquad\sigma=\sin\phi,$$

则

$$
\frac{dX}{d\phi}
=-\sin\phi X_0+\cos\phi\epsilon
=\alpha\epsilon-\sigma X_0
=v^{diff}.
$$

但对一般时间 $t$，

$$\frac{dX}{dt}=\dot\alpha X_0+\dot\sigma\epsilon$$

不必等于 $\alpha\epsilon-\sigma X_0$。因此“$v$-parameterization”与“Flow Matching velocity”只有在声明的 time parameterization 下才一致。

## 六、参数化换算不等于训练等价

若两个输出通过可逆线性变换 $y=A(t)z$ 换算，点预测可以一一对应；但未加权 MSE 满足

$$\|A(t)(z_\theta-z)\|^2
=(z_\theta-z)^\top A(t)^\top A(t)(z_\theta-z),$$

这改变时间/方向权重。共享网络、有限容量、优化器、gradient clipping 和 time sampler 会让 training trajectory 不同。

所以必须分别回答：

- function target 能否换算？
- population loss 是否只差常数/权重？
- empirical gradient estimator 方差是否相同？
- sampling ODE/SDE 是否用同一系数？

## 七、方法—对象对照表

| 方法 | 先指定什么 | 网络 target | 生成动力学 | 主要自由度 |
|---|---|---|---|---|
| Score SDE | forward SDE/corruption | marginal score 的 conditional estimator | reverse SDE 或 PF ODE | drift、diffusion、weight、solver |
| PF ODE | diffusion density path | score 或换算 velocity | deterministic ODE | canonical velocity、ODE solver |
| FM | marginal probability path/field | marginal velocity | deterministic ODE | path 与 velocity choice |
| CFM | conditional path + latent/coupling | conditional velocity | marginal ODE | coupling、path、target variance |
| Rectified Flow | endpoint coupling + straight segments | displacement $X_1-X_0$ | learned ODE | initial coupling、ReFlow rounds |
| Stochastic interpolant | endpoint law + interpolant + latent | velocity/score objectives | ODE 或可调噪声 SDE | interpolant、noise rate、direction |

## 八、等价矩阵

| 比较 | 同 $p_t$ | 同 path law | 同 population minimizer | 同 sample loss | 同 finite sampler |
|---|---:|---:|---:|---:|---:|
| exact SDE vs exact PF ODE | 是 | 否 | 不适用 | 不适用 | 否 |
| marginal SM vs conditional SM | 目标是 | 不适用 | 是（标准条件） | 否 | 需另证 |
| FM vs CFM | 目标是 | 不适用 | 是（标准条件） | 否 | 训练后需另证 |
| independent CFM vs OT-CFM | 端点同，中间通常不同 | 否 | target field 通常不同 | 否 | 否 |
| RF teacher lines vs learned RF ODE | 理想总体下匹配中间边缘 | 通常否 | 不适用 | 否 | 否 |
| ReFlow round $k$ vs $k+1$ | 端点设计上同 | 否 | objective/coupling 已变 | 否 | 否 |

“目标是”表示方法旨在匹配相应 $p_t$，仍依赖 exact field、正则性与训练成功；不是给任意 neural network 的无条件事实。

## 九、证据六级

| 级别 | 例子 | 写作口径 |
|---|---|---|
| exact identity | $p_ts_t=\nabla p_t$、loss Pythagorean | 可完整重推并做特例 |
| theorem | reverse-time diffusion、convex-cost non-increase | 写全假设与结论对象 |
| continuous idealization | exact score + exact ODE/SDE | 明示尚无 finite network/solver |
| numerical proposition | 某阶 solver 的局部/全局误差 | 给 smoothness、步长、稳定域 |
| controlled experiment | equal-NFE/architecture/data 比较 | 报告 seed、误差条与协议 |
| hypothesis/open problem | “直路径更容易学”等机制解释 | 给竞争解释与可证伪实验 |

## 十、一个统一声明的审计模板

遇到“方法 A 等价于方法 B”，逐项填：

1. **对象**：分布、PDE、loss、gradient、trajectory 还是 sampler？
2. **方向**：数据→噪声还是噪声→数据？
3. **假设**：density positivity、regularity、exact score、infinite capacity？
4. **等价类型**：恒等、相差常数、同 minimizer、连续极限还是经验近似？
5. **误差**：model、Monte Carlo、coupling、solver、terminal mismatch 哪些未覆盖？
6. **证据**：博客推导、原 theorem、官方实现还是受控复现？

只要其中任一项空白，就不要写“本质相同”。

## 十一、科学空间研读框

科学空间的连续生成系列提供了少见的长链条：

- [[S-2022-Su-9209-扩散模型SDE篇]] 与 [[S-2022-Su-9228-概率流ODE]]：SDE/ODE 同边缘主线；
- [[S-2022-Su-9305-万有引力到扩散模型]]：PFGM 展示 score diffusion 之外的场构造；
- [[S-2022-Su-9379-构建ODE一般步骤中]] 与 [[S-2023-Su-9497-构建ODE一般步骤下]]：conditional path、CFM 与 ReFlow；
- [[S-2023-Su-9467-W距离与得分匹配]]：展示 theorem 假设与直觉证明缺口不能省略。

本节不把这些文章拼成“大统一口号”，而用 [[S-2021-Song-Score-SDE]]、[[S-2023-Lipman-Flow-Matching]]、[[S-2022-Liu-Rectified-Flow]] 与 [[S-2025-Albergo-Stochastic-Interpolants]] 分别约束方法定义和 theorem 边界。

## 十二、图：统一的不是全部对象

先看图回答：一条 probability path 向右分叉成 ODE 与 SDE 后，哪些节点仍共享，哪些账本已经分离？

![[00-知识库管理/_assets/figures/generative-models/fig-diffusion-flow-equivalence-evidence-v1.svg|900]]

> [!figure] 图 50.7-08　Diffusion、Flow 与 Rectified Flow 的对象—等价—证据地图
> 中心是 density path/continuity equation，向外连接 score、velocity、conditional regression、SDE/ODE 与 finite solver；线型区分恒等、带条件定理和经验接口。来源：据 Score-SDE、Flow Matching、Rectified Flow 与 stochastic interpolants 独立绘制。

**怎样读图**：从中心向外走，每跨一条边先看标签是 identity、theorem 还是 empirical；到达 sampler 后必须再经过 model error 与 numerical error 两个门。

**图没有证明什么**：图不证明所有方法可用同一网络无损互换，不证明共享 $p_t$ 就共享 coupling，也不证明统一框架能预测任一 benchmark 的优劣。

## 十三、本节回顾与训练

- 同一 density path 可以有 ODE 与一族 SDE，但 path law 不同；
- score diffusion 与 FM 可通过 continuity/conditional expectation 相接；
- diffusion 的 $v$-parameterization 只在特定时间坐标下等于 instantaneous velocity；
- 可换算 target、同 population objective、同 finite program 是不同层；
- 每个统一主张都要标对象、方向、假设、误差和证据；
- [[习题 - Diffusion、Flow、速度参数化与统一证据地图]]
- [[解答 - Diffusion、Flow、速度参数化与统一证据地图]]
