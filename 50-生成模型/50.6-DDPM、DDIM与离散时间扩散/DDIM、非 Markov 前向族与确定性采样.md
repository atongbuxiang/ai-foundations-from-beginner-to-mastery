---
type: model
status: verified
area: [generative-models, diffusion, ddim]
node_id: GEN-46
prerequisites: ["[[数据、噪声、速度与 Score 参数化]]", "[[DDPM 反向后验、ELBO 与逐步 KL]]"]
related: ["[[条件核、边缘一致性与统一离散扩散框架]]", "[[生成模型完整课程地图与掌握标准]]"]
sources: ["[[S-2022-Su-9181-DDIM]]", "[[S-2021-Song-DDIM]]"]
exercises: ["[[习题 - DDIM、非 Markov 前向族与确定性采样]]"]
solutions: ["[[解答 - DDIM、非 Markov 前向族与确定性采样]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-ddim-marginal-joint-sampler-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# DDIM、非 Markov 前向族与确定性采样

> [!abstract] 一句话结论
> Denoising Diffusion Implicit Model（DDIM）保留训练所见的 $q(x_t|x_0)$ 边缘，却构造不同的非 Markov joint path；因此同一 denoiser 可配一族 reverse samplers。$\eta=0$ 时给定初始 noise 后路径确定，但大跳步仍有 model/solver error，不是自动 exact inversion。

## 一、same marginal 不决定 same joint

训练 simple loss 只抽 $(x_0,t,\epsilon)$ 并构造

$$x_t=a_tx_0+\sigma_t\epsilon.$$

它只依赖每个 $q(x_t|x_0)$，没有观察 $x_s,x_t$ 的 joint coupling。因此可以构造多个 $q(x_{1:T}|x_0)$ 共享这些 marginals，却有不同 temporal correlation 和 reverse conditionals。

## 二、一般一步/跳步 DDIM 更新

从当前时刻 $t$ 跳到较早 $s<t$。先由网络得到

$$\hat x_0=\frac{x_t-\sigma_t\hat\epsilon_t}{a_t}.$$

定义 stochasticity $\sigma_{t\to s}^{DDIM}\ge0$，更新

$$
\boxed{x_s=a_s\hat x_0
+\sqrt{1-a_s^2-(\sigma_{t\to s}^{DDIM})^2}\,\hat\epsilon_t
+\sigma_{t\to s}^{DDIM}z,\quad z\sim N(0,I).}
$$

常用 parameterization

$$
\sigma_{t\to s}^{DDIM}
=\eta\sqrt{\frac{1-\bar\alpha_s}{1-\bar\alpha_t}}
\sqrt{1-\frac{\bar\alpha_t}{\bar\alpha_s}}.
$$

$\eta=0$ 时删除新随机噪声；相邻时刻且 $\eta=1$ 与 DDPM-style variance 关系对齐。实现必须验证根号内非负。

## 三、确定性到底指什么

当 $\eta=0$，给定 $x_T$、conditioner、network parameters、timestep sequence 和数值实现，输出路径确定。这不表示：

- 不需要多次 network evaluation；
- 不同初始 $x_T$ 得同一输出；
- 可从真实 $x_0$ 无误差反演到唯一 $x_T$；
- 任意跳步保持 DDPM 的 path law；
- denoiser 不准确时仍采到数据分布。

## 四、为何可取时间子序列

若网络对所有训练时刻学到 conditional denoising field，可选择

$$T=\tau_K>\tau_{K-1}>\cdots>\tau_0=0$$

只在这些点调用。NFE 从 $T$ 降为 $K$，每一跳更大，discretization/model extrapolation error 通常上升。训练目标包含这些时刻，不代表大步 transition 被直接监督。

## 五、标量手算

取 $a_t=0.6,\sigma_t=0.8$，$a_s=0.8,\sqrt{1-a_s^2}=0.6$，$x_t=1$，$\hat\epsilon=-0.5$。先

$$\hat x_0=(1-0.8(-0.5))/0.6=7/3.$$

$\eta=0$ 更新

$$x_s=0.8(7/3)+0.6(-0.5)=47/30\approx1.5667.$$

若先 clip $\hat x_0$ 到 $[-1,1]$，结果变为 $0.5$；clipping 显著改变 sampler，因此必须报告。

## 六、DDIM 与 ODE 接口

确定性 DDIM 在连续时间极限与 probability-flow/ODE 视角相连，但有限离散公式、time grid 与 network parameterization 仍定义具体 numerical method。详细 solver order/stability 留到 50.7/50.9；本节不把“ODE connection”写成任意有限步 exact equality。

## 七、科学空间研读框

[[S-2022-Su-9181-DDIM]]突出两点：训练由 $\bar\alpha_t$ 边缘决定，以及子序列可加速。[[S-2021-Song-DDIM]]承担非 Markov construction、$\eta$ sampler 与原始实验。本节把 shared marginal、different joint、same training objective 和 faster finite sampler 分为四层。

## 八、图：同一组边缘怎样容纳不同路径

先看图回答：竖向的 marginal slices 相同，为什么横向连线和 reverse sampler 可以不同？

![[00-知识库管理/_assets/figures/generative-models/fig-ddim-marginal-joint-sampler-v1.svg|900]]

> [!figure] 图 50.6-06　共享 $q(x_t|x_0)$ 边缘、不同 joint coupling 与 $\eta$ sampler
> 左侧两条 path 拥有相同时间切片，中间列 deterministic/stochastic update，右侧用 timestep subsequence 表示 NFE—误差折中。来源：据 DDIM 原论文独立绘制。

**怎样读图**：竖切面只规定每个时刻 distribution；跨时刻连线规定 joint。训练 denoiser 看切面，采样算法选择一条连线/离散化。

**图没有证明什么**：图不证明跳步误差单调、不证明 deterministic sample 更好，也不证明任何 shared-marginal process 都有同一 ELBO 或可用 sampler。

## 九、本节回顾与训练

- marginals 不唯一决定 joint process；
- DDIM 可复用 DDPM denoising training；
- $\eta$ 控制新增随机性，timestep subsequence 控制 NFE；
- deterministic 是条件于初始 noise/网络/grid 的程序属性；
- [[习题 - DDIM、非 Markov 前向族与确定性采样]]
- [[解答 - DDIM、非 Markov 前向族与确定性采样]]
