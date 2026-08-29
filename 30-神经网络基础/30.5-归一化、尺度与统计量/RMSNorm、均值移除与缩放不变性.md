---
type: derivation
status: draft
area: [neural-networks/normalization, rmsnorm, geometry]
aliases: [RMSNorm Geometry, Root Mean Square Normalization]
node_id: NN-37
prerequisites: ["[[LayerNorm 的逐样本几何与反向传播]]", "[[局部微分、Jacobian、JVP 与 VJP]]", "[[内积空间]]"]
related: ["[[InstanceNorm、GroupNorm 与 WeightNorm]]", "[[Pre-Norm、Post-Norm 与归一化放置]]", "[[小批量、混合精度、分布式与因果归一化边界]]"]
sources: ["[[S-2019-Zhang-Sennrich-RMSNorm]]", "[[S-2026-PyTorch-Normalization-Systems]]", "[[S-2016-Ba-Kiros-Hinton-LayerNorm]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]"]
exercises: ["[[习题 - RMSNorm、均值移除与缩放不变性]]"]
solutions: ["[[解答 - RMSNorm、均值移除与缩放不变性]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-rmsnorm-centering-invariance-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---

# RMSNorm、均值移除与缩放不变性

> [!abstract] 本章主问题
> RMSNorm 不是“近似 LayerNorm”或“少一次减法的同一算子”。它直接按原点半径归一化，删除正尺度方向，却保留共同平移与输入均值信息；因此 Jacobian 比 LayerNorm 少一个 centering projection。这个差异会改变自由度、梯度和、小宽度退化、epsilon 默认值与模型参数化。

## 课程位置与两遍学习路线

- **承接什么：** NN-36 已把 LayerNorm 写成“先减均值、再除 centered RMS”的逐 token 几何，并得到两项投影的 VJP；
- **本页解决什么：** 删除 centering 这一步，逐项检查前向保留了什么、反向少删了哪个方向，而不是把 RMSNorm 当成 LayerNorm 的性能缩写；
- **后续为何需要：** 现代 Transformer 常在 RMSNorm、LayerNorm 与 residual placement 之间选择，NN-38—40 必须以精确对象和 Jacobian 差异为基础。

**第一遍只比较一条向量。** 对 $(1,2,3)$ 分别计算 LN 与 RMSNorm：前者落到 $\boldsymbol1^\perp$，后者保留正均值；再比较两个输入梯度的和。

**第二遍再研究球面几何。** 推导 vector gain VJP、径向/切向 eigenvalues、$\varepsilon$ 对尺度不变性的破坏，以及 partial RMS 与 fused kernel 的统计—系统合同。

### 问题链

1. LayerNorm 的 mean subtraction 删除了哪个一维方向？
2. RMSNorm 不减均值时，输入的共同 offset 如何进入输出？
3. 两者都具有正尺度不变性时，为什么 Jacobian 的 null space 仍不同？
4. 为什么 RMSNorm 的输入梯度通常不满足坐标和为 0？
5. “少一次 reduction”何时真能转化为端到端速度收益？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal N_\square$ 第一行上得到 $\widehat x_{\mathrm{RMS}}=b(1,2,3)$、$b=\sqrt{3/14}$，并从 $g=(1,0,0)$ 算出 $dx=b(13/14,-1/7,-3/14)$，就已掌握本页主干。

## 符号与对象账本

| 对象 | 定义 | 几何身份 | 与 LayerNorm 的差别 |
|---|---|---|---|
| $q_0=D^{-1}\|\boldsymbol x\|_2^2$ | 关于原点的二阶矩 | squared radius / $D$ | 不是 centered variance |
| $r_0=\sqrt{q_0+\varepsilon}$ | RMS divisor | radial scale | 不依赖 sample mean 的显式 subtraction |
| $\widehat{\boldsymbol x}=\boldsymbol x/r_0$ | RMS-normalized core | 原点球面上的方向 | 不必位于 $\boldsymbol1^\perp$ |
| $\boldsymbol\gamma$ | 逐 feature gain | 输出坐标重缩放 | 标准 RMSNorm 通常无 additive bias |
| $\boldsymbol u=\boldsymbol\gamma\odot\boldsymbol g$ | 穿过 gain 的 VJP seed | 待删除径向分量的 covector | 不再先删除常数方向 |

### 贯穿算例 $\mathcal N_\square$：保留均值会留下可观测差异

继续使用

$$
X=
\begin{bmatrix}
1&2&3\\
2&4&6\\
3&6&9
\end{bmatrix},
\qquad
b=\sqrt{\frac3{14}},
\qquad
\varepsilon=0.
$$

三行都是 $(1,2,3)$ 的正倍数。它们的 RMS square moments 为

$$
\left(\frac{14}{3},\frac{56}{3},42\right),
$$

所以 RMSNorm 删除这三个正尺度，得到

$$
\widehat X_{\mathrm{RMS}}
=b
\begin{bmatrix}
1&2&3\\
1&2&3\\
1&2&3
\end{bmatrix}.
$$

NN-36 的 LayerNorm 对同一张量给出

$$
\widehat X_{\mathrm{LN}}
=a
\begin{bmatrix}
-1&0&1\\
-1&0&1\\
-1&0&1
\end{bmatrix},
\qquad a=\sqrt{\frac32}.
$$

两者都把三行的正尺度差异删除，但只有 LN 把每行共同 offset 删除。第一行 RMSNorm 输出的坐标和是 $6b\ne0$，LN 输出的坐标和严格为 0。

再令第一行的 gain 为 1、上游 seed 为 $\boldsymbol g=(1,0,0)$。此时

$$
\widehat{\boldsymbol x}=b(1,2,3),
\qquad
\overline{g\widehat x}=\frac b3,
\qquad
r_0=\frac1b.
$$

RMSNorm VJP 为

$$
\begin{aligned}
d\boldsymbol x
&=b\left[\boldsymbol g-\widehat{\boldsymbol x}\,\overline{g\widehat x}\right]\\
&=b\left(\frac{13}{14},-\frac17,-\frac3{14}\right).
\end{aligned}
$$

它满足径向验算

$$
\widehat{\boldsymbol x}^{\mathsf T}d\boldsymbol x=0,
$$

却有

$$
\boldsymbol1^{\mathsf T}d\boldsymbol x=\frac{4b}{7}\ne0.
$$

这正是“少一个 centering projection”在反向中的可测后果。

## 核心公式七问：RMSNorm VJP

$$
\boxed{
\nabla_{\boldsymbol x}L
=\frac1{r_0}\left[
\boldsymbol u-\widehat{\boldsymbol x}\,\overline{u\widehat x}
\right],
\qquad
\boldsymbol u=\boldsymbol\gamma\odot\boldsymbol g
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 把输出 seed 拉回原点半径归一化的输入，同时删除无效径向变化 |
| 对象 | 单个 token/normalized-shape group，不跨 batch 或 token |
| 来路 | 对 $x/r_0$ 微分；$dr_0$ 只产生沿 $\widehat x$ 的反馈项 |
| 步骤 | 穿过 gain→算 $\overline{u\widehat x}$→删径向分量→除以 $r_0$ |
| 读法 | 与 LN 相比没有 $-\overline u\boldsymbol1$，因此共同平移方向仍可传梯度 |
| 检查 | $\varepsilon=0$ 时 $\widehat x^{\mathsf T}dx=0$；但 $\boldsymbol1^{\mathsf T}dx$ 一般不为 0 |
| 去路 | LLM normalization choice、Pre/Post-Norm Jacobian、partial RMS 与 fused kernels |

### AI / 系统对应

RMSNorm 常用于 decoder-only Transformer，但“LLM 常用”不是理论证明。选择时应分别记录：任务是否需要保留 feature mean、residual stream 的尺度参数化、$\varepsilon$ 与 accumulation dtype、是否有 bias、kernel 是否真的减少 memory traffic，以及替换 LN 后 initialization/learning-rate 是否仍可比。

## 一、学习目标

读完本节，你应能：

1. 对 $(B,T,D)$ 写出 RMSNorm$(D)$ 的统计组、参数 shape 与状态；
2. 从定义推导输出平方均值与正尺度不变性；
3. 精确比较 RMSNorm 与 LayerNorm 删除的方向；
4. 推导 vector gain 下的 VJP 与参数梯度；
5. 写出 Jacobian 的径向、切向 eigenvalues；
6. 解释 $D=1$、常量向量和共同 shift 的边界；
7. 区分完整 RMS 与 partial RMS 的估计对象；
8. 审计 epsilon、bias、accumulation dtype 与 fused-kernel 性能。

## 二、最小问题：均值到底是不是“无关信息”

考虑两个二维向量

$$
\boldsymbol x=(1,2),
\qquad
\boldsymbol x'=\boldsymbol x+10\boldsymbol1=(11,12).
$$

LayerNorm 在 $\varepsilon=0$ 时会把共同平移完全删除，所以二者 normalized core 相同。RMSNorm 的 denominator 分别是

$$
\sqrt{\frac{1^2+2^2}{2}}=\sqrt{\frac52},
$$

$$
\sqrt{\frac{11^2+12^2}{2}}=\sqrt{\frac{265}{2}},
$$

方向也不同。因此共同 offset 会改变 RMSNorm 输出。

这不是缺陷或优点的先验判断，而是建模选择：模型是否应该把沿 $\boldsymbol1$ 的分量视为可删除 nuisance？

## 三、正式定义与张量合同

对一个统计组

$$
\boldsymbol x=(x_1,\ldots,x_D)^{\mathsf T}\in\mathbb R^D,
$$

定义 quadratic mean

$$
q=\frac1D\sum_{j=1}^D x_j^2
=\frac1D\|\boldsymbol x\|_2^2,
$$

$$
r=\sqrt{q+\varepsilon},
\qquad
\widehat{\boldsymbol x}=\frac{\boldsymbol x}{r}.
$$

标准 RMSNorm 写为

$$
\boxed{
\boldsymbol y
=\boldsymbol\gamma\odot\widehat{\boldsymbol x}
}.
$$

原始定义与访问日 PyTorch 2.13 RMSNorm 都只有 gain，没有 additive bias。若某实现使用

$$
\boldsymbol y=\boldsymbol\gamma\odot\widehat{\boldsymbol x}+\boldsymbol\beta,
$$

那是扩展合同，必须显式记录，不能仍假设“RMSNorm 默认无 bias”。

对

$$
X\in\mathbb R^{B\times T\times D}
$$

和 RMSNorm$(D)$：

- 固定 $(b,t)$，归约最后的 $D$ 维；
- 统计组数是 $BT$，每组大小 $D$；
- $q,r$ 的 keepdim shape 是 $(B,T,1)$；
- $\gamma$ shape 是 $(D)$，参数量 $D$；
- 输出 shape 仍是 $(B,T,D)$；
- 不维护 running statistics，train/eval 使用同一统计规则。

## 四、前向手算

取

$$
\boldsymbol x=(1,2,2),
\qquad
\boldsymbol\gamma=(1,2,1),
\qquad
\varepsilon=0.
$$

则

$$
q=\frac{1+4+4}{3}=3,
\qquad
r=\sqrt3,
$$

$$
\widehat{\boldsymbol x}
=\frac1{\sqrt3}(1,2,2),
$$

$$
\boxed{
\boldsymbol y
=\frac1{\sqrt3}(1,4,2)
}.
$$

affine 前有

$$
\frac1D\sum_j\widehat x_j^2=1,
$$

但

$$
\frac1D\sum_j\widehat x_j
=\frac5{3\sqrt3}\ne0.
$$

RMSNorm 约束平方均值，不约束普通均值；逐坐标 gain 后连平方均值也不再固定为 1。

## 五、输出能量与 epsilon

一般地，

$$
\frac1D\|\widehat{\boldsymbol x}\|_2^2
=\frac q{q+\varepsilon}.
$$

所以：

- $\varepsilon=0,\boldsymbol x\ne0$ 时平方均值恰为 1；
- $q\ll\varepsilon$ 时输出能量约为 $q/\varepsilon$，趋近 0；
- $\boldsymbol x=0$ 时只要 $\varepsilon>0$，normalized output 为 0；
- 写成 $\sqrt q+\varepsilon$ 会得到不同的能量和导数，不能混用。

访问日 PyTorch 2.13 若 `eps=None`，使用 computation/opmath dtype 的 machine epsilon：fp16、bf16 与 fp32 输入对应 float32 epsilon，fp64 对应 float64 epsilon。它并不等于 LayerNorm 常见默认的 $10^{-5}$；公平比较应显式设成同一 epsilon。

## 六、不变性：保留什么，删除什么

令 $a\ne0$。对 $a\boldsymbol x$，

$$
\widehat{a\boldsymbol x}
=\frac{a\boldsymbol x}{\sqrt{a^2q+\varepsilon}}.
$$

于是：

- $a>0,\varepsilon=0$：输出精确不变；
- $a<0,\varepsilon=0$：normalized core 整体变号；
- $\varepsilon>0$：正尺度只近似抵消；
- 共同平移 $\boldsymbol x+b\boldsymbol1$ 一般不会被删除；
- 非均匀逐坐标缩放通常改变方向。

与 LayerNorm 对照：

| 变换 | LayerNorm core | RMSNorm core |
|---|---|---|
| $x\mapsto x+b\boldsymbol1$ | 精确不变 | 一般改变 |
| $x\mapsto ax,a>0,\varepsilon=0$ | 精确不变 | 精确不变 |
| $x\mapsto -x,\varepsilon=0$ | 变号 | 变号 |
| 常量向量 $c\boldsymbol1$ | 归零 | 归到 $\operatorname{sign}(c)\boldsymbol1$ |

因此“删除 centering”保留了原点相对方向中的共同分量，也把可保留自由度从 LayerNorm 的 $D-2$ 提升为 $D-1$。

## 七、几何：球面，而不是超平面与球面的交

当 $\varepsilon=0$ 且 $\boldsymbol x\ne0$，

$$
\|\widehat{\boldsymbol x}\|_2=\sqrt D.
$$

RMSNorm 把每条正射线映到半径 $\sqrt D$ 的球面一点。它不先投影到 $\boldsymbol1^\perp$，因此整个球面都是可能的 normalized core。

LayerNorm 则先做

$$
P=I-\frac1D\boldsymbol1\boldsymbol1^{\mathsf T}
$$

再归一，落在

$$
\boldsymbol1^\perp\cap\{z:\|z\|=\sqrt D\}.
$$

二者的流形维数分别是 $D-1$ 与 $D-2$。

## 八、完整微分推导

从

$$
q=\frac1D\boldsymbol x^{\mathsf T}\boldsymbol x
$$

开始：

$$
dq=\frac2D\boldsymbol x^{\mathsf T}d\boldsymbol x.
$$

又因为

$$
r=(q+\varepsilon)^{1/2},
$$

所以

$$
dr=\frac1{2r}dq
=\frac1{Dr}\boldsymbol x^{\mathsf T}d\boldsymbol x.
$$

对 $\widehat{\boldsymbol x}=\boldsymbol x/r$：

$$
d\widehat{\boldsymbol x}
=\frac1r d\boldsymbol x
-\frac{\boldsymbol x}{r^2}dr.
$$

代入 $dr$，并用 $\widehat{\boldsymbol x}=\boldsymbol x/r$：

$$
d\widehat{\boldsymbol x}
=\frac1r
\left(
I-\frac1D\widehat{\boldsymbol x}\widehat{\boldsymbol x}^{\mathsf T}
\right)d\boldsymbol x.
$$

因此

$$
\boxed{
J_{\mathrm{RMS}}
=\frac1r
\left(
I-\frac1D\widehat{\boldsymbol x}\widehat{\boldsymbol x}^{\mathsf T}
\right)
}.
$$

与 LayerNorm

$$
J_{\mathrm{LN-core}}
=\frac1r
\left(
I-\frac1D\boldsymbol1\boldsymbol1^{\mathsf T}
-\frac1D\widehat{\boldsymbol x}\widehat{\boldsymbol x}^{\mathsf T}
\right)
$$

相比，正好少了共同均值投影项。

## 九、Vector gain 的 VJP

令上游

$$
\boldsymbol g=\nabla_{\boldsymbol y}L,
\qquad
\boldsymbol u=\boldsymbol\gamma\odot\boldsymbol g.
$$

由于 $J_{\mathrm{RMS}}$ 对称，

$$
\boxed{
\nabla_{\boldsymbol x}L
=\frac1r
\left[
\boldsymbol u
-\widehat{\boldsymbol x}
\overline{u\widehat x}
\right]
},
$$

其中

$$
\overline{u\widehat x}
=\frac1D\sum_{j=1}^D u_j\widehat x_j.
$$

参数梯度为

$$
\nabla_{\boldsymbol\gamma}L
=\boldsymbol g\odot\widehat{\boldsymbol x},
$$

并在所有 batch/token 组上求和。若扩展实现含 $\beta$，才有

$$
\nabla_{\boldsymbol\beta}L=\sum\boldsymbol g.
$$

LayerNorm VJP 还有 $-\overline u\boldsymbol1$；RMSNorm 没有，因此输入梯度一般不满足分量和为零。

## 十、反向手算

沿用

$$
\boldsymbol x=(1,2,2),
\quad
\boldsymbol\gamma=(1,2,1),
\quad
\boldsymbol g=(1,1,0),
\quad
\varepsilon=0.
$$

有

$$
\boldsymbol u=(1,2,0),
$$

$$
\overline{u\widehat x}
=\frac{1+4}{3\sqrt3}
=\frac5{3\sqrt3}.
$$

所以

$$
\nabla_{\boldsymbol x}L
=\frac1{\sqrt3}
\left[
(1,2,0)-\frac59(1,2,2)
\right],
$$

$$
\boxed{
\nabla_{\boldsymbol x}L
=\frac1{9\sqrt3}(4,8,-10)
}.
$$

检查径向正交：

$$
\boldsymbol x^{\mathsf T}\nabla_{\boldsymbol x}L
=\frac{4+16-20}{9\sqrt3}=0.
$$

但梯度和为

$$
\boldsymbol1^{\mathsf T}\nabla_{\boldsymbol x}L
=\frac2{9\sqrt3}\ne0,
$$

正是没有删除共同平移方向的证据。

## 十一、Jacobian 谱与 epsilon

令 $\boldsymbol v\perp\boldsymbol x$，则

$$
J_{\mathrm{RMS}}\boldsymbol v=\frac1r\boldsymbol v.
$$

切空间有 $D-1$ 个方向，eigenvalue 为 $1/r$。

对径向 $\widehat{\boldsymbol x}$：

$$
J_{\mathrm{RMS}}\widehat{\boldsymbol x}
=\frac{\varepsilon}{(q+\varepsilon)^{3/2}}
\widehat{\boldsymbol x}.
$$

所以：

- $\varepsilon=0$ 时径向是唯一零方向；
- $\varepsilon>0$ 时尺度不变性被软化；
- $q\ll\varepsilon$ 时所有方向导数约为 $1/\sqrt\varepsilon$；
- 非均匀 gain 使完整 Jacobian $\operatorname{Diag}(\gamma)J_{\mathrm{RMS}}$ 不再对称。

## 十二、低维与常量输入

### 12.1 $D=1$

$$
\widehat x=\frac{x}{\sqrt{x^2+\varepsilon}},
$$

$$
\frac{d\widehat x}{dx}
=\frac{\varepsilon}{(x^2+\varepsilon)^{3/2}}.
$$

$\varepsilon=0,x\ne0$ 时它是局部常量 $\operatorname{sign}(x)$，导数为 0；但它不像一维 LayerNorm 那样总输出 0。

### 12.2 常量向量

若 $\boldsymbol x=c\boldsymbol1,c\ne0,\varepsilon=0$，

$$
\widehat{\boldsymbol x}
=\operatorname{sign}(c)\boldsymbol1.
$$

RMSNorm 保留共同 level 的符号；LayerNorm 会把该输入全部中心化为 0。

### 12.3 零输入

$\varepsilon=0$ 时 $\boldsymbol x=0$ 处未定义；$\varepsilon>0$ 时可定义，但 Jacobian 为

$$
J(0)=\frac1{\sqrt\varepsilon}I.
$$

epsilon 同时是定义域修补和局部 gain 上限的一部分。

## 十三、Partial RMSNorm：省了什么，估计了什么

取坐标子集 $S\subset\{1,\ldots,D\}$，$|S|=k$：

$$
q_S=\frac1k\sum_{j\in S}x_j^2,
\qquad
r_S=\sqrt{q_S+\varepsilon}.
$$

若 $S$ 从坐标中均匀无放回抽取，则对固定 $x$，

$$
\mathbb E_S[q_S]=q.
$$

但一般

$$
\mathbb E_S\left[\frac1{\sqrt{q_S+\varepsilon}}\right]
\ne
\frac1{\sqrt{q+\varepsilon}},
$$

因为 inverse square root 是非线性的。完整输出可能有偏并带共享随机尺度噪声。

若固定使用前 $k$ 个坐标，则它不是对全坐标 RMS 的无偏随机估计；它引入了位置/通道偏置。即使 $\varepsilon=0$ 时正尺度不变性仍成立，旋转或置换不变性也可能因 subset 规则破坏。

## 十四、可靠计算

直接先算 $x_j^2$ 可能溢出。float16 最大有限值约为 $65504$，所以 $|x_j|\gtrsim256$ 时平方已经可能 overflow，即使最终 RMS 本应可表示。

一种缩放算法是取

$$
a=\max_j|x_j|.
$$

若 $a>0$，则

$$
r
=a\sqrt{
\frac1D\sum_j\left(\frac{x_j}{a}\right)^2
+\frac{\varepsilon}{a^2}
}.
$$

这避免中间平方超出动态范围。工程实现还应记录：

- input/storage dtype；
- square/product dtype；
- accumulation dtype；
- reciprocal-square-root dtype；
- output cast；
- backward reduction dtype。

“使用混合精度”不是完整说明。访问日 PyTorch autocast 对不同 norm/op 有版本化策略，自定义 fused RMSNorm 必须单独核查。

## 十五、性能边界

RMSNorm 从算法图上删除 mean reduction 与 centering，但端到端速度不只由标量操作数决定：

- 归一化 kernel 常受 memory bandwidth 与 launch overhead 限制；
- fused residual/dropout/norm 可改变读写次数；
- 很小 $D$ 时 launch 占主导；
- tensor parallel 让 normalized axis 跨设备时需要 collective；
- 不同 epsilon/default dtype 会使“同精度比较”失真。

因此应同时报告 kernel latency、memory traffic、shape、dtype、fusion 与模型收敛步数，不能只引用原论文旧硬件百分比。

## 十六、图：少一个投影意味着什么

先看图回答：LayerNorm 与 RMSNorm 为什么都删除径向尺度，却只有前者删除共同平移？这如何反映到 VJP 与保留自由度？

![[00-知识库管理/_assets/figures/neural-networks/fig-rmsnorm-centering-invariance-v2.svg|900]]

> [!figure] 图 30.5-05　LayerNorm 与 RMSNorm 的投影、球面和 VJP 对照
> 左栏从同一输入分出“先中心化再归一”和“直接按原点半径归一”两条路径；中栏显示 LayerNorm 落在 $\boldsymbol1^\perp$ 与球面的交，而 RMSNorm 使用整个球面；右栏把 VJP 中是否含 $-\overline u\boldsymbol1$、梯度和与径向正交列成可检查差异。来源：依据 Zhang–Sennrich 2019、Ba–Kiros–Hinton 2016 与本节 differential 独立绘制；由 [[00-知识库管理/_labs/code/plot_normalization_advanced_v2.py]] 确定性生成。

**怎样读图**：先数两条路径删除了几个方向，再比较同一 upstream $u$ 在两个 VJP 中经过哪些投影，最后用“梯度和是否为 0”作为可执行判别。

**图没有证明什么**：图没有证明保留均值一定提高表达力，也没有证明 RMSNorm 在所有 LLM 上更快或更准；任务效果与系统性能需要受控实验。

## 十七、AI 调用与研究判断

在常见 Transformer 中，RMSNorm$(D)$ 对每个 token 的 residual feature vector 操作。它：

- 不跨 token，因此归一化本身不引入未来 token 统计；
- 不跨 batch，因此不受 batch size 统计估计影响；
- 保留共同 feature level，模型可利用该方向；
- 用 gain 恢复逐 feature 可学习尺度；
- 与 Pre/Post placement 组合后，深层 Jacobian 由 residual 路径共同决定。

选择 RMSNorm 前应回答：

1. 模型是否需要共同 shift 不变性？
2. epsilon 是否显式匹配比较基线？
3. normalized axis 是否跨 tensor-parallel shard？
4. fused kernel 的 accumulator 是什么 dtype？
5. 是否比较相同训练预算与调参预算？

## 十八、最小验收

1. 手算 $D=3$ forward 与 vector-gain backward；
2. finite difference 验证 VJP；
3. $\varepsilon=0$ 检查 $x^{\mathsf T}dx=0$；
4. 验证 $\sum dx$ 一般不为 0；
5. 比较共同 shift 前后输出；
6. 检查 $D=1$、零向量与常量向量；
7. 显式设置相同 epsilon 比较 LN/RMSNorm；
8. 对 partial subset 比较 $q_S$ 与完整 $q$；
9. 用大 offset/大 magnitude 检查 square overflow；
10. 记录 kernel shape、dtype、fusion 与 wall time。

> [!summary]
> RMSNorm 是“绕原点的方向归一 + per-feature gain”。它在 $\varepsilon=0$ 删除一个径向自由度，保留 LayerNorm 删除的共同平移方向；VJP 因而没有 mean-removal 项。是否值得删除 centering，是建模、数值与系统三层共同问题。

- [[归一化、尺度与统计量 MOC]]
- [[习题 - RMSNorm、均值移除与缩放不变性]]
- [[解答 - RMSNorm、均值移除与缩放不变性]]
