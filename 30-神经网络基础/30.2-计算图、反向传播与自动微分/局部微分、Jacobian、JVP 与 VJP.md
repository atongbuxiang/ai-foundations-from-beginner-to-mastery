---
type: concept
status: draft
area: [neural-networks/differentiation, jacobian, jvp, vjp]
aliases: [Local Differential, Neural JVP VJP]
node_id: NN-10
prerequisites: ["[[计算图、拓扑序与前向执行]]", "[[Jacobian、JVP 与 VJP]]", "[[全微分与 Fréchet 导数]]"]
related: ["[[标量链式法则与反向传播递推]]", "[[线性层与仿射层的反向传播]]", "[[Forward_Reverse AD、Tape 与复杂度|Forward/Reverse AD、Tape 与复杂度]]"]
sources: ["[[S-2018-Baydin-AD-Survey]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]"]
exercises: ["[[习题 - 局部微分、Jacobian、JVP 与 VJP]]"]
solutions: ["[[解答 - 局部微分、Jacobian、JVP 与 VJP]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-local-jacobian-jvp-vjp-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---
# 局部微分、Jacobian、JVP 与 VJP

> [!abstract] 本章主问题
> 节点的真正一阶对象是局部线性算子 $Df(x)$。Jacobian 只是选定坐标后的完整表；JVP 把输入扰动向前推，VJP 把输出协向量向后拉。大网络通常不物化 Jacobian，而沿计算图组合这些线性作用。

## 课程位置与两遍学习路线

- **承接什么：** NN-09 已得到一张可执行图和完整 forward trace，但每个节点还只有数值规则，没有一阶变化规则；
- **本页解决什么：** 以 differential 为本体，统一 Jacobian、JVP 与 VJP，并用同一个矩阵任务验证前推和回拉的点积一致性；
- **后续为何需要：** NN-11 会把局部 VJP 按逆拓扑序动态规划，NN-12 则给 affine primitive 写出不物化 Jacobian 的闭式 VJP。

**第一遍只追踪方向与 shape。** 记住 $J:[m,n]$、$v:[n]$、$Jv:[m]$、$u:[m]$、$J^Tu:[n]$；把 JVP 看作输入扰动的前推，把 VJP 看作输出线性 functional 的回拉。

**第二遍再进入算子视角。** 从 Fréchet 一阶模型重建局部微分，证明伴随点积恒等式，并检查 batch、broadcast、reduction 和不可微 primitive 的程序约定。

### 问题链

1. 为什么“偏导数表”不是导数最本质的定义？
2. JVP 和 VJP 分别回答哪一种一阶问题？
3. 为什么 VJP 是 transpose/adjoint action，而不是 Jacobian inverse？
4. 一个 scalar loss 对海量参数为何只需要一个 reverse seed？
5. 怎样不形成完整 Jacobian，也能检验局部前向与反向实现相互一致？

> [!check] 第一遍停靠线
> 若你能根据输入输出 shape 判断 JVP/VJP 方向，并在贯穿算例中得到 directional derivative $2.5$ 的两种算法，就可以进入反向递推；Fréchet 余项与复杂 primitive 留到第二遍。

## 符号与对象账本

| 对象 | shape | 几何身份 | AI 自动微分接口 |
|---|---|---|---|
| $Df(x)$ | 线性算子 $\mathbb R^n\to\mathbb R^m$ | 局部最佳一阶模型 | primitive linearization |
| $J_f(x)$ | $m\times n$ | 选定坐标后的矩阵表示 | 通常不显式形成 |
| $v$ | input-shaped | tangent/direction | JVP seed |
| $u$ | output-shaped | cotangent/linear functional | VJP seed |
| $Jv,J^Tu$ | output/input-shaped | pushforward/pullback | forward/reverse local result |

### 贯穿算例：同一个方向导数的前推与回拉

沿用 NN-09 的 $X_\diamond,W_\diamond,b_\diamond,Y_\diamond$，只扰动权重

$$
\dot W=\begin{bmatrix}1&0\\0&0\end{bmatrix},\qquad \dot X=0,\quad\dot b=0.
$$

JVP 前推得到

$$
\dot Z=X_\diamond\dot W=\begin{bmatrix}1&0\\-1&0\end{bmatrix},\qquad
\dot L=\langle R,\dot Z\rangle_F+\lambda\langle W_\diamond,\dot W\rangle_F=2+0.5=2.5.
$$

若从 scalar seed $\bar L=1$ 做 VJP，权重 cotangent 将是 $\bar W=X_\diamond^TR+\lambda W_\diamond$；暂时只取其与 $\dot W$ 的配对，也得到 $\langle\bar W,\dot W\rangle_F=2.5$。这就是 $u^T(Jv)=(J^Tu)^Tv$ 在矩阵参数空间中的 Frobenius 版本。

## 核心公式七问：$\langle u,Jv\rangle=\langle J^*u,v\rangle$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 用同一个 scalar pairing 连接 tangent 前推与 cotangent 回拉 |
| 对象 | $J$ 是局部导数，$J^*$ 是由所选内积定义的 adjoint，不要求方阵或可逆 |
| 来路 | 将 $\delta y=J\delta x$ 代入输出 functional $\langle u,\delta y\rangle$ |
| 步骤 | 先做 JVP 再与 $u$ 配对，或先做 VJP 再与 $v$ 配对，结果必须一致 |
| 读法 | reverse mode 把“输出变化的价值”拉回每个输入方向的价值 |
| 检查 | 两侧都是 scalar；$J$ 矩形时仍成立；坐标 Euclidean 情形 $J^*=J^T$ |
| 去路 | dot test、reverse accumulation、matrix-calculus VJP 与 implicit differentiation |

### 贯穿图的局部规则卡

下表只描述单个 primitive；NN-11 才负责按图组合。`dot` 表示 tangent，`bar` 表示 cotangent。

| forward primitive | JVP | 给定输出 `bar` 的 VJP |
|---|---|---|
| $Z=XW$ | $\dot Z=\dot XW+X\dot W$ | $\bar X=\bar ZW^T,\ \bar W=X^T\bar Z$ |
| $Z=A+\mathbf1b$ | $\dot Z=\dot A+\mathbf1\dot b$ | $\bar A=\bar Z,\ \bar b=\mathbf1^T\bar Z$ |
| $R=Z-Y$ | $\dot R=\dot Z-\dot Y$ | $\bar Z=\bar R,\ \bar Y=-\bar R$ |
| $s=\frac12\|R\|_F^2$ | $\dot s=\langle R,\dot R\rangle_F$ | $\bar R=\bar sR$ |
| $r=\frac\lambda2\|W\|_F^2$ | $\dot r=\lambda\langle W,\dot W\rangle_F$ | $\bar W{+}=\bar r\lambda W$ |
| $L=s+r$ | $\dot L=\dot s+\dot r$ | $\bar s{+}=\bar L,\ \bar r{+}=\bar L$ |

逐行 shape 都闭合；最后两行的 `+=` 已预告 fan-out accumulation。它们是 AI 自动微分系统注册 primitive rule 时真正需要的接口，而不是完整 Jacobian 表。

## 一、对象与形状
若 $f:\mathbb R^n\to\mathbb R^m$，则
$$Df(x):\mathbb R^n\to\mathbb R^m,\qquad J_f(x)\in\mathbb R^{m\times n}.$$
对 $v\in\mathbb R^n$，JVP 为 $Jv\in\mathbb R^m$；对 $u\in\mathbb R^m$，VJP 为 $J^Tu\in\mathbb R^n$。

JVP 与输出同形，VJP 与输入同形。这条 shape rule 是最有效的局部检查之一。

## 二、Fréchet 一阶模型
$f$ 在 $x$ 可微表示存在唯一线性算子 $A=Df(x)$，使
$$f(x+h)=f(x)+A[h]+o(\|h\|).$$
偏导数组只有在这个统一线性近似存在时才表示 Jacobian；各坐标偏导存在本身不充分。

## 三、多输入节点
若 $z=f(x,y)$，总微分为
$$dz=D_1f(x,y)[dx]+D_2f(x,y)[dy].$$
JVP 同时读取所有输入 tangents；VJP 则把一个输出 cotangent 分别回拉到每个输入。add 节点把同一个 cotangent 传给两父节点，multiply 节点分别乘另一个 primal 值。

## 四、一个完整 Jacobian 例子
令
$$f(x_1,x_2)=(x_1x_2,\sin x_1).$$
则
$$J_f(x)=\begin{bmatrix}x_2&x_1\\\cos x_1&0\end{bmatrix}.$$
在 $(2,3)$，
$$J=\begin{bmatrix}3&2\\\cos2&0\end{bmatrix}.$$
若 $v=(1,-1)^T$，
$$Jv=(1,\cos2)^T.$$
若 $u=(4,5)^T$，
$$J^Tu=(12+5\cos2,8)^T.$$

## 五、JVP 是 Directional Pushforward
沿曲线 $x(t)=x+tv$，
$$\left.\frac d{dt}f(x(t))\right|_{t=0}=Df(x)[v]=Jv.$$
它回答“输入朝 $v$ 微小变化，输出一阶怎样变”。forward-mode AD 正是给每个 primal 同步携带 tangent。

## 六、VJP 是 Cotangent Pullback
给输出线性 functional $u^T\delta y$，代入 $\delta y=J\delta x$：
$$u^TJ\delta x=(J^Tu)^T\delta x.$$
所以输入侧 cotangent 是 $J^Tu$。这是 dual map/adjoint action，不是 $J^{-1}$，矩形或奇异 Jacobian 同样可做。

## 七、伴随点积恒等式
正确实现必须满足
$$\boxed{u^T(Jv)=(J^Tu)^Tv.}$$
随机 $u,v$ 的 dot test 可同时检查 JVP/VJP 配对；它是强诊断但有限次随机测试仍不能证明所有方向完全正确。

## 八、链式组合
若 $h=g\circ f$，
$$J_h=J_gJ_f.$$
JVP 按 $v\mapsto J_fv\mapsto J_g(J_fv)$ 前推；VJP 按 $u\mapsto J_g^Tu\mapsto J_f^T(J_g^Tu)$ 逆序回拉。无需形成 $J_gJ_f$。

## 九、为何不物化完整 Jacobian
参数数 $n$ 可达十亿，标量 loss 的 Jacobian 只有一行，但完整中间 Jacobian 可能有数万亿元素。reverse mode 只需一次 VJP seed $1$ 得全部参数 gradient，计算通常是 forward 的常数倍，代价转移到 activation storage/recompute。

若输出方向少，VJP 有利；输入 directions 少时 JVP 有利。形成 full $m\times n$ Jacobian 通常需约 $n$ 次 forward seeds 或 $m$ 次 reverse seeds。

## 十、Batch Jacobian 与梯度不是同一对象
逐样本 map $f(x_i)$ 的 per-example Jacobian 有 batch block structure；若 loss 先 sum/mean，VJP seed 已经过 reduction，得到的是 batch-aggregated parameter gradient。`grad` 默认结果不能冒充 per-example gradients。

## 十一、Broadcast 与 Reduction 的对偶
forward 把 bias $b:[d]$ 广播到 $[B,T,d]$；其 VJP 必须沿 $B,T$ 求和。forward `sum` 的 VJP 是把 cotangent 广播回所有输入；forward reshape/transpose 的 VJP 是 inverse reshape/inverse permutation。

这体现一个通则：forward 数据复制/聚合的线性算子，在 reverse 中使用其 transpose。

## 十二、不可微点与程序导数
ReLU 在零点没有唯一 classical derivative，框架选一个 convention；max tie、sort、index 和 discrete branch 也需要规则。AD 返回所执行 primitive 定义的 derivative/adjoint，不自动证明目标数学函数处处可微。

## 十三、数值验证
1. shape/type check；
2. JVP 对中心有限差分 $(f(x+hv)-f(x-hv))/(2h)$；
3. VJP/JVP dot test；
4. 小问题显式 Jacobian 对照；
5. 改 dtype 与 step size 检查 truncation/roundoff U 形曲线。

## 十四、图：一张表与两种作用
先看图回答：为什么 scalar loss 对海量参数只需要一次反向 seed，而不是存一张巨大 Jacobian？

![[00-知识库管理/_assets/figures/neural-networks/fig-local-jacobian-jvp-vjp-v2.svg|900]]

> [!figure] 图 30.2-02　局部导数算子、JVP 前推与 VJP 回拉
> 左栏区分 derivative 与坐标 Jacobian；中栏用同一局部节点对照 tangent/cotangent；右栏比较 full Jacobian、forward seeds 与 scalar-loss reverse。来源：依据 Baydin 等 2018 和本库[[Jacobian、JVP 与 VJP]]独立绘制；由 [[00-知识库管理/_labs/code/plot_backprop_foundations_v2.py]] 确定性生成。

**怎样读图**：先核对 $J:[m,n]$，再沿 JVP 正向和 VJP 反向检查形状，最后依据所需方向数选接口。

**图没有证明什么**：图没有给任意硬件上的精确成本，也没有保证 primitive 在不可微点的 convention 符合某个理论极限。

## 十五、回顾与练习
> [!summary]
> $Df$ 是本体，$J$ 是坐标表；JVP=$Jv$，VJP=$J^Tu$；反向传播由局部 VJP 逆序组合并在共享输入处累加。

- [[习题 - 局部微分、Jacobian、JVP 与 VJP]]
- [[解答 - 局部微分、Jacobian、JVP 与 VJP]]
