---
type: model
status: verified
area: [generative-models, normalizing-flows, coupling]
node_id: GEN-34
prerequisites: ["[[变量替换、基分布与 Exact Likelihood Flow]]", "[[Jacobian、JVP 与 VJP]]"]
related: ["[[Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]", "[[Autoregressive Flow、MAF 与 IAF 的方向权衡]]"]
sources: ["[[S-2018-Su-5776-NICE流模型]]", "[[S-2018-Su-5807-RealNVP与Glow]]", "[[S-2016-Dinh-RealNVP]]"]
exercises: ["[[习题 - Coupling Layer、NICE 与 RealNVP]]"]
solutions: ["[[解答 - Coupling Layer、NICE 与 RealNVP]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-flow-coupling-triangular-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Coupling Layer、NICE 与 RealNVP

> [!abstract] 一句话结论
> Coupling layer 故意让一部分坐标原样通过，并用它们变换另一部分。这样 conditioner 可以很复杂，整体 inverse 仍显式，Jacobian 仍块三角；代价是单层混合不充分，必须交替 mask、置换或通道混合。

## 一、最小问题：网络复杂，逆怎么还能便宜

把 $x\in\mathbb R^d$ 分为 $x_A\in\mathbb R^{d_A}$ 和 $x_B\in\mathbb R^{d_B}$。我们希望 $s,t$ 是任意深网络，却不愿对它们求逆。关键技巧是：让网络只产生变换参数，而不被放进待求逆的位置。

## 二、NICE 的 additive coupling

定义

$$
y_A=x_A,\qquad y_B=x_B+m(x_A).
$$

逆变换不需求 $m^{-1}$：

$$
x_A=y_A,\qquad x_B=y_B-m(y_A).
$$

Jacobian 为

$$
J=\frac{\partial y}{\partial x}
=\begin{pmatrix}
I&0\\
\frac{\partial m}{\partial x_A}&I
\end{pmatrix},
$$

所以 $\det J=1$。它能弯曲密度，却不能由 coupling 自身改变局部体积；NICE 因而另配全局 scale。

## 三、RealNVP 的 affine coupling

令 $s,t:\mathbb R^{d_A}\to\mathbb R^{d_B}$，逐元素定义

$$
\boxed{y_A=x_A,\qquad
y_B=x_B\odot e^{s(x_A)}+t(x_A).}
$$

因为 $e^{s_j}>0$，逆为

$$
\boxed{x_A=y_A,\qquad
x_B=(y_B-t(y_A))\odot e^{-s(y_A)}.}
$$

Jacobian 的右上块仍为 0，右下块是 $\operatorname{diag}(e^{s(x_A)})$，故

$$
\log|\det J|=\sum_{j=1}^{d_B}s_j(x_A).
$$

注意左下块可以很复杂，却不影响块三角 determinant。这就是架构设计换计算可行性的核心。

## 四、手算一个二维层

取 $A={1\},B={2\}$，令 $s(x_1)=\log2$，$t(x_1)=x_1$。对 $x=(1,3)$，

$$y_1=1,\qquad y_2=3\cdot2+1=7.$$

逆算：$x_1=y_1=1$，$x_2=(7-1)/2=3$。Jacobian

$$
J=\begin{pmatrix}1&0\\1&2\end{pmatrix},
\qquad \log|\det J|=\log2.
$$

代回、determinant 和 log-scale 三种检查给同一答案。

## 五、为什么一层不够

在一层里，$x_A$ 完全没被改变。若每层永远保留同一部分，某些坐标永远只做 conditioner，无法被直接塑形。常用补救是：

- 交替 checkerboard/channel mask；
- 在层间 permutation；
- 使用 [[Glow、ActNorm、可逆 1×1 卷积与多尺度结构|可逆 $1\times1$ 卷积]]学习 mixing；
- 多层堆叠，让每一维轮流被变换。

这说明“单层可逆”与“复合模型表达力充分”是两本账。

## 六、数值稳定：scale 既是表达力也是风险

若 $s=30$，$e^s\approx10^{13}$；若 $s=-30$，逆中 $e^{-s}$ 同样巨大。即使数学上非零，浮点 round-trip 和梯度都可能失真。实现通常令

$$s=\alpha\tanh(\hat s)$$

或使用其他 bounded log-scale，并记录 $\min s,\max s$。这改变了可表达尺度范围，属于模型合同，不能藏在“稳定技巧”里。

复杂度方面，若 conditioner 成本为 $C_s+C_t$，coupling 的额外 logdet 只是 $O(d_B)$ 求和；无需显式构造完整 Jacobian。

## 七、AI 中的张量合同

图像 $x\in\mathbb R^{B\times C\times H\times W}$ 可用 channel mask 分成 $x_A,x_B$。conditioner 输出与 $x_B$ 同形的 $(s,t)$。必须测试：

1. `inverse(forward(x))` 的最大/相对误差；
2. analytic logdet 与小维 autodiff Jacobian 的差；
3. mask 轮换后每个 channel 是否至少被更新；
4. scale clipping 对 likelihood、条件数和样本的消融。

## 八、科学空间研读框

[[S-2018-Su-5776-NICE流模型]]清楚展示 additive coupling 的“网络无需可逆”；[[S-2018-Su-5807-RealNVP与Glow]]把它推进到 affine coupling 与 multiscale。公式与原始模型边界由[[S-2016-Dinh-RealNVP]]承担。博客中的历史实现不作为当前框架 API 证据。

## 九、图：复杂 conditioner 为什么不破坏易求逆

先看图回答：Jacobian 中哪一个零块使 determinant 只看 scale，对应 inverse 又为什么无需反解 $s,t$ 网络？

![[00-知识库管理/_assets/figures/generative-models/fig-flow-coupling-triangular-v1.svg|900]]

> [!figure] 图 50.5-02　Affine coupling 的数据流、块三角 Jacobian 与逐元素逆
> 左侧画出保留块向 conditioner 供参、变换块被仿射更新；右侧标出 determinant 只由对角 scale 决定。来源：据 NICE/RealNVP 结构独立重绘。

**怎样读图**：先沿实线看 $x_A\to y_A$ 原样通过，再看它只生成 $s,t$ 去改变 $x_B$。逆向时 $y_A$ 已知，所以直接重算 $s(y_A),t(y_A)$，无需网络本身可逆。

**图没有证明什么**：图不证明一层 coupling 能表达任意 diffeomorphism，也不保证极端 scale 的浮点稳定，更不说明某一种 mask 在任意数据上最优。

## 十、边界与常见误用

- “conditioner 必须可逆”：错；整体结构给出显式逆。
- “additive coupling 没表达力”：错；它能剪切，但局部 determinant 为 1。
- “determinant 好算所以 Jacobian 条件好”：错；大/小 scale 可极度病态。
- “split 一半等于丢一半信息”：错；这里只是分块计算，不是丢弃。

## 十一、本节回顾与训练

你应能从定义独立写出 inverse 和块 Jacobian，手算二维例子，解释 mask 轮换，并把 logdet 正确接入上一节的编码/生成方向公式。

- [[习题 - Coupling Layer、NICE 与 RealNVP]]
- [[解答 - Coupling Layer、NICE 与 RealNVP]]

