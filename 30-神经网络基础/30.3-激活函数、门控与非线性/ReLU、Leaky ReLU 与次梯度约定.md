---
type: concept
status: draft
area: [neural-networks/activations, relu, leaky-relu, nonsmoothness]
aliases: [Rectifiers, ReLU Family, Dying ReLU]
node_id: NN-19
prerequisites: ["[[激活函数的角色、选择准则与函数性质]]", "[[激活、分支、广播与梯度累加]]", "[[凸集、凸组合与分离超平面]]"]
related: ["[[ELU、SELU 与自归一化接口]]", "[[Kaiming、He 初始化]]", "[[深度分离、线性区域与表达效率]]"]
sources: ["[[S-2010-Nair-Hinton-ReLU]]", "[[S-2013-Maas-Hannun-Ng-Leaky-ReLU]]", "[[S-2015-He-Delving-Rectifiers]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]"]
exercises: ["[[习题 - ReLU、Leaky ReLU 与次梯度约定]]"]
solutions: ["[[解答 - ReLU、Leaky ReLU 与次梯度约定]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-relu-family-boundaries-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---
# ReLU、Leaky ReLU 与次梯度约定

> [!abstract] 本章主问题
> ReLU 把正半轴保留为 identity、负半轴压为 0，由此得到廉价、稀疏、分段线性的网络，也引入 kink、死亡单元与正齐次重缩放。Leaky/PReLU 用负斜率修复“完全无梯度”，但同时改变稀疏性、方差传播和参数对称。必须把 classical derivative、convex subgradient 与 AD convention 分开。

## 课程位置与两遍学习路线

- **承接什么：** NN-18 的 S 形函数平滑有界但两端饱和；本页研究保留正半轴线性传播的另一种取舍；
- **本页解决什么：** 把 sparsity、positive homogeneity、kink convention、dying units 与 negative leak 放进同一推导；
- **后续为何需要：** NN-20 会用平滑指数负支替代硬折线，并讨论从单点性质升级到均值—方差固定点需要哪些条件。

**第一遍只做分段计算。** 对每个输入先判断所在区间，再写 output 与 slope；在零点单独标注 classical derivative 不存在和程序 convention。

**第二遍再连接深层系统。** 推导正齐次重缩放、二阶矩增益、dying mechanism、PReLU 参数梯度及低精度/稀疏实现边界。

### 问题链

1. ReLU 为什么避免正侧饱和，又为何会永久关闭某些单元？
2. kink 处的导数、凸次梯度集合和框架返回值有什么区别？
3. Leaky slope $\alpha$ 修复了什么，又牺牲了什么？
4. 正一阶齐次为何同时影响表达、初始化与参数对称性？
5. “ReLU 更容易训练”需要哪些架构和分布条件才能成为可检验命题？

> [!check] 第一遍停靠线
> 若你能在 $s_\triangle$ 上分别算出 ReLU 和 $\alpha=0.1$ Leaky ReLU 的值/VJP，并对零点明确声明约定，就可以进入 ELU/SELU；方差增益和 dying dynamics 留到第二遍。

## 符号与对象账本

| 对象 | 数学身份 | 在 AI 网络中的身份 | 关键边界 |
|---|---|---|---|
| $z$ | pre-activation | gate 判定输入 | 分布漂移会改变 active fraction |
| $\mathbf1_{z>0}$ | binary mask | ReLU backward cache | $z=0$ 需 convention |
| $\alpha$ | negative slope | Leaky/PReLU 超参数或参数 | 改变稀疏性与增益 |
| active fraction | 分布统计量 | signal/gradient throughput | 不是单点函数性质 |
| $\phi(cz)=c\phi(z)$ | positive homogeneity | layer rescaling gauge | 只对 $c>0$ |

### 贯穿算例：硬门、泄漏与零点约定

沿用 $s_\triangle=(-2,0,2)$，声明 ReLU 在零点的程序导数为 $0$；对 Leaky ReLU 取 $\alpha=0.1$，并声明零点使用负侧斜率 $\alpha$。于是

$$
\operatorname{ReLU}(s_\triangle)=(0,0,2),\qquad
\operatorname{ReLU}'_{\rm AD}(s_\triangle)=(0,0,1),
$$

$$
\operatorname{LReLU}_{0.1}(s_\triangle)=(-0.2,0,2),\qquad
\operatorname{LReLU}'_{\rm AD}(s_\triangle)=(0.1,0.1,1).
$$

upstream 全 1 时，后两组斜率就是 VJP。Leaky 让负区仍能收到信号，却不再产生 exact zero sparsity；零点数值是本页声明的程序规则，不是 classical derivative 定理，也不应假定所有框架相同。

## 核心公式七问：$\operatorname{LReLU}_\alpha(z)=\max(z,\alpha z)$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 用可控负斜率避免 ReLU 负半轴完全零梯度 |
| 对象 | $\alpha\in[0,1)$；固定时是超参数，可学习时成为 PReLU 参数 |
| 来路 | 两个 affine branches 的 pointwise maximum/分段选择 |
| 步骤 | $z>0$ 选 slope 1，$z<0$ 选 slope $\alpha$，$z=0$ 单独声明 convention |
| 读法 | 正证据原样通过，负证据被缩小但不完全删除 |
| 检查 | $\alpha=0$ 退化为 ReLU，$\alpha=1$ 退化为 identity；均为正齐次 |
| 去路 | He gain、PReLU、piecewise-linear regions、parameter symmetry 与 dead-unit diagnostics |

## 一、定义与分段导数

$$
\operatorname{ReLU}(x)=\max(0,x)
=\begin{cases}x,&x>0,\\0,&x\le0.\end{cases}
$$

在 $x\ne0$，

$$
\operatorname{ReLU}'(x)=\mathbf1_{x>0}.
$$

在 $x=0$，左导数 0、右导数 1，classical derivative 不存在。凸分析中的 subdifferential 是

$$
\partial\operatorname{ReLU}(0)=[0,1].
$$

框架返回 0、1 或别的值是 primitive convention；它不把不可微点变成可微点。

## 二、Leaky ReLU 与 PReLU

固定负斜率 $a\in(0,1)$ 的 leaky ReLU 为

$$
\phi_a(x)=\max(x,ax)
=\begin{cases}x,&x\ge0,\\ax,&x<0.
\end{cases}
$$

PReLU 把 $a$ 设为可学习参数，可按 layer 或 channel 共享。对 $x\ne0$，

$$
\frac{\partial\phi_a}{\partial x}
=\mathbf1_{x>0}+a\mathbf1_{x<0},
\qquad
\frac{\partial\phi_a}{\partial a}=x\mathbf1_{x<0}.
$$

若 $a<0$，函数在负半轴递减，不再是通常的单调 rectifier；若 $a>1$，负侧 gain 还可能更大。工程实现应声明是否约束 $a$。

## 三、正齐次与重缩放对称

对 $c\ge0$，ReLU 与固定 $a$ 的 leaky ReLU 满足

$$
\phi(cx)=c\phi(x).
$$

于是相邻层可作

$$
W_\ell\mapsto cW_\ell,
\qquad
W_{\ell+1}\mapsto c^{-1}W_{\ell+1}
$$

而函数不变。这产生 parameter non-identifiability，也解释 raw parameter norm/sharpness 可能随等价重缩放改变。$c<0$ 一般不能如此搬移。

## 四、分段线性网络

固定每个 ReLU 的 active/inactive mask 后，网络在该输入 region 内是仿射函数。region 边界由某些 preactivation 等于 0 定义；跨边界时 Jacobian 可跳变。

因此：

- 一阶导在几乎处处存在；
- 每个 open region 内 Hessian 对输入为 0；
- 全局函数仍可非常复杂，因为 region 数随结构增长；
- “Hessian 几乎处处为 0”不表示函数没有 curvature-like optimization difficulty。

## 五、稀疏激活与信息保留

负 preactivation 被精确映为 0，会产生 activation sparsity 和条件计算机会；正半轴不饱和，幅度信息继续传递。代价是负半轴所有幅度折叠到同一值，局部不可逆。

Leaky ReLU 保留负半轴的排序与小梯度，但输出不再精确稀疏。稀疏、信息保留和梯度通道之间存在设计权衡。

## 六、Dying ReLU 的机制

对单元 $z=w^Tx+b$，若训练数据上始终 $z<0$，则 ReLU output 与 local derivative 都为 0：

$$
\nabla_wL=\sum_i\bar h_i\mathbf1_{z_i>0}x_i=0,
\qquad
\nabla_bL=\sum_i\bar h_i\mathbf1_{z_i>0}=0.
$$

该单元在当前数据与路径上无法靠一阶梯度自行恢复。诱因可能是过大更新、负 bias、输入分布漂移或不合适初始化。

“一次 mini-batch 全负”不等于永久死亡；应在完整数据/时间窗口与 train/eval 状态下定义 dead rate。

## 七、Leaky slope 如何修复又引入新尺度

若 $z<0$，leaky ReLU 仍传回 $a\bar h$，所以 $a>0$ 避免严格零梯度。但深层全负路径的 activation contribution 仍按 $a^k$ 缩小；$a=0.01$ 跨十层约为 $10^{-20}$。

因此 leaky 不等于“没有 vanishing gradient”。它只移除 ReLU 负侧的精确零门。

## 八、二阶矩与初始化接口

若 $Z$ 关于 0 对称、$E[Z^2]=q$，则 ReLU 有

$$
E[\operatorname{ReLU}(Z)^2]=\frac q2.
$$

对 leaky ReLU，

$$
E[\phi_a(Z)^2]=\frac{1+a^2}{2}q.
$$

这给出 activation-aware weight variance 的核心因子，但依赖对称性和独立近似。训练后分布偏斜时，$1/2$ 不必保持。

## 九、均值不为零

即使 $Z$ 关于 0 对称，

$$
E[\operatorname{ReLU}(Z)]>0
$$

只要 $Z$ 非退化。若 $Z\sim\mathcal N(0,q)$，

$$
E[\operatorname{ReLU}(Z)]=\sqrt{\frac{q}{2\pi}}.
$$

所以 variance propagation 不能只追踪 second moment；mean、variance 与 second moment $E[H^2]$ 是三个不同对象。

## 十、Lipschitz 与 smoothness

ReLU 是 1-Lipschitz；$a\in[0,1]$ 的 leaky ReLU 也是 1-Lipschitz。PReLU 若学习到 $|a|>1$，Lipschitz constant 变为 $|a|$。

它们连续但在 0 处通常不 $C^1$。对输入梯度惩罚、二阶元学习或 PDE residual，必须说明 kink 的采样概率与框架高阶 convention。

## 十一、一个二维几何例子

令

$$
f(x_1,x_2)=\operatorname{ReLU}(x_1+x_2-1).
$$

直线 $x_1+x_2=1$ 把平面分成：

- inactive half-space：$f=0,\nabla f=(0,0)$；
- active half-space：$f=x_1+x_2-1,\nabla f=(1,1)$；
- boundary：classical gradient 不存在，AD 按 convention 返回某个值。

多个单元的超平面切分叠加，形成 piecewise-affine partition。

## 十二、实现边界

- in-place ReLU 若覆盖 backward 所需 primal/mask，系统必须保存 mask 或追踪 version；
- fused kernels 可能只保存 one-bit mask，而不是完整 input；
- at zero 的 exact comparison 受 dtype、flush-to-zero 与前序舍入影响；
- sparse activation 不自动变成 wall-clock 加速，硬件 kernel 必须利用 sparsity；
- quantization calibration 要覆盖正半轴 tail，否则 clipping 改变输出与 gradient surrogate。

## 十三、比较协议

比较 ReLU/leaky/PReLU 时记录：

1. negative slope 固定值、初始化值、共享粒度与约束；
2. dead rate、negative-path derivative 和 activation sparsity；
3. matched initialization factor $(1+a^2)/2$；
4. parameter/FLOP overhead；
5. per-layer mean、second moment、gradient norm；
6. kink convention 与 gradient-check 采样规则；
7. train/validation performance、wall-clock 与 seeds。

## 十四、图：四种机制而非三条曲线

先看图回答：Leaky ReLU 修复的是哪一条局部通道，为什么它没有消除深层尺度问题？

![[00-知识库管理/_assets/figures/neural-networks/fig-relu-family-boundaries-v2.svg|900]]

> [!figure] 图 30.3-03　ReLU family：区域边界、死亡单元与负侧尺度
> 左栏显示 piecewise-linear region 与 kink；中栏追踪一个单元从 active 到 dataset-wide inactive 的梯度机制；右栏比较 ReLU、leaky 与 PReLU 的负侧 slope、二阶矩和稀疏性。来源：依据 Nair–Hinton 2010、Maas–Hannun–Ng 2013 与 He 等 2015 独立绘制；由 [[00-知识库管理/_labs/code/plot_activation_foundations_v2.py]] 确定性生成。

**怎样读图**：先区分单点 kink、单 batch inactive 与跨数据长期 dead，再读负斜率如何改变 gradient 与 moment scale。

**图没有证明什么**：图没有证明 leaky/PReLU 在任意任务优于 ReLU，也没有把局部非零斜率升级成深层梯度下界。

## 十五、常见错误

1. 把框架在 0 返回 0 说成 classical derivative；
2. 把一次输出 0 认定为永久死亡；
3. 认为 leaky slope 非零就不会梯度消失；
4. 忘记 leaky/PReLU 改变初始化二阶矩因子；
5. 把稀疏 tensor 值与硬件稀疏加速混为一谈；
6. 忽略正齐次导致的参数重缩放等价；
7. 用输入 Hessian 几乎处处为 0 推出网络“没有非线性”。

## 十六、回顾与练习

> [!summary]
> ReLU 的核心不是一条折线，而是正侧 identity、负侧 exact zero、kink convention、分段仿射区域与正齐次对称的组合。Leaky/PReLU 重新打开负侧通道，但必须重新审计尺度、稀疏和参数语义。

- [[习题 - ReLU、Leaky ReLU 与次梯度约定]]
- [[解答 - ReLU、Leaky ReLU 与次梯度约定]]
