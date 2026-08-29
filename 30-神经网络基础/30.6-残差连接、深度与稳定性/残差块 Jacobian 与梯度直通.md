---
type: derivation
status: draft
area: [neural-networks/residual-stability, jacobian, backpropagation]
aliases: [Residual Block Jacobian, Identity Gradient Rail]
node_id: NN-42
prerequisites: ["[[残差学习、恒等捷径与退化问题]]", "[[局部微分、Jacobian、JVP 与 VJP]]", "[[标量链式法则与反向传播递推]]", "[[奇异值分解]]"]
related: ["[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]", "[[Pre-Norm、Post-Norm 与归一化放置]]", "[[残差缩放、Lipschitz 界与深度稳定性]]", "[[深度、有效路径与稳定性证据地图]]"]
sources: ["[[S-2016-He-Identity-Mappings]]", "[[S-2016-He-ResNet]]", "[[S-2022-Su-8994-Why-Residual]]"]
exercises: ["[[习题 - 残差块 Jacobian 与梯度直通]]"]
solutions: ["[[解答 - 残差块 Jacobian 与梯度直通]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-residual-jacobian-rail-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---

# 残差块 Jacobian 与梯度直通

> [!abstract] 本章主问题
> 对 $x^+=x+F(x)$，局部 Jacobian 的确是 $I+J_F$，反向 VJP 的确包含一份未乘 branch 权重的上游梯度。但“含有 $I$”不等于总梯度必为 identity：branch 项可以增强、旋转或抵消直接项，跨层仍是多个 $I+J_F$ 的有序乘积。

## 课程位置与两遍学习路线

- **承接什么：** NN-41 已在 $\mathcal R_\square$ 中逐层展开 residual state，并说明 identity baseline 是函数参数化事实；
- **本页解决什么：** 对同一 block 求 JVP、VJP、singular gains 与四层有序乘积，精确定义“梯度直通”的强度；
- **后续为何需要：** NN-43 的 Euler variational equation 和 NN-44 的 Lipschitz product bound 都直接复用 $I+J_F$。

**第一遍只算一层和四层。** 先把上游 $g$ 分成 identity term 与 branch term，再乘四个 block Jacobians；亲手看到一个方向放大、另一个方向衰减。

**第二遍再做谱与路径。** 比较 singular/eigen directions、non-normality、cancellation、projection 与 normalization，并把 path expansion 视为精确代数而非独立路径概率模型。

### 问题链

1. $I$ 从计算图的哪条边进入 Jacobian 和 VJP？
2. 为什么 $g+J_F^{\mathsf T}g$ 可能比 $g$ 大、比 $g$ 小，甚至为零？
3. 单层 $\|J_F\|<1$ 能给出哪些 singular-value 界，又不能给出什么？
4. 多层 Jacobian 为什么必须按求值点有序相乘？
5. path expansion 中不同长度项为何不能未经假设就当成独立随机贡献？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal R_\square$ 中把 $g=(1,-1)$ 分成 identity term $(1,-1)$ 与 branch term $(1/20,1/2)$，得到一层 VJP $(21/20,-1/2)$ 和四层 VJP $(1.21550625,-1/16)$，就已掌握本页主干。

## 符号与对象账本

| 对象 | 定义 | 方向 | 不能混成 |
|---|---|---|---|
| $J_F(x_\ell)$ | branch 对 state 的局部 Jacobian | JVP 中向前作用 | 参数 Jacobian $J_\theta F$ |
| $M_\ell=I+J_F(x_\ell)$ | 完整 residual block Jacobian | state perturbation map | identity 保证书 |
| $v$ | JVP tangent | input→output | VJP cotangent $g$ |
| $g$ | 输出端 VJP seed | output→input，经转置作用 | forward activation |
| $\sigma_{\min},\sigma_{\max}$ | 最坏方向局部 gains | Euclidean norm | eigenvalue magnitudes |
| $M_{L-1}\cdots M_0$ | 多层 forward Jacobian | 右侧先作用 | 可交换标量乘积 |

### 贯穿算例 $\mathcal R_\square$：identity rail 与 branch 逐方向干涉

共享线性 branch 的 Jacobian 为

$$
J_F=B=
\begin{bmatrix}
1/20&0\\
0&-1/2
\end{bmatrix},
$$

所以完整 block Jacobian

$$
M=I+B
=\begin{bmatrix}
21/20&0\\
0&1/2
\end{bmatrix}.
$$

对 JVP direction $v=(1,1)^{\mathsf T}$：

$$
Mv=v+Bv
=(1,1)+\left(\frac1{20},-\frac12\right)
=\left(\frac{21}{20},\frac12\right).
$$

第一坐标 branch 与 identity 同向，第二坐标反向；同一个 block 同时含 expansion 与 contraction。

对上游 VJP seed $g=(1,-1)^{\mathsf T}$，因为本例矩阵对称，

$$
B^{\mathsf T}g
=\left(\frac1{20},\frac12\right)^{\mathsf T},
$$

因此

$$
\boxed{
g_x=g+B^{\mathsf T}g
=\left(\frac{21}{20},-\frac12\right)^{\mathsf T}
}.
$$

identity term 确实未经 branch weight 直接进入 accumulator，但第二坐标仍从 $-1$ 衰减到 $-1/2$；“有直达项”不等于“总梯度原样复制”。

四层 Jacobian 为

$$
M^4
=\begin{bmatrix}
(21/20)^4&0\\
0&(1/2)^4
\end{bmatrix}
=\begin{bmatrix}
194481/160000&0\\
0&1/16
\end{bmatrix}.
$$

所以

$$
(M^4)^{\mathsf T}g
=\left(\frac{194481}{160000},-\frac1{16}\right)
=(1.21550625,-0.0625).
$$

单层 singular values 是 $(21/20,1/2)$，四层是 $((21/20)^4,1/16)$。直接项没有阻止一个方向逐层消失，也没有阻止另一方向逐层增长。

## 核心公式七问：residual VJP

$$
\boxed{
g_{x_\ell}
=\left[I+J_F(x_\ell)\right]^{\mathsf T}g_{x_{\ell+1}}
=g_{x_{\ell+1}}+J_F(x_\ell)^{\mathsf T}g_{x_{\ell+1}}
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 把上游 cotangent 沿 shortcut 与 branch 两条输入路径拉回并累加 |
| 对象 | 固定 forward state 上的局部 VJP，不是期望梯度或训练后统计 |
| 来路 | addition 的两条 differential 加 chain rule |
| 步骤 | 保留一份 $g$→计算 branch VJP→在同一 input accumulator 相加 |
| 读法 | identity term 直接存在；总结果由两项方向关系决定 |
| 检查 | JVP/VJP 对偶 $g^TMv=(M^Tg)^Tv$；finite difference；singular-value scan |
| 去路 | Euler variational step、深层 product、residual scaling 与 effective-path evidence |

### AI / 系统对应

训练日志若只报 gradient norm，会把方向性抵消、layerwise rotation 和某些 coordinates 的消失混在一起。更可靠的 residual 诊断包括随机 JVP/VJP 对偶、branch/identity cosine、局部 singular estimates、跨深度 gain，以及 normalization/dropout realization。mixed precision 中两条路径的加法顺序和尺度差还会造成可见 rounding loss。

## 一、学习目标

读完本节，你应能：

1. 从 differential 推导 residual block 的 JVP、VJP 与参数梯度；
2. 标注每个 Jacobian 的 shape 与求值点；
3. 推导多层有序乘积与 linear path expansion；
4. 解释“直接项”为什么存在又为什么不能保证稳定；
5. 用 operator norm 给出单层 singular-value 界；
6. 构造 cancellation、放大和非正规反例；
7. 区分 eigenvalue、singular value 与 gradient direction；
8. 设计有限差分、JVP/VJP 对偶和随机方向谱诊断。

## 二、单块 differential

设

$$
F:\mathbb R^D\to\mathbb R^D,
\qquad
y=x+F(x;\theta).
$$

对输入与参数扰动 $(dx,d\theta)$，

$$
dy
=dx+J_xF(x;\theta)dx+J_\theta F(x;\theta)d\theta.
$$

因此输入 Jacobian 为

$$
\boxed{
J_xy=I_D+J_xF(x;\theta)
}.
$$

这个 $I_D$ 来自 addition 的第一条输入边，不来自近似或初始化假设。

## 三、JVP：扰动怎样向前传播

给方向 $v\in\mathbb R^D$，

$$
\operatorname{JVP}_y(x;v)
=(I+J_F)v
=v+J_Fv.
$$

几何上，输出扰动是原方向 $v$ 与 branch 造成的局部变形相加。

三种局部情形：

- $J_Fv$ 与 $v$ 同向：放大；
- $J_Fv$ 与 $v$ 反向：衰减或抵消；
- $J_Fv$ 近似正交：旋转并增加 norm。

因此只看 $\|J_Fv\|$ 不够，还要看夹角。

## 四、VJP：梯度怎样向后传播

令列向量上游余切为

$$
g_y=\nabla_y\mathcal L\in\mathbb R^D.
$$

则

$$
\boxed{
g_x=(I+J_F)^\mathsf Tg_y
=g_y+J_F^\mathsf Tg_y
}.
$$

第一项 $g_y$ 是 identity rail；第二项是 residual branch 的 VJP。二者在同一个 accumulator 中相加，所以可能相长也可能相消。

参数梯度为

$$
\boxed{
g_\theta=J_\theta F(x;\theta)^\mathsf Tg_y
}.
$$

若 block 带 scale $\alpha$，即 $y=x+\alpha F(x;\theta)$，则 state branch VJP 与参数梯度都乘 $\alpha$。

## 五、一个二维 VJP 手算

令

$$
J_F=
\begin{bmatrix}
-1/2&1\\
0&-1/2
\end{bmatrix},
\qquad
g_y=
\begin{bmatrix}1\\-1\end{bmatrix}.
$$

直接项是

$$
g_y=(1,-1)^\mathsf T.
$$

branch 项是

$$
J_F^\mathsf Tg_y
=
\begin{bmatrix}
-1/2&0\\
1&-1/2
\end{bmatrix}
\begin{bmatrix}1\\-1\end{bmatrix}
=
\begin{bmatrix}-1/2\\3/2\end{bmatrix}.
$$

所以

$$
g_x=
\begin{bmatrix}1/2\\1/2\end{bmatrix}.
$$

identity rail 存在，但总梯度既不是 $g_y$，norm 也不是自动保持。

## 六、最短反例：$I$ 可以被完全抵消

若局部

$$
J_F=-I,
$$

则

$$
I+J_F=0.
$$

该点所有输入方向的一阶变化都被取消。若 $J_F=cI$，则 block gain 为 $1+c$：

- $c=0$：gain 1；
- $c=-1$：gain 0；
- $c>0$：gain 大于 1；
- $c<-2$：绝对 gain 大于 1 且方向翻转。

所以“$I+J_F$ 不会消失”是错误命题。

## 七、单层 singular-value 界

令

$$
a=\|J_F\|_2.
$$

对任意 $v$，三角不等式给出

$$
\|(I+J_F)v\|_2
\le(1+a)\|v\|_2,
$$

反三角不等式给出

$$
\|(I+J_F)v\|_2
\ge(1-a)\|v\|_2.
$$

因此当 $a<1$ 时，

$$
\boxed{
1-a
\le\sigma_{\min}(I+J_F)
\le\sigma_{\max}(I+J_F)
\le1+a
}.
$$

并且 block 局部可逆，条件数满足

$$
\kappa_2(I+J_F)
\le\frac{1+a}{1-a}.
$$

若 $a\ge1$，下界 $1-a$ 非正，只剩平凡的 $\sigma_{\min}\ge0$，不能证明可逆。

## 八、eigenvalue 不能替代 singular value

考虑

$$
J_F=
\begin{bmatrix}
-0.9&3\\
0&-0.9
\end{bmatrix},
\qquad
I+J_F=
\begin{bmatrix}
0.1&3\\
0&0.1
\end{bmatrix}.
$$

两个 eigenvalues 都是 $0.1$，看起来“都衰减”。但该矩阵非正规，其 singular values 约为

$$
3.0033,
\qquad
0.00333.
$$

一个方向被强放大，另一个方向几乎塌缩。反向传播关心 $J^\mathsf T$ 对向量和 singular spectrum 的作用，不能只画 eigenvalue 点。

## 九、多层 Jacobian 是有序乘积

对

$$
x_{\ell+1}=x_\ell+F_\ell(x_\ell),
$$

令

$$
A_\ell=J_{F_\ell}(x_\ell).
$$

从 $x_0$ 到 $x_L$ 的 Jacobian 是

$$
\boxed{
J_{0\to L}
=(I+A_{L-1})\cdots(I+A_1)(I+A_0)
}.
$$

顺序不能交换。反向余切为

$$
g_0=(I+A_0)^\mathsf T\cdots(I+A_{L-1})^\mathsf Tg_L.
$$

## 十、linear path expansion

在线性或固定局部 Jacobian 情形，

$$
\prod_{\ell=0}^{L-1}(I+A_\ell)
$$

可展开为

$$
I
+\sum_iA_i
+\sum_{j>i}A_jA_i
+\sum_{k>j>i}A_kA_jA_i
+\cdots.
$$

每层选择 $I$ 或 $A_\ell$，形式上有 $2^L$ 条有序项。这给出“不同有效路径长度”的代数入口。

但在非线性网络中 $A_\ell$ 依赖实际 trajectory，且 activation mask、normalization 和 stochastic branch 共同改变它；不能把这 $2^L$ 项直接解释为 $2^L$ 个独立训练的子网络。

## 十一、跨层 norm 上下界

若 $a_\ell=\|A_\ell\|_2$，则

$$
\|J_{0\to L}\|_2
\le
\prod_{\ell=0}^{L-1}(1+a_\ell).
$$

若所有 $a_\ell<1$，则

$$
\sigma_{\min}(J_{0\to L})
\ge
\prod_{\ell=0}^{L-1}(1-a_\ell).
$$

这些是合法 worst-case bounds，但可能很松：不同层方向可相消，非正规矩阵可产生暂态放大，最坏 singular direction 也可能逐层变化。

## 十二、带 projection、gate 与 normalization

一般 block

$$
y=P(x)+\alpha F(N(x))
$$

的 Jacobian 是

$$
J_y
=J_P(x)
+\alpha J_F(N(x))J_N(x).
$$

只有 $P(x)=x$ 时直达项才是 $I$。若 shortcut 为 $\lambda x$，直达项是 $\lambda I$；跨层直接路径会乘 $\prod\lambda_\ell$。若 addition 后还有 norm/activation，还要左乘相应 Jacobian。

## 十三、不可微点与广义导数

若 branch 含 ReLU，$J_F$ 在 kink 处依赖 subgradient convention。工程框架通常选定一个局部导数值；有限差分若跨过 kink，可能与该 convention 不同。

因此 gradient check 应：

1. 避免恰落在 kink；
2. 记录 dtype 与 step；
3. 比较 directional derivative 而非只比逐坐标；
4. 对 stochastic layer 固定 RNG；
5. 对 BatchNorm 固定 train/eval 与 batch。

## 十四、JVP/VJP 对偶校验

对任意 $v,u\in\mathbb R^D$，正确实现应满足

$$
u^\mathsf T(Jv)
=(J^\mathsf Tu)^\mathsf Tv.
$$

这是无需显式构造 Jacobian 的强检查。对 residual block：

$$
Jv=v+J_Fv,
\qquad
J^\mathsf Tu=u+J_F^\mathsf Tu.
$$

若二者内积不一致，常见原因是 broadcast reduction、in-place 修改、detach、RNG replay 或 normalization state 不一致。

## 十五、图：identity rail、branch 干涉与谱

先看图回答：反向中哪一项不乘 branch Jacobian？为什么它仍可能被 branch 抵消？跨层路径展开和 singular-value 账本分别回答什么？

![[00-知识库管理/_assets/figures/neural-networks/fig-residual-jacobian-rail-v2.svg|900]]

> [!figure] 图 30.6-02　$I+J_F$ 提供 identity rail，但稳定性由总算子决定
> 左栏把 JVP/VJP 拆成 identity 与 branch 两项；中栏展示 cancellation、amplification 和 non-normal singular-value 反例；右栏把 $\prod(I+A_\ell)$ 展开成不同长度的有序算子路径。来源：依据 He et al. 2016 与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_residual_foundations_v2.py]] 确定性生成。

**怎样读图**：先沿蓝色 rail 找到精确的 $v$ 或 $g$，再把 branch 项作为同一 accumulator 的第二个向量相加；最后只用 singular values 判断最坏方向增益，不以 eigenvalue 代替。

**图没有证明什么**：图没有给出训练后每层 $A_\ell$ 的真实分布，也没有证明 path expansion 中各项统计独立或贡献相等。

## 十六、诊断协议

对一个已训练深网，至少记录：

1. 随机方向 $\|Jv\|/\|v\|$；
2. 随机余切 $\|J^\mathsf Tu\|/\|u\|$；
3. power iteration 的 $\sigma_{\max}$ 估计与残差；
4. inverse/shift 方法或 Lanczos 的小 singular-value 诊断；
5. per-block identity/branch VJP norm 与夹角；
6. layerwise product 的 log gain；
7. finite-difference step sweep；
8. train/eval、mask、dtype 与 batch state。

## 十七、最小验收

1. 从 differential 推出 $I+J_F$；
2. 写出 JVP、VJP 和参数 VJP；
3. 复算二维 VJP 例子；
4. 用 $J_F=-I$ 反驳“永不消失”；
5. 证明 $1-a$ 与 $1+a$ singular-value 界；
6. 解释非正规例子为何 eigenvalue 误导；
7. 写出三层有序 product 与全部 8 项；
8. 说明 nonlinear path interpretation 的边界；
9. 写出 projection + norm block Jacobian；
10. 完成 JVP/VJP 对偶检查。

> [!summary]
> residual block 的严格优势是 Jacobian 中出现显式 identity summand，而不是总 Jacobian 等于 identity。真实传播由 $I+J_F$ 的方向干涉、singular spectrum 与跨层有序乘积决定；只有继续控制 branch 尺度和结构，identity rail 才可能转化为深度稳定性。

- [[残差连接、深度与稳定性 MOC]]
- [[习题 - 残差块 Jacobian 与梯度直通]]
- [[解答 - 残差块 Jacobian 与梯度直通]]
