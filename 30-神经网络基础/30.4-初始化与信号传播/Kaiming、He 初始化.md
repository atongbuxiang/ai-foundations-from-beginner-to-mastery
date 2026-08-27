---
type: derivation
status: draft
area: [neural-networks/initialization, kaiming, he, rectifiers]
aliases: [He Initialization, Kaiming Initialization]
node_id: NN-27
prerequisites: ["[[方差传播与宽层均值场近似]]", "[[ReLU、Leaky ReLU 与次梯度约定]]", "[[Xavier、Glorot 初始化]]"]
related: ["[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]", "[[偏置、输出层与零初始化的对称性边界]]"]
sources: ["[[S-2015-He-Delving-Rectifiers]]", "[[S-2026-PyTorch-NN-Init]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]"]
exercises: ["[[习题 - Kaiming、He 初始化]]"]
solutions: ["[[解答 - Kaiming、He 初始化]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-kaiming-rectifier-moments-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---
# Kaiming、He 初始化

> [!abstract] 本章主问题
> ReLU 会把 centered symmetric preactivation 的负半轴截成 0，所以二阶矩平均只保留一半。He 初始化把单权重 variance 从 $1/\text{fan}$ 提高到 $2/\text{fan}$；对负侧 slope 为 $a$ 的 rectifier，修正为 $2/[(1+a^2)\text{fan}]$。这里守住的是 second moment，而不是 activation variance、非零比例或全 Jacobian spectrum。

## 一、从一般 Leaky Rectifier 开始

定义

$$
\phi_a(z)=
\begin{cases}
z,&z>0,\\
az,&z\le0,
\end{cases}
\qquad a\ge0.
$$

$a=0$ 是 ReLU，固定小 $a$ 是 Leaky ReLU，learnable $a$ 是 PReLU。

若 $Z$ 关于 0 对称、$\mathbb E[Z^2]=q$，则正负半轴各承担一半二阶矩：

$$
\mathbb E[Z^2\mathbf 1_{\{Z>0\}}]
=\mathbb E[Z^2\mathbf 1_{\{Z\le0\}}]
=\frac q2.
$$

所以

$$
\boxed{
\mathbb E[\phi_a(Z)^2]
=\frac{1+a^2}{2}q.
}
$$

这个结论只需分布对称和有限二阶矩；并不必须先假设 Gaussian。

## 二、前向 He Scale

对 $n_{\mathrm{in}}$ 个输入的线性层，令单权重 variance 为 $v$。零 bias 近似下，

$$
q_{\ell}
=n_{\mathrm{in}}v\,
\frac{1+a^2}{2}q_{\ell-1}.
$$

要令 $q_\ell=q_{\ell-1}$，必须选择

$$
\boxed{
v_{\mathrm{He,fan\_in}}
=\frac{2}{(1+a^2)n_{\mathrm{in}}}.
}
$$

ReLU 的 $a=0$ 给

$$
\boxed{v=\frac2{n_{\mathrm{in}}}}.
$$

这比 Xavier 方阵尺度 $1/n$ 大一倍，正好补偿负半轴被置零造成的二阶矩损失。

## 三、Normal 与 Uniform 参数

### Kaiming normal

$$
W_{ji}\sim\mathcal N\!\left(
0,\frac{2}{(1+a^2)\operatorname{fan}}
\right),
$$

标准差为

$$
\sqrt{\frac{2}{(1+a^2)\operatorname{fan}}}.
$$

### Kaiming uniform

若 $W\sim\mathcal U[-b,b]$，由 $\operatorname{Var}(W)=b^2/3$ 得

$$
\boxed{
b=\sqrt{\frac{6}{(1+a^2)\operatorname{fan}}}.
}
$$

框架常把

$$
g(a)=\sqrt{\frac{2}{1+a^2}}
$$

称为 rectifier gain。

## 四、为什么必须说 Second Moment

对 $Z\sim\mathcal N(0,q)$，

$$
\mathbb E[\operatorname{ReLU}(Z)]
=\sqrt{\frac{q}{2\pi}},
$$

$$
\mathbb E[\operatorname{ReLU}(Z)^2]=\frac q2.
$$

因此

$$
\operatorname{Var}(\operatorname{ReLU}(Z))
=q\left(\frac12-\frac1{2\pi}\right),
$$

不是 $q/2$。He derivation 保持的是平均平方长度/uncentered second moment。下一层新权重零均值可重新把 preactivation ensemble mean 拉回 0，但 activation 本身没有零中心。

## 五、反向为何出现同一个二分之一

ReLU derivative 在非零点为 $\mathbf 1_{\{Z>0\}}$。对 symmetric continuous $Z$，

$$
\mathbb E[\phi'(Z)^2]=\frac12.
$$

Leaky ReLU 则为

$$
\mathbb E[\phi_a'(Z)^2]
=\frac{1+a^2}{2}.
$$

所以激活带来的 forward second-moment factor 与 backward derivative factor 恰好相同。若层宽相等，fan-in He scale 可同时守住两条标量递推；非方层仍有 fan-in/fan-out 冲突。

## 六、Convolution 的 Fan

普通 $d$ 维 convolution 中，

$$
\operatorname{fan\_in}
=C_{\mathrm{in}}\prod_{s=1}^d k_s,
\qquad
\operatorname{fan\_out}
=C_{\mathrm{out}}\prod_{s=1}^d k_s.
$$

直觉是一个输出位置汇总多少输入，一个输入位置向多少输出通道/核位置传播。padding 不改变参数 fan，但边界位置的实际有效输入数可能更少；group/depthwise convolution 要按真实 tensor shape 与连接图处理。

## 七、Mode：Fan-In 或 Fan-Out

当前 PyTorch Kaiming API 允许：

- mode 为 fan-in：优先保持 forward magnitude；
- mode 为 fan-out：优先保持 backward magnitude。

这不是两个名称相同的实现细节，而是在非方层选择不同目标。权重存储若与框架预期转置关系不同，fan 会算反，尺度因子可能达到 aspect ratio 的平方根级差异。

## 八、PReLU 的时间一致性问题

若初始化时使用 $a_0$，

$$
v=\frac{2}{(1+a_0^2)n_{\mathrm{in}}},
$$

但训练后 PReLU slope 变为 $a_t$，当前二阶增益变成

$$
n_{\mathrm{in}}v\frac{1+a_t^2}{2}
=\frac{1+a_t^2}{1+a_0^2}.
$$

因此初始化只校准 $t=0$；learned activation、weight drift 与 normalization 会共同改变后续尺度。

## 九、He 初始化没有解决什么

它没有自动解决：

- ReLU 单元长期不激活；
- bias 把 preactivation 推离对称分布；
- residual branches 相加后的 covariance；
- BatchNorm/LayerNorm 的新统计量；
- 低精度 overflow、optimizer update scale；
- singular values 的宽分布与方向性消失/爆炸。

“每层 variance 看起来稳定”仍可能同时存在极坏的 Jacobian condition number。

## 十、Truncation 与低精度

若先从 normal 采样再截断而不重标定，实际 variance 会小于目标；量化、clipping 和 low-precision cast 也会改变 distribution。发布级初始化必须在最终存储 dtype 上测 sample moment，而不是只抄 generator 的 nominal standard deviation。

## 十一、图：负半轴如何改变增益

先看图回答：为什么 ReLU 的 factor 是 $1/2$，而 Leaky ReLU 是 $(1+a^2)/2$，不是 $(1+a)/2$？

![[00-知识库管理/_assets/figures/neural-networks/fig-kaiming-rectifier-moments-v2.svg|900]]

> [!figure] 图 30.4-03　He/Kaiming：半轴二阶矩、gain 与卷积 fan
> 左栏把 symmetric input 的正负二阶质量拆开；中栏从 $(1+a^2)/2$ 导出 normal/uniform 参数；右栏区分 dense/conv fan、fan-in/fan-out mode 与 PReLU drift。来源：依据 He et al. 2015、PyTorch 官方初始化文档及本库 ReLU moment 推导独立绘制；由 [[00-知识库管理/_labs/code/plot_initialization_foundations_v2.py]] 确定性生成。

**怎样读图**：先看平方后负侧贡献变成 $a^2$，再把 activation factor 与 fan/weight variance 相乘，最后核对代码使用的 mode 与参数布局。

**图没有证明什么**：图没有证明 activation variance 精确保持，没有证明 finite-width masks 恰有一半激活，也没有证明 Kaiming scale 足以获得 dynamical isometry 或训练后稳定。

## 十二、最小验收协议

1. 用大量样本检查目标 weight variance 与 uniform bound；
2. 对 symmetric Gaussian input 测 activation second moment、variance、positive rate；
3. 分别扫描 dense/conv/grouped conv 与不同 aspect ratio；
4. 用 dot test 核对 backward，再记录各层 gradient second moment；
5. 改变 $a$、bias、dtype、truncation 和训练步数，量化公式偏离。

> [!summary]
> He 初始化的关键不是“ReLU 更大一点”，而是平方后的正负半轴账本：rectifier factor 为 $(1+a^2)/2$。fan-in/fan-out、second moment/variance 和初始化/训练时刻必须明确区分。

- [[习题 - Kaiming、He 初始化]]
- [[解答 - Kaiming、He 初始化]]
