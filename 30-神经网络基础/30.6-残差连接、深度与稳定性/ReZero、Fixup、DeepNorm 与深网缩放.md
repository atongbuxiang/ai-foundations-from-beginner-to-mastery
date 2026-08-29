---
type: derivation
status: draft
area: [neural-networks/residual-stability, initialization, residual-scaling, transformers]
aliases: [Ultra-Deep Residual Scaling, ReZero Fixup DeepNorm]
node_id: NN-47
prerequisites: ["[[残差缩放、Lipschitz 界与深度稳定性]]", "[[LSUV、Fixup 与现代初始化诊断]]", "[[偏置、输出层与零初始化的对称性边界]]", "[[Pre-Activation、Pre-Norm 与 Post-Norm 残差]]"]
related: ["[[正交初始化与 Dynamical Isometry]]", "[[深度、有效路径与稳定性证据地图]]", "[[自适应优化方法]]"]
sources: ["[[S-2021-Bachlechner-ReZero]]", "[[S-2019-Zhang-Dauphin-Ma-Fixup]]", "[[S-2022-Wang-DeepNet-DeepNorm]]", "[[S-2021-Su-8978-千层Transformer困难]]", "[[S-2022-Su-8994-Why-Residual]]"]
exercises: ["[[习题 - ReZero、Fixup、DeepNorm 与深网缩放]]"]
solutions: ["[[解答 - ReZero、Fixup、DeepNorm 与深网缩放]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-ultradeep-scaling-methods-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---

# ReZero、Fixup、DeepNorm 与深网缩放

> [!abstract] 本章主问题
> ReZero、Fixup 与 DeepNorm 都试图控制极深网络的初始化或更新，但作用对象不同：ReZero 用零初始化的运行时 gate 令状态映射从恒等开始；Fixup 在无归一化 residual network 中对 branch 权重做深度缩放并把末层置零；DeepNorm 在 Post-LN Transformer 中同时使用运行时 shortcut 系数 $\alpha$ 与指定权重的初始化系数 $\beta$。比较它们必须分开 state Jacobian、parameter gradient、parameter update 和 normalization 合同。

## 课程位置与两遍学习路线

- **承接什么：** NN-44 给出 $\sum|\alpha_\ell|L_\ell$ 的一般尺度账，NN-45 固定了 placement，NN-32 已介绍 Fixup 的完整 recipe；
- **本页解决什么：** 把 ReZero、Fixup 与 DeepNorm 分别放入 forward state、state Jacobian、parameter gradient、parameter update 四本账，防止仅凭“都有 depth scale”混搭；
- **后续为何需要：** NN-48 将把这些方法的理论对象和实验结论放入统一证据梯，区分初始化证书与训练全程事实。

**第一遍只问 scale 乘在哪里。** ReZero 乘 branch output 且从 0 学；Fixup 缩初始化权重并 zero-last；DeepNorm 在 Post-LN 中运行时缩 shortcut、初始化时缩指定 branch weights。

**第二遍再追第一步学习。** 分别计算 state Jacobian、gate/末层/早层梯度、相对 update，并核对 normalization、架构位置与论文深度变量。

### 问题链

1. ReZero 为何在初始化时 state Jacobian 为 $I$，branch 参数梯度却为 0？
2. zero-last Fixup 为什么末层能先学，而更早 branch 层暂时没有梯度？
3. Fixup 的 $L^{-1/(2m-2)}$ 控制哪个链式幅度？
4. DeepNorm 的运行时 $\alpha$ 与初始化 $\beta$ 为什么不能合成一个系数理解？
5. 两种 recipe 偶然出现相同数值时，怎样证明它们仍是不同方法？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal R_\square$ 上算出 ReZero 的 gate gradient $-9/5$、Fixup 的 $L=4,m=3$ 缩放 $1/\sqrt2$，并得到 encoder-only DeepNorm 的 $\alpha=2^{3/4},\beta=2^{-5/4}$，就已掌握本页主干。

## 符号与对象账本

| 方法/量 | 乘在哪里 | 初始化时是否仍在前向 | 第一时刻主要学习对象 |
|---|---|---|---|
| ReZero $\rho_\ell$ | branch output | $\rho_\ell=0$，stack 为 identity | gate 先学，branch 参数被 $\rho$ 阻断 |
| Fixup $s_L$ | branch 内非末层 weights | 缩放后的特征存在，末层 output 为 0 | zero-last 先学 |
| Fixup scalar bias/multiplier | branch 内指定位置 | 按 recipe 初始化 | 补平移/尺度自由度 |
| DeepNorm $\alpha$ | Post-LN residual shortcut | 训练与推理始终存在 | 固定，不由 optimizer 学 |
| DeepNorm $\beta$ | 指定 weights 的 initialization | 之后只是参数初值 | 参数正常学习 |

### 贯穿算例 $\mathcal R_\square$：同一个数字可以来自三本不同的账

仍取

$$
A=\operatorname{diag}\left(\frac15,-2\right),
\qquad
x=(1,-1)^{\mathsf T},
\qquad
g=(1,-1)^{\mathsf T}.
$$

#### ReZero：先开 gate

令

$$
x^+=x+\rho Ax,
\qquad
\rho(0)=0.
$$

由于

$$
Ax=\left(\frac15,2\right)^{\mathsf T},
$$

初始化时

$$
x^+=x,
\qquad
J_x=I,
\qquad
\nabla_\theta L=0,
$$

但 gate gradient 为

$$
\boxed{
\frac{\partial L}{\partial\rho}
=g^{\mathsf T}Ax
=\frac15-2
=-\frac95
}.
$$

无动量 SGD、$\eta=0.01$ 会给出 $\rho^+=0.018$；随后 branch parameters 才获得非零 scale。

#### Fixup：缩初始化链并让末层先学

取 $L=4$ 个 residual branches、每个 branch 有 $m=3$ 个 weight layers。非末层的附加 amplitude scale 是

$$
s_{\mathrm{Fixup}}
=L^{-1/(2m-2)}
=4^{-1/4}
=\frac1{\sqrt2}.
$$

两个非末层相乘的 branch amplitude scale 为

$$
s_{\mathrm{Fixup}}^{m-1}=\frac12=L^{-1/2},
$$

平方尺度为 $1/4$。末层置零使 branch output 初始为 0，但末层对已有 hidden features 的梯度通常非零。

#### DeepNorm：运行时 shortcut 与初始化 branch 分账

对 encoder-only $N=4$：

$$
\alpha_{\mathrm{DN}}=(2N)^{1/4}=8^{1/4}=2^{3/4}\approx1.681793,
$$

$$
\beta_{\mathrm{DN}}=(8N)^{-1/4}=32^{-1/4}=2^{-5/4}\approx0.420448.
$$

恰有

$$
\alpha_{\mathrm{DN}}\beta_{\mathrm{DN}}
=2^{-1/2}
=\frac1{\sqrt2}
=s_{\mathrm{Fixup}}.
$$

这个数值巧合不表示方法等价：DeepNorm 的 $\alpha$ 运行时乘 shortcut，$\beta$ 只初始化指定 FFN/value/output weights，并且最外层仍有 Post-LN；Fixup 的 $1/\sqrt2$ 直接缩无 normalization branch 内的非末层 weights。

## 核心公式七问：四本深度账

| 问题 | 本页的回答 |
|---|---|
| 目的 | 比较超深方法究竟控制 state、state Jacobian、parameter gradient 还是 parameter update |
| 对象 | 完整 recipe 加架构/normalization/optimizer 合同，不是孤立 scale 数字 |
| 来路 | 对每种前向式分别求 state 与 parameter differentials，再读原论文深度参数化 |
| 步骤 | 定 placement→定位 scale→算 step-0 map/Jacobian→算各参数梯度→追训练后变化 |
| 读法 | 相同数值若乘在不同对象、存在于不同生命周期，就不具有相同语义 |
| 检查 | step-0 identity、gate/末层/早层梯度、branch ratio、update ratio 与原 recipe 对照 |
| 去路 | ultra-deep Transformer/CNN、初始化消融、mup/DeepNorm 与稳定性证据地图 |

### AI / 系统对应

复现实验必须报告 layer/branch count 定义、Pre/Post placement、norm 类型、哪些 weights 乘 scale、gate/zero-last 初始化、optimizer 与 warm-up。把 ReZero、Fixup、DeepNorm 任意叠加会同时改变多个机制；若要研究组合方法，应把它作为新参数化，重新建立 step-0 梯度和训练全程的消融证据。

## 一、学习目标

读完本节，你应能：

1. 写出 ReZero、Fixup 与 DeepNorm 的准确方法合同；
2. 推导 ReZero 第一时刻 state/parameter/gate 三类梯度；
3. 解释 Fixup 的 zero-last 为什么不同于全网全零；
4. 计算 Fixup 的 $L^{-1/(2m-2)}$ 缩放；
5. 区分 DeepNorm 的运行时 $\alpha$ 与初始化 $\beta$；
6. 复现 encoder-only、decoder-only 与 encoder–decoder 的系数公式；
7. 识别理论更新界的假设边界与混搭方法的隐性变更。

## 二、极深训练至少有四本账

考虑

$$
x_{\ell+1}
=S_\ell(x_\ell)+a_\ell F_\ell(x_\ell;\theta_\ell).
$$

“稳定”至少可能指：

1. **forward state**：$\|x_\ell\|$、branch/state ratio 不爆炸；
2. **state Jacobian**：$\partial x_L/\partial x_0$ 的 singular values；
3. **parameter gradient**：$\nabla_{\theta_\ell}\mathcal L$ 的大小与相关性；
4. **parameter update**：$\|\Delta\theta\|/\|\theta\|$ 或 function change。

使初始 state Jacobian 等于 $I$，不代表每个参数第一步都获得非零梯度；控制 expected parameter update，也不代表输入扰动的 worst-case Lipschitz 常数小。

## 三、ReZero 的前向合同

ReZero 在每个 residual branch 前加入一个可学习标量：

$$
\boxed{
x_{\ell+1}
=x_\ell+\alpha_\ell F_\ell(x_\ell;\theta_\ell),
\qquad
\alpha_\ell(0)=0
}.
$$

在初始化时，若首尾没有其他非恒等层，整条 residual stack 为

$$
x_L=x_0.
$$

单块 state Jacobian 为

$$
J_\ell
=I+\alpha_\ell J_{F_\ell},
$$

故初始化时

$$
J_\ell=I,
\qquad
J_{0\to L}=I.
$$

这给出初始 dynamical-isometry 基线；训练后 $\alpha_\ell\ne0$，结论必须重新测量。

## 四、ReZero 的第一步梯度

令上游列梯度为

$$
g_{\ell+1}=\nabla_{x_{\ell+1}}\mathcal L.
$$

对 branch 参数：

$$
\boxed{
\nabla_{\theta_\ell}\mathcal L
=\alpha_\ell
J_{\theta_\ell}F_\ell(x_\ell;\theta_\ell)^\mathsf T
g_{\ell+1}
}.
$$

所以初始化 $\alpha_\ell=0$ 时，branch 内参数的第一步梯度为零。

对 gate：

$$
\boxed{
\frac{\partial\mathcal L}{\partial\alpha_\ell}
=g_{\ell+1}^\mathsf T F_\ell(x_\ell;\theta_\ell)
}.
$$

只要 branch 输出与上游梯度不正交，gate 先动；之后 branch 才逐渐获得梯度。ReZero 的学习启动顺序是“先开门，再改分支”。

## 五、ReZero 手算与死锁边界

若某层

$$
F(x)=3,
\qquad
g^+=2,
\qquad
\alpha=0,
$$

则

$$
\frac{\partial\mathcal L}{\partial\alpha}=2\times3=6,
$$

而

$$
\nabla_\theta\mathcal L=0.
$$

用学习率 $\eta=0.01$ 的无动量 SGD，

$$
\alpha^+=0-0.01\times6=-0.06.
$$

若同时把 branch 构造为

$$
F(x;\theta)=0
$$

且 $J_\theta F$ 也被 $\alpha=0$ 乘掉，则 gate 与 branch 都可能在第一步为零梯度。这说明“多加一个零 gate”和“分支输出也精确置零”不能未经分析地叠加。

## 六、Fixup 的目标与结构

Fixup 面向**不使用 normalization** 的 residual networks。设网络有 $L$ 个 residual branches，每个 branch 含 $m\ge2$ 个 weight layers。其核心做法是：

1. 按常规初始化 branch 内权重；
2. 将每个 branch 内除末层外的权重按

   $$
   \boxed{L^{-1/(2m-2)}}
   $$

   缩放；
3. 将每个 residual branch 的末层权重置零；
4. 将分类器权重置零（按原方法合同）；
5. 在 branch 中加入标量 bias，并在末层前加入可学习 scalar multiplier。

这些 scalar 参数不是装饰；它们补偿 normalization 移除后，优化所需的平移与缩放自由度。

## 七、Fixup 的 zero-last 梯度路径

以两层 branch 为例：

$$
F(x)=W_2\phi(W_1x).
$$

初始化 $W_2=0$，则

$$
F(x)=0,
\qquad
x^+=x.
$$

但

$$
\nabla_{W_2}\mathcal L
=g^+\phi(W_1x)^\mathsf T
$$

通常非零；另一方面

$$
\nabla_{W_1}\mathcal L
=W_2^\mathsf T g^+\odot\phi'(W_1x)x^\mathsf T
=0.
$$

所以末层先学，较早 branch 层随后获得梯度。这与“所有权重都为零”导致隐藏单元对称且无有用特征不同。

## 八、Fixup 缩放手算

若

$$
m=2,
\qquad
L=100,
$$

则指数为

$$
-\frac1{2m-2}=-\frac12,
$$

所以非末层缩放为

$$
100^{-1/2}=0.1.
$$

若 $m=3,L=256$，则

$$
256^{-1/4}=\frac14.
$$

这里 $L$ 是 residual branches 的数目，$m$ 是每个 branch 的 weight-layer 数；把总网络层数随意代入两个位置会得到错误 scale。

## 九、DeepNorm 的前向合同

DeepNorm 修改 Post-LN Transformer 的 residual sublayer：

$$
\boxed{
x_{\ell+1}
=\operatorname{LN}\!\left(
\alpha x_\ell+G_\ell(x_\ell;\theta_\ell)
\right)
}.
$$

它包含两类不同系数：

- $\alpha$：固定的运行时 shortcut scale，训练和推理都存在；
- $\beta$：只在初始化时缩放指定权重，之后参数自由训练。

因此 DeepNorm 不是 ReZero：它不是零 gate，也不从精确 identity map 开始；after-addition LayerNorm 仍在最外层。

## 十、DeepNorm 的 depth-dependent 公式

令 $N$ 为 encoder 层数、$M$ 为 decoder 层数。论文给出的参数化为：

| 架构位置 | $\alpha$ | $\beta$ |
|---|---:|---:|
| encoder-only，$N$ 层 | $(2N)^{1/4}$ | $(8N)^{-1/4}$ |
| decoder-only，$M$ 层 | $(2M)^{1/4}$ | $(8M)^{-1/4}$ |
| encoder–decoder 的 encoder | $0.81(N^4M)^{1/16}$ | $0.87(N^4M)^{-1/16}$ |
| encoder–decoder 的 decoder | $(3M)^{1/4}$ | $(12M)^{-1/4}$ |

encoder-only 取 $N=100$：

$$
\alpha=200^{1/4}\approx3.7606,
$$

$$
\beta=800^{-1/4}\approx0.1880.
$$

不要把 encoder-only 公式机械复制到 encoder–decoder 两侧。

## 十一、哪些权重乘 $\beta$

按 DeepNorm 原方法，$\beta$ 用于缩放：

- FFN 的权重；
- attention 的 value projection；
- attention 的 output projection。

query/key projections 不按同一条规则缩放。若实现把所有矩阵都乘 $\beta$，那是新方法，需要独立实验与理论，不能仍声称严格复现 DeepNorm。

## 十二、DeepNorm 理论对象的边界

DeepNet 的推导围绕特定初始化和优化近似下的**模型更新量**建立深度依赖界。可靠表述应保留：

- 对象是 expected/model update，而非任意输入的 global Lipschitz 常数；
- 推导在初始化附近使用结构与随机性假设；
- 经验训练使用的 optimizer 和完整非线性轨迹比理想化推导更复杂；
- 论文实验支持指定 Transformer 配置，不形成任意深网的无条件稳定定理。

“论文成功训练到 1000 层”是重要系统证据，但层定义、参数、数据、精度、优化预算和硬件都必须随结论保留。

## 十三、三种方法逐项比较

| 项目 | ReZero | Fixup | DeepNorm |
|---|---|---|---|
| 原始目标架构 | residual/Transformer | 无 normalization ResNet | Post-LN Transformer |
| 运行时新增 scale | 可学习 $\alpha_\ell$ | scalar multiplier/bias | 固定 $\alpha$ |
| 初始化 scale | gate 为 0 | $L^{-1/(2m-2)}$ | 指定权重乘 $\beta$ |
| 初始 stack 映射 | 条件下精确 identity | residual branches 为零 | 一般非 identity |
| 初始 state Jacobian | residual stack 为 $I$ | 受首尾与 shortcut 决定 | 含 $J_{\mathrm{LN}}$ |
| 第一时刻 branch 内梯度 | 被 gate 乘零 | 末层先非零 | 一般非零 |
| normalization 依赖 | 原方法可无 norm | 原方法无 norm | 必须按 Post-LN 合同 |
| 主要理论账本 | dynamical isometry/训练经验 | depth-scaling 更新量 | expected model update bound |

## 十四、为什么不能随意混搭

把 ReZero、zero-last、Pre-Norm、DeepNorm $\alpha/\beta$ 与不同 optimizer 同时叠加，会同时改变：

1. 初始函数；
2. 哪些参数第一步有梯度；
3. effective learning rate；
4. weight decay 相对强度；
5. normalization 输入分布；
6. 低精度下 branch/state ratio；
7. 理论证明的前提。

混搭不是禁止的，但必须换一个方法名并做逐组件消融。尤其当参数重缩放后，相同 nominal learning rate 不代表相同 update-to-weight ratio。

## 十五、训练与系统诊断

对极深缩放至少逐层记录：

- $\|x_\ell\|_{\mathrm{RMS}}$ 与 $\|F_\ell\|/\|x_\ell\|$；
- gate/$\alpha_\ell$ 的分布与更新；
- parameter gradient norm 和 update-to-weight ratio；
- JVP/VJP gain 与部分 singular-value 估计；
- activation finite/nonzero fraction；
- residual add 前后的 dtype、ulp ratio 与 absorption；
- loss spike、吞吐、显存与通信。

公平比较同时报告 natural protocol 与 matched-update protocol：前者保留相同 optimizer schedule，后者尽量匹配初始 update-to-weight，帮助识别“架构改进”是否只是隐式学习率变化。

## 十六、图：三种极深缩放方法

先看图回答：ReZero 初始化时谁先获得梯度？Fixup 的 $m,L$ 分别表示什么？DeepNorm 的 $\alpha$ 与 $\beta$ 哪个存在于运行时？

![[00-知识库管理/_assets/figures/neural-networks/fig-ultradeep-scaling-methods-v2.svg|900]]

> [!figure] 图 30.6-07　ReZero、Fixup 与 DeepNorm 的作用位置和首步账本
> 左栏展示 ReZero 的 gate/branch 梯度分层；中栏记录 Fixup 的 depth-aware scale 与 zero-last；右栏区分 DeepNorm 的运行时 $\alpha$ 和初始化 $\beta$。来源：依据 Bachlechner et al. 2021、Zhang et al. 2019、Wang et al. 2022/2024 与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_residual_advanced_v2.py]] 确定性生成。

**怎样读图**：先看 scale 乘在 shortcut、branch output 还是参数初始化上，再问它是否在训练/推理期继续存在，最后沿反向图检查哪些参数第一步被零因子阻断。

**图没有证明什么**：图中的初始化数值不证明训练全程 Jacobian 稳定，也不证明三个方法可无代价互换或组合。

## 十七、最小验收

1. 推导 ReZero 的 state、gate 与 branch-parameter gradients；
2. 复算 $F=3,g=2$ 的 gate 第一步；
3. 用两层 branch 推导 Fixup zero-last 的梯度顺序；
4. 复算 $m=2,L=100$ 与 $m=3,L=256$ 的 Fixup scale；
5. 背写并解释 DeepNorm 四组 $\alpha/\beta$；
6. 指出 DeepNorm 哪些 attention 权重乘 $\beta$；
7. 设计 natural/matched-update 双协议消融。

> [!summary]
> 极深缩放没有一个统一旋钮。ReZero控制初始状态映射和 gate 开启顺序，Fixup控制无归一化 residual branch 的深度依赖更新，DeepNorm控制 Post-LN Transformer 的 shortcut 与指定初始化权重。只有把 state、gradient、update、normalization 与系统精度分账，方法比较才有意义。

- [[残差连接、深度与稳定性 MOC]]
- [[习题 - ReZero、Fixup、DeepNorm 与深网缩放]]
- [[解答 - ReZero、Fixup、DeepNorm 与深网缩放]]
