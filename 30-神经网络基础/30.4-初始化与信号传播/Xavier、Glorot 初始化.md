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
updated: 2026-08-23
---
# Xavier、Glorot 初始化

> [!abstract] 本章主问题
> 对一个 $n_{\mathrm{in}}\to n_{\mathrm{out}}$ 的非方线性层，前向二阶矩希望单权重 variance 为 $1/n_{\mathrm{in}}$，反向梯度却希望它为 $1/n_{\mathrm{out}}$。Xavier/Glorot 用 $2/(n_{\mathrm{in}}+n_{\mathrm{out}})$ 做对称折中；它是带假设的尺度折中，不是让随机矩阵变成正交矩阵的定理。

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
