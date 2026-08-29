---
type: derivation
status: draft
area: [neural-networks/normalization, batch-normalization, backpropagation]
aliases: [BatchNorm Backward, BatchNorm Scale Invariance]
node_id: NN-35
prerequisites: ["[[BatchNorm 前向统计与训练—推理差异]]", "[[局部微分、Jacobian、JVP 与 VJP]]", "[[正交投影]]"]
related: ["[[LayerNorm 的逐样本几何与反向传播]]", "[[Hessian、二阶微分与曲率|损失地形、曲率与重参数化边界]]", "[[小批量、混合精度、分布式与因果归一化边界]]"]
sources: ["[[S-2015-Ioffe-Szegedy-BatchNorm]]", "[[S-2018-Santurkar-BatchNorm-Optimization]]", "[[S-2026-PyTorch-Normalization-Semantics]]"]
exercises: ["[[习题 - BatchNorm 反向传播、尺度不变性与噪声]]"]
solutions: ["[[解答 - BatchNorm 反向传播、尺度不变性与噪声]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-batchnorm-backward-coupling-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---

# BatchNorm 反向传播、尺度不变性与噪声

> [!abstract] 本章主问题
> 训练态 BatchNorm 的每个输入既影响自己的标准化值，也影响全组 mean 与 variance，因此反向梯度不是逐元素乘一个 scale，而是“先乘 gain，再删除组均值方向，再删除标准化径向分量”。这产生 dense batch coupling、近似尺度不变性、方向—长度解耦和由 batch composition 驱动的相关噪声；eval 态固定 statistics 后，这些耦合全部消失。

## 课程位置与两遍学习路线

- **承接什么：** NN-34 已把 BatchNorm 拆成 current-statistics training graph 与 frozen-statistics eval graph；
- **本页解决什么：** 沿 training graph 对 mean、variance、inverse standard deviation 逐层反传，说明为什么一个位置的上游梯度会传到同组全部样本；
- **后续为何需要：** LayerNorm、RMSNorm 与 GroupNorm 的 VJP 都复用这套“删均值方向、删径向分量”的投影结构，只是统计组不同。

**第一遍抓住闭式 VJP。** 先把 $u_i=\gamma g_i$ 写出来，再从每个 $u_i$ 中减掉组均值与沿 $\widehat x$ 的分量；最后除以 $r$。

**第二遍再研究几何后果。** 用 Jacobian eigenspaces 理解尺度不变性、weight-gradient orthogonality、batch-composition noise，以及 $\varepsilon>0$ 对零方向的解除。

### 问题链

1. 为什么把 BN 当成固定 affine scale 会漏掉两条反向路径？
2. $\operatorname{mean}(u)$ 与 $\operatorname{mean}(u\widehat x)$ 分别删除什么方向？
3. 上游梯度只落在一个样本时，为什么其余样本仍能收到输入梯度？
4. $\sum_i dx_i=0$ 与 $\widehat x^{\mathsf T}dx=0$ 应怎样解释和验算？
5. 为什么 train-mode Jacobian dense，而 eval-mode Jacobian diagonal？

> [!check] 第一遍停靠线
> 若你能从 $\mathcal N_\square$ 第一列与上游 $g=(1,0,0)$ 算出 $dx=(a/6,-a/3,a/6)$，并解释后两个非零分量来自统计量路径，就已掌握本页主干。

## 符号与对象账本

| 对象 | 定义 | 形状/作用域 | 反向角色 |
|---|---|---|---|
| $\boldsymbol x$ | 一个 channel 的 training statistics group | $m$ 个 batch/spatial entries | 所有 entries 经统计量密集耦合 |
| $\boldsymbol g=\nabla_{\boldsymbol y}L$ | 输出端 VJP seed | 与 $\boldsymbol x$ 同形 | 来自后续网络 |
| $\boldsymbol u=\gamma\boldsymbol g$ | 穿过 affine gain 后的 seed | 同组向量 | 进入 normalization Jacobian |
| $\boldsymbol1$ | 常数/共同平移方向 | 组内一维子空间 | VJP 必须删除其分量 |
| $\widehat{\boldsymbol x}$ | centered radial direction | 与 $\boldsymbol1$ 正交 | $\varepsilon=0$ 时再删除其分量 |
| $r=\sqrt{q+\varepsilon}$ | 前向实际除数 | 正标量 | 缩放整个 VJP |

### 贯穿算例 $\mathcal N_\square$：一个上游坐标，三个输入都有梯度

取共享张量第一列构成的 BN 统计组

$$
\boldsymbol x=(1,2,3),
\qquad
\mu=2,
\qquad
q=\frac23,
\qquad
r=\sqrt{\frac23}=\frac1a,
$$

其中 $a=\sqrt{3/2}$，所以

$$
\widehat{\boldsymbol x}=(-a,0,a).
$$

暂取 $\gamma=1$，令损失只直接读取该 channel 第一个样本的 BN 输出，即

$$
\boldsymbol g=(1,0,0),
\qquad
\overline g=\frac13,
\qquad
\overline{g\widehat x}=-\frac a3.
$$

代入闭式 VJP：

$$
dx_i
=\frac1r
\left[g_i-\overline g-\widehat x_i\,\overline{g\widehat x}\right].
$$

逐项得到

$$
\begin{aligned}
dx_1&=a\left(1-\frac13-\frac12\right)=\frac a6,\\
dx_2&=a\left(0-\frac13-0\right)=-\frac a3,\\
dx_3&=a\left(0-\frac13+\frac12\right)=\frac a6.
\end{aligned}
$$

即

$$
\boxed{
\nabla_{\boldsymbol x}L
=\left(\frac a6,-\frac a3,\frac a6\right)
\approx(0.204,-0.408,0.204)
}.
$$

虽然 $g_2=g_3=0$，但 $x_2,x_3$ 会改变第一项所用的 mean 与 variance，所以其输入梯度不为零。两项验算为

$$
\boldsymbol1^{\mathsf T}d\boldsymbol x=0,
\qquad
\widehat{\boldsymbol x}^{\mathsf T}d\boldsymbol x=0.
$$

参数梯度也能直接读出：$d\beta=1$，$d\gamma=-a$。

## 核心公式七问：BatchNorm training VJP

$$
\boxed{
\frac{\partial L}{\partial x_i}
=\frac1r\left[
u_i-\overline u-\widehat x_i\,\overline{u\widehat x}
\right],
\qquad u_i=\gamma g_i
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 把输出端 seed 精确拉回共享统计量的所有输入 |
| 对象 | 一个 training statistics group，而不是彼此独立的 scalar activations |
| 来路 | affine、除法、variance、centering 与 mean 五条 differential 合并 |
| 步骤 | 算 $u$→算 $\overline u$→算 $\overline{u\widehat x}$→删两分量→除以 $r$ |
| 读法 | 第一项是直接路径，第二项来自 mean，第三项来自 variance/radial normalization |
| 检查 | 总和应为 0；$\varepsilon=0$ 时还应与 $\widehat x$ 正交；gradcheck 应通过 |
| 去路 | LN/RMSNorm VJP、scale-invariant parameterization、batch noise 与 distributed BN |

### AI / 系统对应

在 data-parallel BN 中，是否跨设备同步 statistics 不只改变前向数值，也改变 backward coupling graph：local BN 只在单卡 group 内传梯度，SyncBN 则跨卡归约。gradient accumulation 不会自动补上这种耦合。调试时应同时记录 group size、companion samples、mode 与通信边界；只比较最终 loss 无法定位差异来源。

## 一、学习目标

学完本节，你应能：

1. 从 differential 逐步推导 BatchNorm 的 $d\beta,d\gamma,dX$；
2. 把闭式反向写成 VJP 与 Jacobian 矩阵；
3. 证明输入梯度和为零，并解释 $\varepsilon=0$ 时第二个径向零方向；
4. 手算一个上游只作用于单样本、但梯度传播到全 batch 的例子；
5. 区分 train-mode dense coupling 与 eval-mode diagonal scaling；
6. 推导正尺度不变性、$w^{\mathsf T}\nabla_wL=0$ 与 gradient 的逆尺度变化；
7. 解释 batch-statistic noise 为什么不是独立加性噪声或 Dropout；
8. 设计 gradcheck、companion sensitivity 与尺度扫描验收。

## 二、单个统计组的符号

只看一个 channel 的一个归约组：

$$
\boldsymbol x=(x_1,\ldots,x_m)^{\mathsf T}\in\mathbb R^m.
$$

定义

$$
\mu=\frac1m\boldsymbol1^{\mathsf T}\boldsymbol x,
\qquad
\boldsymbol c=\boldsymbol x-\mu\boldsymbol1,
$$

$$
q=\frac1m\boldsymbol c^{\mathsf T}\boldsymbol c,
\qquad
r=\sqrt{q+\varepsilon},
\qquad
\widehat{\boldsymbol x}=\frac{\boldsymbol c}{r},
$$

$$
\boldsymbol y=\gamma\widehat{\boldsymbol x}+\beta\boldsymbol1.
$$

令上游 VJP seed 为

$$
\boldsymbol g=\nabla_{\boldsymbol y}L.
$$

本节先假设同一组共享标量 $\gamma,\beta$，正对应 BatchNorm 的一个 channel；多 channel 逐组独立应用。

## 三、先求 affine 参数梯度

由

$$
dy_i=\widehat x_i\,d\gamma+d\beta+\gamma\,d\widehat x_i
$$

可直接收集

$$
\boxed{
\frac{\partial L}{\partial\beta}
=\sum_{i=1}^m g_i
},
$$

$$
\boxed{
\frac{\partial L}{\partial\gamma}
=\sum_{i=1}^m g_i\widehat x_i
}.
$$

这两项分别测量上游梯度在常数方向与 normalized feature 方向上的投影。卷积 BN 还要对 $N,H,W$ 联合求和。

## 四、从 differential 推导输入梯度

### 4.1 mean 的 differential

$$
d\mu=\frac1m\boldsymbol1^{\mathsf T}d\boldsymbol x.
$$

所以

$$
d\boldsymbol c
=d\boldsymbol x-d\mu\,\boldsymbol1
=\left(I-\frac1m\boldsymbol1\boldsymbol1^{\mathsf T}\right)d\boldsymbol x.
$$

记 centering projection

$$
P=I-\frac1m\boldsymbol1\boldsymbol1^{\mathsf T}.
$$

### 4.2 variance 的 differential

从

$$
q=\frac1m\boldsymbol c^{\mathsf T}\boldsymbol c
$$

得到

$$
dq=\frac2m\boldsymbol c^{\mathsf T}d\boldsymbol c.
$$

又因 $\boldsymbol c^{\mathsf T}\boldsymbol1=0$，

$$
\boldsymbol c^{\mathsf T}d\boldsymbol c
=\boldsymbol c^{\mathsf T}d\boldsymbol x.
$$

故

$$
\boxed{
dq=\frac2m\boldsymbol c^{\mathsf T}d\boldsymbol x
}.
$$

### 4.3 reciprocal scale 的 differential

由 $r=(q+\varepsilon)^{1/2}$，

$$
dr=\frac{1}{2r}\,dq
=\frac{1}{mr}\boldsymbol c^{\mathsf T}d\boldsymbol x.
$$

同时

$$
d(r^{-1})=-r^{-2}dr
=-\frac{1}{mr^3}\boldsymbol c^{\mathsf T}d\boldsymbol x.
$$

### 4.4 normalized vector 的 differential

使用乘积法则：

$$
d\widehat{\boldsymbol x}
=d(r^{-1}\boldsymbol c)
=r^{-1}d\boldsymbol c+\boldsymbol c\,d(r^{-1}).
$$

逐项代入：

$$
d\widehat{\boldsymbol x}
=\frac1rP\,d\boldsymbol x
-\frac1{mr^3}\boldsymbol c\boldsymbol c^{\mathsf T}d\boldsymbol x.
$$

因为 $\boldsymbol c=r\widehat{\boldsymbol x}$，

$$
\boxed{
d\widehat{\boldsymbol x}
=\frac1r
\left(
P-\frac1m\widehat{\boldsymbol x}\widehat{\boldsymbol x}^{\mathsf T}
\right)d\boldsymbol x
}.
$$

这已经给出 normalization Jacobian。

## 五、闭式 VJP

令

$$
\boldsymbol u=\gamma\boldsymbol g.
$$

由 Jacobian 对称，

$$
\nabla_{\boldsymbol x}L
=\frac1r
\left(
P-\frac1m\widehat{\boldsymbol x}\widehat{\boldsymbol x}^{\mathsf T}
\right)\boldsymbol u.
$$

展开 $P$，得到最适合实现的形式：

$$
\boxed{
\frac{\partial L}{\partial x_i}
=\frac{\gamma}{r}
\left[
g_i-\overline g
-\widehat x_i\,\overline{g\widehat x}
\right]
},
$$

其中

$$
\overline g=\frac1m\sum_jg_j,
\qquad
\overline{g\widehat x}=\frac1m\sum_jg_j\widehat x_j.
$$

读法是：

1. 从每个 $g_i$ 减去全组上游均值；
2. 再减去沿 $\widehat{\boldsymbol x}$ 的分量；
3. 最后乘 $\gamma/r$。

任何漏掉后两项之一的“逐元素 backward”都不是 train-mode BatchNorm。

## 六、Jacobian 元素与 dense batch coupling

逐元素写成

$$
\boxed{
\frac{\partial y_i}{\partial x_k}
=\frac{\gamma}{r}
\left[
\mathbf1[i=k]-\frac1m-\frac1m\widehat x_i\widehat x_k
\right]
}.
$$

当 $i\ne k$ 时通常仍非零。也就是说，样本 $k$ 通过 mean 与 variance 改变样本 $i$ 的输出；反向时，一个样本的 loss 也会给同组其他样本输入分配梯度。

这是一种计算图依赖，不是概率相关性的类比。

## 七、两个被删除的方向与 $\varepsilon$ 边界

### 7.1 共同平移方向

因为 $P\boldsymbol1=0$ 且

$$
\widehat{\boldsymbol x}^{\mathsf T}\boldsymbol1=0,
$$

所以

$$
J_{\widehat x}\boldsymbol1=0.
$$

等价地，

$$
\boxed{
\sum_i\frac{\partial L}{\partial x_i}=0
}.
$$

这对任意 $\varepsilon$ 都成立：共同平移不会改变输出。

### 7.2 centered radial direction

注意

$$
\frac1m\|\widehat{\boldsymbol x}\|^2
=\frac{q}{q+\varepsilon}.
$$

因此

$$
J_{\widehat x}\widehat{\boldsymbol x}
=\frac1r
\left(1-\frac{q}{q+\varepsilon}\right)
\widehat{\boldsymbol x}
=\frac{\varepsilon}{(q+\varepsilon)^{3/2}}
\widehat{\boldsymbol x}.
$$

- $\varepsilon=0,q>0$：radial direction 也是精确零方向；
- $\varepsilon>0$：它只被强烈抑制，不被完全删除；
- $q\ll\varepsilon$：normalization 近似线性 centering 后乘 $1/\sqrt\varepsilon$。

所以“BN Jacobian 总有两个零奇异值”只在非退化、$\varepsilon=0$ 的组内模型成立。

## 八、一个把梯度扩散到全 batch 的手算

取

$$
\boldsymbol x=(-1,0,1),\qquad
\gamma=1,\quad\beta=0,\quad\varepsilon=0.
$$

有

$$
\mu=0,\qquad q=\frac23,\qquad
r=\sqrt{\frac23},
$$

$$
\widehat{\boldsymbol x}
=\left(-\sqrt{\frac32},0,\sqrt{\frac32}\right).
$$

令上游只作用于第一个输出：

$$
\boldsymbol g=(1,0,0).
$$

计算

$$
\overline g=\frac13,
\qquad
\overline{g\widehat x}
=-\frac13\sqrt{\frac32}.
$$

代回闭式公式得到

$$
\nabla_{\boldsymbol x}L
=\left(
\frac1{2\sqrt6},
-\frac1{\sqrt6},
\frac1{2\sqrt6}
\right)
\approx(0.2041,-0.4082,0.2041).
$$

检查：

$$
\sum_i\frac{\partial L}{\partial x_i}=0,
$$

$$
\boldsymbol x^{\mathsf T}\nabla_{\boldsymbol x}L=0.
$$

尽管 $g_2=g_3=0$，$x_2,x_3$ 仍有非零梯度；它们参与了第一个输出使用的 mean/variance。

## 九、eval-mode 反向为什么完全不同

eval mode 中若 $\bar\mu,\bar q$ 被视为固定 buffers，

$$
y_i=\gamma\frac{x_i-\bar\mu}{\sqrt{\bar q+\varepsilon}}+\beta.
$$

于是

$$
\boxed{
\frac{\partial L}{\partial x_i}
=\frac{\gamma}{\sqrt{\bar q+\varepsilon}}g_i
}.
$$

Jacobian 是 diagonal，组内样本不再耦合。比较 backward 必须固定 mode；用 eval-mode gradcheck 不能验证 train-mode BN 的 coupling 公式。

## 十、正尺度不变性与权重梯度

设 BN 前的标量 feature 为

$$
\boldsymbol z=X\boldsymbol w,
$$

忽略 bias，且 $\varepsilon=0$。对任意 $a>0$，

$$
\operatorname{BN}(X(a\boldsymbol w))
=\operatorname{BN}(a\boldsymbol z)
=\operatorname{BN}(\boldsymbol z).
$$

因此 loss 作为权重函数满足

$$
L(a\boldsymbol w)=L(\boldsymbol w).
$$

对 $a$ 在 1 处求导：

$$
\boxed{
\boldsymbol w^{\mathsf T}\nabla_{\boldsymbol w}L=0
}.
$$

梯度在一阶上正交于径向，只改变方向。再对重参数化比较：

$$
\boxed{
\nabla_{a\boldsymbol w}L
=\frac1a\nabla_{\boldsymbol w}L
}.
$$

权重放大 $a$ 倍，raw gradient 缩小 $a$ 倍；相对于参数 norm 的角度步长还会再除一次 $a$，近似按 $1/a^2$ 变化。

## 十一、为何不能说“weight norm 完全无关”

精确尺度不变性会被以下因素破坏：

- $\varepsilon>0$；
- weight decay 或其他显式 regularizer；
- optimizer 的 momentum/adaptive state；
- finite step size 而非无穷小 gradient flow；
- mixed precision、clipping 与 quantization；
- BN 前后还有未归一化旁路；
- $a<0$ 会翻转 normalized sign。

即使函数值近似不依赖 norm，norm 仍控制有效方向学习率；weight decay 可能通过缩小 norm 间接增大角度步长。把它只解释成“正则化函数复杂度”会遗漏重参数化动力学。

## 十二、batch-statistic noise 不是独立噪声

对某个样本 $x_i$，训练输出是

$$
\widehat x_i
=\frac{x_i-\mu(\{x_j\}_{j=1}^m)}
{\sqrt{q(\{x_j\}_{j=1}^m)+\varepsilon}}.
$$

改变 companions 会同时改变 numerator 与 denominator。噪声具有：

1. **数据依赖**：与 batch 内容、类别、增强相关；
2. **跨样本相关**：同组共享同一 $\mu,q$；
3. **跨层传播**：前一层 batch coupling 改变后一层输入；
4. **非加性**：出现在 ratio 中；
5. **mode-specific**：常见 eval path 消失。

因此不能写成

$$
\widehat x_i=\text{deterministic signal}+\text{iid Gaussian noise}
$$

而不注明近似条件。BN 的 stochasticity 也不等于 Dropout 的 independent Bernoulli mask。

## 十三、有限样本误差的第一层近似

若 $X_1,\ldots,X_m$ IID，均值 $\mu_\star$、variance $\sigma^2$，则

$$
\operatorname{Var}(\mu_B)=\frac{\sigma^2}{m}.
$$

biased sample variance 满足

$$
\mathbb E[q_B]=\frac{m-1}{m}\sigma^2.
$$

这些公式解释小 $m$ 时统计噪声增大，但实际网络中：

- spatial values 往往相关；
- samples 可能按长度、类别或设备非随机分组；
- upstream activations 随参数改变；
- ratio 的 expectation 不等于 moments ratio。

所以 $1/m$ 规律只是 IID 基线，不是 BatchNorm 误差的完整定理。

## 十四、机制解释：精确公式能支持到哪里

闭式 Jacobian精确说明：

- gradient 被 center；
- $\varepsilon=0$ 时 radial component 被删除；
- 组内产生 dense coupling；
- scale 改变会改变 gradient magnitude；
- train/eval optimization geometry 不同。

Santurkar et al. 进一步报告 BN 下 loss/gradient 在测量方向更平滑、更可预测，并挑战“一阶二阶分布稳定就是主要原因”的充分性。

但这些证据不推出：

- 所有架构都获得相同 smoothness；
- smoothness 是唯一机制；
- BN 必然改善 generalization；
- 某个 batch size、learning rate 或 weight decay 普遍最优。

## 十五、图：反向投影、跨样本耦合与尺度方向

先看图回答：为什么一个局部上游梯度会扩散到整个 batch？哪两个几何方向被删除，权重放大后 raw gradient 与方向步长分别怎样变化？

![[00-知识库管理/_assets/figures/neural-networks/fig-batchnorm-backward-coupling-v2.svg|900]]

> [!figure] 图 30.5-03　BatchNorm 反向的两次投影、dense coupling 与尺度—方向解耦
> 左栏把 $g$ 依次变成 $u=\gamma g$、减去组均值、减去 normalized-radial 分量并乘 $1/r$；中栏用非对角 Jacobian 网格显示一个输出对全组输入的依赖，并对比 eval 的 diagonal map；右栏画出 scale-invariant weight ray、切向 gradient 与 $a$ 倍缩放后的 $1/a$ raw gradient、约 $1/a^2$ angular step。来源：依据标准化 differential 与 Santurkar et al. 2018 Appendix C 独立推导绘制；由 [[00-知识库管理/_labs/code/plot_normalization_foundations_v2.py]] 确定性生成。

**怎样读图**：先把左栏当作 VJP 算法逐项核对，再用中栏确认 train/eval 的依赖图不同；右栏只在正尺度、$\varepsilon=0$ 和无额外 regularizer 的局部模型下读取缩放律。

**图没有证明什么**：图没有证明 BN 在所有网络中提升优化或泛化，也没有把 batch noise 近似成独立 Gaussian；它表达的是单组精确 Jacobian 及其受限尺度几何。

## 十六、实现与数值验收

至少执行以下测试：

1. 用 float64 小张量做 central-difference gradcheck；
2. 分别检查 $d\beta,d\gamma,dX$；
3. 验证 $\sum_i dx_i\approx0$；
4. 在 $\varepsilon=0$ 的非退化组验证 $\boldsymbol c^{\mathsf T}d\boldsymbol x\approx0$；
5. 改变 companion batch，确认 train-mode 输出与梯度改变；
6. 切到 eval，确认 Jacobian 变为固定逐元素 scale；
7. 扫描 $\boldsymbol w\mapsto a\boldsymbol w$，记录 loss、gradient norm 与 angular update；
8. 对 $q\ll\varepsilon$、constant group、fp16/bf16 accumulation 单独记录误差；
9. 固定 loss reduction，避免 batch mean/sum 自身引入额外 $m$ 因子。

> [!summary]
> BatchNorm 训练反向是一个组内投影型 VJP：减去常数方向和近似径向分量，再按 $\gamma/\sqrt{q+\varepsilon}$ 缩放。它同时解释跨样本耦合、尺度不变性和 batch-dependent noise；eval 固定 statistics 后则退化为普通 diagonal affine backward。

- [[归一化、尺度与统计量 MOC]]
- [[习题 - BatchNorm 反向传播、尺度不变性与噪声]]
- [[解答 - BatchNorm 反向传播、尺度不变性与噪声]]
