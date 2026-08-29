---
type: derivation
status: draft
area: [neural-networks/initialization, xavier, glorot]
aliases: [Xavier Initialization, Glorot Initialization]
node_id: NN-26
prerequisites: ["[[方差传播与宽层均值场近似]]", "[[线性层、批量张量与参数计数]]"]
related: ["[[Kaiming、He 初始化]]", "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]", "[[正交初始化与 Dynamical Isometry]]"]
sources: ["[[S-2010-Glorot-Bengio-Training-Difficulty]]", "[[S-1998-LeCun-Efficient-Backprop]]", "[[S-2026-PyTorch-NN-Init]]", "[[S-2020-Su-7180-初始化几何]]", "[[S-2021-Su-8725-非方阵初始化]]"]
exercises: ["[[习题 - Xavier、Glorot 初始化]]"]
solutions: ["[[解答 - Xavier、Glorot 初始化]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-xavier-fan-compromise-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---
# Xavier、Glorot 初始化

> [!abstract] 本章主问题
> 对一个 $n_{\mathrm{in}}\to n_{\mathrm{out}}$ 的非方线性层，前向二阶矩希望单权重 variance 为 $1/n_{\mathrm{in}}$，反向梯度却希望它为 $1/n_{\mathrm{out}}$。Xavier/Glorot 用 $2/(n_{\mathrm{in}}+n_{\mathrm{out}})$ 做对称折中；它是带假设的尺度折中，不是让随机矩阵变成正交矩阵的定理。

## 课程位置与两遍学习路线

- **承接什么：** NN-25 已证明 forward 单坐标的二阶矩乘数是 $n_{\mathrm{in}}v$；现在将同一个矩阵转置放入 reverse；
- **本页解决什么：** 从 forward/backward 两个不同求和长度推出 fan-in、fan-out 与 Glorot 算术平均折中；
- **后续为何需要：** NN-27 会加入 ReLU 的 $1/2$ 因子，NN-28 则把两条乘数放到深度乘积中。

**第一遍只做三次代入。** 先算 $v_F=1/n_{\mathrm{in}}$，再算 $v_B=1/n_{\mathrm{out}}$，最后算 $v_X=2/(n_{\mathrm{in}}+n_{\mathrm{out}})$；每次都代回 $\chi_f=n_{\mathrm{in}}v$ 和 $\chi_b=n_{\mathrm{out}}v$。

**第二遍再看实现边界。** 比较 normal/uniform 同方差不同高阶矩，审计 tensor layout、convolution/group fan、activation gain 与“期望 Gram 是单位阵”的谱论越级。

### 问题链

1. $W$ 在 forward 中一行求和，在 reverse 中为什么变成一列求和？
2. 非方层中，为什么 $1/n_{\mathrm{in}}$ 与 $1/n_{\mathrm{out}}$ 不能同时成立？
3. Xavier 的“同时考虑前后向”究竟是精确守恒还是对称折中？
4. normal 的 standard deviation 与 uniform 的 bound 怎样由同一 variance 得到？
5. 为什么 $\mathbb E[WW^T]=I$ 不等于一次抽样的所有 singular values 为 1？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal I_\square$ 上算出 $v_X=1/6$、$\chi_f=2/3$、$\chi_b=4/3$，并解释它们为什么不是两个 1，就掌握了本页主干。

## 符号与对象账本

| 对象 | Shape/定义 | AI 实现角色 | 检查问题 |
|---|---|---|---|
| $W\in\mathbb R^{8\times4}$ | $z=Wh$ | Linear 权重的数学布局 | API 是否假设用 $xW^T$ |
| $v_F=1/4$ | fan-in target | 优先守 forward 坐标 | reverse 会放大多少 |
| $v_B=1/8$ | fan-out target | 优先守 backward 坐标 | forward 会收缩多少 |
| $v_X=1/6$ | fan-average target | Xavier initializer | 折中是否适合当前 activation |
| $\chi_f,\chi_b$ | 单层二阶矩乘数 | 尺度诊断指标 | 不能当成 Jacobian 极值 |

### 贯穿算例 $\mathcal I_\square$：$4\to8$ 近线性层

沿用 $n_{\mathrm{in}}=4,n_{\mathrm{out}}=8$，并在 linear 或 tanh 小信号近似中取 $c=d=1$。三个候选是

$$
v_F=\frac14,\qquad v_B=\frac18,\qquad
v_X=\frac{2}{4+8}=\frac16.
$$

Xavier 代回两条路径后得

$$
\chi_f=4\times\frac16=\frac23,qquad
\chi_b=8\times\frac16=\frac43.
$$

它没有同时守住两边，而是让两个 fan 共享 effective fan $6$。对 normal，$\operatorname{std}(W)=\sqrt{1/6}\approx0.408248$；对 uniform $[-a,a]$，

$$
a=\sqrt{3v_X}=\sqrt{\frac12}\approx0.707107.
$$

这两个分布只匹配前两阶 moment；有限宽的最大权重、tail 和 singular spectrum 仍会不同。

## 核心公式七问：$v_X=2/(n_{\mathrm{in}}+n_{\mathrm{out}})$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 在非方层中对称折中 forward 与 backward 的坐标尺度 |
| 对象 | 单个权重元素的 variance，不是 standard deviation |
| 来路 | 把 fan-in 和 fan-out 的算术平均当作 effective fan |
| 步骤 | 确认布局→计算两个 fan→求 variance→转成 normal std 或 uniform bound |
| 读法 | 方阵时两向同为 1；扩宽时 forward 收缩、backward 放大 |
| 检查 | $n_{\mathrm{in}}=n_{\mathrm{out}}=n$ 必须返回 $1/n$；单位与采样方式要匹配 |
| 去路 | ReLU gain、fan mode、正交初始化与 dynamical isometry |

### AI / 系统对应

Transformer MLP 的扩宽/压窄 projection、attention 的 $Q/K/V/O$ 投影和 convolution channel change 都是非方层。真正的工程对象是“存储布局 + forward contraction + initializer API”三元组，不是一个脱离形状的 `xavier_uniform_` 名字。

## 一、Shape 与 Fan 的定义

采用

$$
z=Wx+b,
\qquad
W\in\mathbb R^{n_{\mathrm{out}}\times n_{\mathrm{in}}}.
$$

于是

$$
\operatorname{fan\_in}=n_{\mathrm{in}},
\qquad
\operatorname{fan\_out}=n_{\mathrm{out}}.
$$

fan 不是矩阵维度名称本身，而是一个输出/输入坐标实际连接的项数。若代码使用 $xW$ 且 $W$ 存成 $[n_{\mathrm{in}},n_{\mathrm{out}}]$，必须确认初始化 API 的布局约定；PyTorch 官方文档明确提醒其 fan 计算默认对应 Linear 中 $xW^T$ 的用法。

## 二、前向守恒给出 Fan-In

设 $x_i,W_{ji}$ 独立、零均值，

$$
\mathbb E[x_i^2]=q_x,
\qquad
\operatorname{Var}(W_{ji})=v.
$$

则

$$
\mathbb E[z_j^2]
=n_{\mathrm{in}}v q_x.
$$

若希望线性层前后平均平方尺度相同，就要

$$
\boxed{v_{\mathrm{forward}}=\frac1{n_{\mathrm{in}}}}.
$$

这就是 LeCun/fan-in 尺度的核心。

## 三、反向守恒给出 Fan-Out

若上游梯度为 $g_z$，则

$$
g_x=W^Tg_z.
$$

在类似的独立零均值近似下，

$$
\mathbb E[(g_{x,i})^2]
=n_{\mathrm{out}}v\,\mathbb E[(g_{z,j})^2].
$$

守住反向平均平方尺度要求

$$
\boxed{v_{\mathrm{backward}}=\frac1{n_{\mathrm{out}}}}.
$$

方阵时两个目标一致；非方阵时一般冲突。

## 四、Glorot 的对称折中

Glorot–Bengio 采用

$$
\boxed{
v_{\mathrm{Xavier}}
=\frac{2}{n_{\mathrm{in}}+n_{\mathrm{out}}}
=\frac1{(n_{\mathrm{in}}+n_{\mathrm{out}})/2}.
}
$$

它相当于用输入/输出 fan 的算术平均作为 effective fan。对应的单层乘数为

$$
\chi_f=n_{\mathrm{in}}v
=\frac{2n_{\mathrm{in}}}{n_{\mathrm{in}}+n_{\mathrm{out}}},
$$

$$
\chi_b=n_{\mathrm{out}}v
=\frac{2n_{\mathrm{out}}}{n_{\mathrm{in}}+n_{\mathrm{out}}}.
$$

只有方阵时 $\chi_f=\chi_b=1$。若层突然扩宽，前向会收缩而反向会放大；突然压窄时相反。所谓“同时考虑”不等于“两边精确守恒”。

## 五、Normal 与 Uniform 是同一个方差合同

### Xavier normal

$$
W_{ji}\sim\mathcal N\!\left(
0,\frac{2}{n_{\mathrm{in}}+n_{\mathrm{out}}}
\right).
$$

### Xavier uniform

若 $W_{ji}\sim\mathcal U[-a,a]$，则 $\operatorname{Var}(W)=a^2/3$。令它等于 Xavier variance：

$$
\boxed{
a=\sqrt{\frac{6}{n_{\mathrm{in}}+n_{\mathrm{out}}}}.
}
$$

两者匹配前两 moments，却不匹配 tail、极值和有限宽谱。distribution family 仍是实验合同的一部分。

## 六、Gain 的准确含义

框架常写

$$
\operatorname{Var}(W)
=g^2\frac{2}{n_{\mathrm{in}}+n_{\mathrm{out}}},
$$

其中 $g$ 试图补偿 activation 的平均增益。若

$$
c_\phi(q)=
\frac{\mathbb E[\phi(\sqrt q Z)^2]}{q},
$$

理想前向条件近似为 $n_{\mathrm{in}}v\,c_\phi(q)\approx1$。单个常数 gain 只有在工作区与输入 law 固定时才有明确意义；饱和函数的 $c_\phi(q)$ 会随 $q$ 改变。

## 七、为什么它适合 Tanh，却不自动修好 Sigmoid

Tanh 在 0 附近斜率为 1、输出零中心，Xavier 能帮助初始 preactivation 留在较线性的区域。Sigmoid 的中心斜率仅 $1/4$ 且输出均值约 $1/2$，深层均值漂移和饱和仍在；Xavier 不是对 sigmoid 的全局梯度保证。

## 八、几何直觉与严格边界

当 $n_{\mathrm{in}}=n_{\mathrm{out}}=n$ 且元素 variance 为 $1/n$ 时，

$$
\mathbb E[WW^T]=I.
$$

这表示对初始化 ensemble，Gram matrix 的期望是 identity；高维下不同 row 常近正交。它不等于一次抽样就满足 $WW^T=I$，更不等于所有 singular values 接近 1。Gaussian square matrix 的极端 singular values 仍可相差很大。dynamical isometry 是更强的谱命题。

## 九、卷积与非标准参数张量

普通 convolution 常用

$$
n_{\mathrm{in}}=C_{\mathrm{in}}\prod_s k_s,
\qquad
n_{\mathrm{out}}=C_{\mathrm{out}}\prod_s k_s.
$$

grouped/depthwise/transposed convolution、embedding、attention projection 和自定义 einsum 的连接图不同。最安全的流程是：

1. 写出单个输出坐标的求和项数；
2. 写出反向单个输入坐标接收的项数；
3. 再核对框架 fan calculator 与 tensor layout。

## 十、Bias 与零初始化

zero bias 常用于保持初始 preactivation ensemble mean 为 0。bias 可以全零，因为不同 neurons 已由随机 weights 打破对称；但把同层所有 weights 也全零会让 hidden units 接收相同梯度，无法产生分工。输出层、residual branch 或门控参数可能有不同目标，不能把一个默认扩散到全模型。

## 十一、图：Forward 与 Backward 的非方阵冲突

先看图回答：当 $n_{\mathrm{out}}\gg n_{\mathrm{in}}$ 时，Xavier 的前向与反向乘数分别大于还是小于 1？

![[00-知识库管理/_assets/figures/neural-networks/fig-xavier-fan-compromise-v2.svg|900]]

> [!figure] 图 30.4-02　Xavier：fan-in、fan-out 与非方阵折中
> 左栏从 forward/backward 两个求和数导出互相冲突的目标；中栏给出 normal/uniform 同方差合同；右栏沿 aspect ratio 展示 $\chi_f,\chi_b$ 和矩阵布局警告。来源：依据 LeCun et al. 1998、Glorot–Bengio 2010、PyTorch 官方初始化文档及科学空间 7180/8725 独立绘制；由 [[00-知识库管理/_labs/code/plot_initialization_foundations_v2.py]] 确定性生成。

**怎样读图**：先看矩阵的箭头方向，确认两个 fan；再把目标 variance 代回乘数；最后检查代码中的存储布局是否与公式一致。

**图没有证明什么**：图没有证明算术平均是所有非方阵的最优折中，没有证明 $\mathbb E[WW^T]=I$ 意味着谱集中，也没有覆盖 residual、normalization 或 attention score 的联合尺度。

## 十二、工程验收

对每个参数张量输出 shape、fan-in/out、目标 variance、样本 variance、最大绝对值和 seed。以大量采样检查 normal/uniform variance；再在目标网络记录各层 preactivation/activation/gradient second moment。

若使用框架 helper，必须同时保存：

- 框架版本与 exact function；
- gain、mode、nonlinearity 参数；
- 权重的存储 shape 与 forward 乘法；
- truncation、clipping 或 quantization 是否改变实际 variance。

> [!summary]
> Xavier 是线性/近线性网络前后尺度的对称折中：方阵时归一到 $1/n$，非方阵时无法同时精确满足 fan-in 和 fan-out。正确使用它先要认清矩阵方向、activation gain 与真实架构。

- [[习题 - Xavier、Glorot 初始化]]
- [[解答 - Xavier、Glorot 初始化]]
