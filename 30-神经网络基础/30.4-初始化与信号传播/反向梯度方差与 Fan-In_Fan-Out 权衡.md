---
type: derivation
status: draft
area: [neural-networks/initialization, backpropagation, gradient-propagation]
aliases: [Backward Variance Propagation, Fan-In Fan-Out Tradeoff]
node_id: NN-28
prerequisites: ["[[方差传播与宽层均值场近似]]", "[[线性层与仿射层的反向传播]]", "[[Xavier、Glorot 初始化]]", "[[Kaiming、He 初始化]]"]
related: ["[[相关传播、Edge of Chaos 与临界初始化]]", "[[正交初始化与 Dynamical Isometry]]", "[[残差块 Jacobian 与梯度直通]]"]
sources: ["[[S-2010-Glorot-Bengio-Training-Difficulty]]", "[[S-2015-He-Delving-Rectifiers]]", "[[S-2017-Schoenholz-Deep-Information-Propagation]]", "[[S-2026-PyTorch-NN-Init]]", "[[S-2021-Su-8725-非方阵初始化]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]"]
exercises: ["[[习题 - 反向梯度方差与 Fan-In_Fan-Out 权衡]]"]
solutions: ["[[解答 - 反向梯度方差与 Fan-In_Fan-Out 权衡]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-forward-backward-fan-tradeoff-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---
# 反向梯度方差与 Fan-In/Fan-Out 权衡

> [!abstract] 本章主问题
> 前向一坐标汇总 fan-in 个输入，反向一坐标却汇总 fan-out 个输出 cotangents。再乘 activation derivative 后，两条二阶递推一般需要不同的权重 variance。初始化要先声明守护前向、反向还是某种折中；标量 gradient variance 稳定仍不等于 Jacobian 各方向稳定。

## 课程位置与两遍学习路线

- **承接什么：** NN-25 给出 forward moment operator，NN-26/27 分别给出近线性与 rectifier 的候选 weight scale；
- **本页解决什么：** 把 $W$ 与 $W^T$ 的求和方向并排，显式推出 $\chi_f,\chi_b$ 以及宽度变化下的不可兼得；
- **后续为何需要：** NN-29 会从单输入二阶矩走向两输入 correlation，NN-30 则从方向平均走向全 Jacobian singular spectrum。

**第一遍只画两支箭头。** Forward 从 $n_{\mathrm{in}}$ 个坐标汇总到一个输出；reverse 从 $n_{\mathrm{out}}$ 个 cotangents 汇总回一个输入。分别乘 $c$ 和 $d$，不要先背 mode 名字。

**第二遍再追踪深度与边界。** 将单层乘数连乘，然后逐一拆除 gradient independence、plain chain、loss reduction 和 scalar-moment 假设，看它们在 residual/norm/optimizer 系统中如何改写。

### 问题链

1. forward 与 reverse 中每个坐标各累加多少个独立项？
2. activation output factor $c$ 和 derivative factor $d$ 为什么是两个对象？
3. 对 $4\to8$ ReLU 层，fan-in He 为什么会使 backward second moment 翻倍？
4. Glorot-style rectifier 折中为什么仍会沿深度产生指数累积？
5. $\mathbb E\|Jv\|^2$ 守恒为什么不足以推出 $\sigma_{\min}(J)$ 与 $\sigma_{\max}(J)$ 都接近 1？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal I_\square$ 上分别算出 fan-in He 的 $(\chi_f,\chi_b)=(1,2)$、fan-out He 的 $(1/2,1)$ 与 fan-average rectifier 折中的 $(2/3,4/3)$，就已掌握本页的方向账本。

## 符号与对象账本

| 对象 | 定义 | AI 计算中的身份 | 不包含什么 |
|---|---|---|---|
| $c=\mathbb E[\phi(Z)^2]/\mathbb E[Z^2]$ | forward activation factor | activation 前后平均平方比 | correlation 与非高斯效应 |
| $d=\mathbb E[\phi'(Z)^2]$ | backward mask/gain factor | VJP 局部平方增益 | $\phi'(\mathbb E Z)^2$ |
| $\chi_f=n_{\mathrm{in}}vc$ | forward multiplier | 单层 activation scale 诊断 | 整个向量总 norm 比 |
| $\chi_b=n_{\mathrm{out}}vd$ | backward multiplier | 单层 cotangent scale 诊断 | optimizer update scale |
| $J=D_LW_L\cdots D_1W_1$ | 端到端 Jacobian | 真正的方向性传播对象 | 不由一个 $\chi$ 完整描述 |

### 贯穿算例 $\mathcal I_\square$：三种 mode 的得与失

对 $4\to8$ ReLU 层，$c=d=1/2$。三个候选 weight variances 为

$$
v_{\mathrm{in}}=\frac12,qquad
v_{\mathrm{out}}=\frac14,qquad
v_{\mathrm{avg}}=\frac{2}{4c+8d}=\frac13.
$$

代入两条乘数：

| mode | $v$ | $\chi_f=4v/2$ | $\chi_b=8v/2$ | 真正优先项 |
|---|---:|---:|---:|---|
| fan-in He | $1/2$ | $1$ | $2$ | forward |
| fan-out He | $1/4$ | $1/2$ | $1$ | backward |
| fan-average rectifier | $1/3$ | $2/3$ | $4/3$ | 算术-fan 对称折中 |

若一个教学型网络连续 6 次将宽度加倍，且每层都使用第三行，则标量近似给出

$$
\prod_{\ell=1}^6\chi_f^{(\ell)}
=\left(\frac23\right)^6
=\frac{64}{729}
\approx0.087791,
$$

$$
\prod_{\ell=1}^6\chi_b^{(\ell)}
=\left(\frac43\right)^6
=\frac{4096}{729}
\approx5.618656.
$$

“每层只是 $2/3$ 和 $4/3$”在深度乘积中并不小。这个算例是尺度假说，不是对真实有限网络的精确预测：宽度、mask、权重与 gradient 相关性都会产生偏离。

## 核心公式七问：$\chi_f=n_{\mathrm{in}}vc,\qquad\chi_b=n_{\mathrm{out}}vd$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 用两个标量显式区分前向与反向的单层平均平方增益 |
| 对象 | 坐标级 second moment，不是总 norm、极端方向或 parameter gradient |
| 来路 | $W$ 行求和的 fan-in、$W^T$ 行求和的 fan-out 与 activation 局部因子 |
| 步骤 | 确认 shape→求 $c,d$→选 $v$→计算两个 $\chi$→沿深度连乘 |
| 读法 | 小于 1 表示对应统计收缩，大于 1 表示放大；等于 1 仅是标量临界 |
| 检查 | linear 取 $c=d=1$，ReLU 对称输入取 $c=d=1/2$；方阵对应 scale 应使两者同时为 1 |
| 去路 | correlation fixed point、edge of chaos、正交初始化、dynamical isometry 与 residual Jacobian |

### AI / 系统对应

MLP expansion ratio、bottleneck projection、MoE expert width 和 attention output projection 都会让 fan-in/fan-out 不对称。运行时观测到的 gradient 还混入 token/batch reduction、loss scaling、all-reduce、clipping 与 optimizer preconditioning；因此诊断应同时保留网络 Jacobian ledger 与优化器 ledger，不能只看一个 global gradient norm。

## 一、从一层反向公式开始

一层写成

$$
z^{(\ell)}=W^{(\ell)}h^{(\ell-1)}+b^{(\ell)},
\qquad
h^{(\ell)}=\phi(z^{(\ell)}),
$$

其中

$$
W^{(\ell)}
\in\mathbb R^{n_\ell\times n_{\ell-1}}.
$$

定义 preactivation cotangent

$$
\delta^{(\ell)}
=\frac{\partial L}{\partial z^{(\ell)}}.
$$

则

$$
\frac{\partial L}{\partial h^{(\ell-1)}}
=(W^{(\ell)})^T\delta^{(\ell)},
$$

$$
\delta^{(\ell-1)}
=\phi'(z^{(\ell-1)})
\odot (W^{(\ell)})^T\delta^{(\ell)}.
$$

反向的一项也许看似与前向相同，但求和长度已经从 $n_{\ell-1}$ 变成 $n_\ell$。

## 二、反向二阶矩逐项推导

令单权重 variance 为 $v_\ell$，并作教学级近似：

- 权重零均值且坐标独立；
- 当前 $\delta_j^{(\ell)}$ 同尺度、交叉 covariance 可忽略；
- 权重与 cotangent/derivative 的依赖暂时忽略。

对

$$
u_i^{(\ell-1)}
=\sum_{j=1}^{n_\ell}W_{ji}^{(\ell)}\delta_j^{(\ell)}
$$

有

$$
\mathbb E[(u_i^{(\ell-1)})^2]
\approx
n_\ell v_\ell\,
\mathbb E[(\delta_j^{(\ell)})^2].
$$

再乘本层 activation derivative：

$$
\boxed{
\mathbb E[(\delta_i^{(\ell-1)})^2]
\approx
n_\ell v_\ell\,
d_{\ell-1}\,
\mathbb E[(\delta_j^{(\ell)})^2],
}
$$

其中

$$
d_{\ell-1}
=\mathbb E[\phi'(z^{(\ell-1)})^2].
$$

## 三、与前向递推并排

把前向 activation factor 记为

$$
c_{\ell-1}
=\frac{\mathbb E[\phi(z^{(\ell-1)})^2]}
{\mathbb E[(z^{(\ell-1)})^2]}.
$$

则忽略 bias 时，

$$
\chi_f^{(\ell)}
=n_{\ell-1}v_\ell c_{\ell-1},
$$

$$
\chi_b^{(\ell)}
=n_\ell v_\ell d_{\ell-1}.
$$

它们分别是一层 forward 与 backward second-moment multiplier。理想标量守恒要求

$$
\chi_f^{(\ell)}=1,
\qquad
\chi_b^{(\ell)}=1.
$$

要同时成立，必须满足

$$
n_{\ell-1}c_{\ell-1}
=n_\ell d_{\ell-1}.
$$

一般架构、activation 与工作区并不满足这个等式，所以一个 scalar variance 无法解决所有目标。

## 四、Linear、Tanh 与 ReLU

### Linear

$c=d=1$，前向要求 $v=1/n_{\mathrm{in}}$，反向要求 $v=1/n_{\mathrm{out}}$。方阵时一致。

### Tanh 的小信号区

若 $z$ 集中在 0 附近，$\phi(z)\approx z$、$\phi'(z)\approx1$，近似回到 linear；一旦进入饱和区，$c$ 与 $d$ 都随 $q$ 改变，且不是同一个常数合同。

### ReLU

对 centered symmetric continuous preactivation，

$$
c=d=\frac12.
$$

前向要求 $v=2/n_{\mathrm{in}}$，反向要求 $v=2/n_{\mathrm{out}}$。等宽层两者一致，宽度突变时冲突仍在。

## 五、深度把小偏差变成乘积

忽略跨层相关时，

$$
\mathbb E[(\delta^{(0)})^2]
\approx
\left(\prod_{\ell=1}^L\chi_b^{(\ell)}\right)
\mathbb E[(\delta^{(L)})^2].
$$

若每层 $\chi_b=0.95$，100 层后乘数约为

$$
0.95^{100}\approx5.9\times10^{-3}.
$$

若每层 $\chi_b=1.05$，则约为

$$
1.05^{100}\approx131.5.
$$

因此单层 5% 的偏差不能被“差不多是 1”轻易忽略。

## 六、为什么独立梯度近似很危险

$\delta^{(\ell)}$ 是由同一组权重参与的 forward activations 和后续网络共同生成的，所以它一般不与 $W^{(\ell)}$ 独立。严格 mean-field 分析需要更谨慎的极限、conditioning 或修正技巧。教学递推的用途是暴露尺度因子和实验假说，不是对有限训练网络的精确概率恒等式。

## 七、Gradient Variance 不等于 Jacobian Spectrum

总 Jacobian 为

$$
J=D_LW_L\cdots D_1W_1.
$$

平均平方梯度近似只看某种方向平均，例如 Frobenius-energy scale；训练还可能沿某些方向极度收缩、另一些方向放大。即便

$$
\frac1n\mathbb E\|Jv\|^2\approx\frac1n\|v\|^2,
$$

也不推出每个 singular value 都接近 1。[[正交初始化与 Dynamical Isometry]] 将处理这层更强要求。

## 八、Loss Reduction 与 Optimizer Scale

观测到的 parameter gradient 还受以下因素缩放：

- batch loss 是 sum 还是 mean；
- sequence/token mask 的有效元素数；
- mixed-precision loss scaling；
- gradient accumulation 与 distributed all-reduce；
- optimizer preconditioner、clipping 与 weight decay。

初始化理论里的 $\delta$ 递推只描述网络 Jacobian 的一部分。若实验忘记 reduction，宽度效应可能被 batch/token 因子伪装。

## 九、Residual 与 Normalization 改写递推

Residual block

$$
h_{\ell+1}=h_\ell+F_\ell(h_\ell)
$$

的 Jacobian 是 $I+J_F$，梯度包含 identity path 和 covariance/cross terms；LayerNorm/BatchNorm 的 derivative 还耦合同一 normalized group 的坐标。plain-chain fan 公式不能不加修改地覆盖它们。

## 十、如何选择 Fan Mode

一个可审计顺序是：

1. 写出真实 forward 和 VJP shape；
2. 决定首要守护 forward activation、backward cotangent 或二者折中；
3. 计算 activation 的 $c(q)$ 与 $d(q)$；
4. 对 width changes、residual/norm 单独改写；
5. 在目标深度、dtype 与 loss reduction 下实测。

框架的 fan-in/fan-out mode 是明确的目标选择，不是风格偏好。

## 十一、图：两条相反方向的尺度账本

先看图回答：为什么同一个扩宽层会让 Xavier 的 forward 收缩、backward 放大？

![[00-知识库管理/_assets/figures/neural-networks/fig-forward-backward-fan-tradeoff-v2.svg|900]]

> [!figure] 图 30.4-04　Forward/Backward fan tradeoff、深度乘积与证据边界
> 左栏并排画 $W$ 与 $W^T$ 的求和方向；中栏用 aspect ratio 显示 $\chi_f,\chi_b$ 的对向变化和深度乘积；右栏给出从 scalar moment 到 Jacobian spectrum、residual/norm 与系统 reduction 的检查阶梯。来源：依据 Glorot–Bengio 2010、He et al. 2015、Schoenholz et al. 2017、PyTorch 官方文档与科学空间 8725/8620 独立绘制；由 [[00-知识库管理/_labs/code/plot_initialization_foundations_v2.py]] 确定性生成。

**怎样读图**：先按箭头数清每个坐标汇总的项数，再乘 activation/derivative factor，最后看这些乘数如何沿深度相乘。

**图没有证明什么**：图没有证明 gradient independence，没有证明 scalar variance 守恒足够训练，也没有把 plain feedforward 递推外推到 residual、normalization、attention 或 optimizer dynamics。

## 十二、实验矩阵

建立 width profile（等宽、逐层扩宽、逐层压窄、bottleneck）× initialization mode（fan-in、fan-out、Xavier）× activation 的实验矩阵。每层记录：

$$
\mathbb E[z^2],\quad
\mathbb E[h^2],\quad
\mathbb E[\delta_z^2],\quad
\mathbb E[\delta_h^2],
$$

以及 Jacobian top/bottom singular-value estimate、gradient norm、NaN/Inf 与 wall-clock。用多 seed 区分初始化 ensemble variance，固定 loss reduction 并注明 normalization/residual。

> [!summary]
> fan-in 与 fan-out 来自同一矩阵在 forward 和 reverse 中不同的求和长度。初始化只能在明确的 activation、宽度、架构和统计目标下校准；标量二阶矩是起点，不是可训练性的最终证书。

- [[习题 - 反向梯度方差与 Fan-In_Fan-Out 权衡]]
- [[解答 - 反向梯度方差与 Fan-In_Fan-Out 权衡]]
