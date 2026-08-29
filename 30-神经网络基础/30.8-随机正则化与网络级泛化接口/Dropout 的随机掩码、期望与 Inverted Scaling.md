---
type: derivation
status: draft
area: [neural-networks/regularization, dropout, bernoulli-noise, train-eval]
aliases: [Inverted Dropout, Bernoulli Dropout]
node_id: NN-57
prerequisites: ["[[随机变量、分布与分位数]]", "[[期望、方差与矩]]", "[[计算图、拓扑序与前向执行]]", "[[训练集、验证集、测试集与自适应复用]]"]
related: ["[[Dropout 的方差、共适应解释与 Bayesian 边界]]", "[[DropConnect、权重噪声与激活噪声]]", "[[遮蔽预测、Teacher–Student 与自监督目标]]", "[[归一化的对象、轴与不变性]]"]
sources: ["[[S-2014-Srivastava-Dropout]]", "[[S-2026-PyTorch-Dropout-Stochastic-Depth]]", "[[S-2021-Su-8770-Dropout-MLM-MAE]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]"]
exercises: ["[[习题 - Dropout 的随机掩码、期望与 Inverted Scaling]]"]
solutions: ["[[解答 - Dropout 的随机掩码、期望与 Inverted Scaling]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-dropout-expectation-inverted-scaling-v2.svg]]"
created: 2026-08-24
updated: 2026-08-29
---

# Dropout 的随机掩码、期望与 Inverted Scaling

> [!abstract] 本章主问题
> Dropout 不是一句“随机删神经元”，而是一份带概率空间、广播轴、缩放、训练—推理状态和随机数流的算子合同。Inverted Dropout 在训练时将保留项除以 keep probability，使被 mask 张量的条件均值保持不变；它同时放大二阶矩，而且只在后续映射为仿射时自动保持输出均值。经过一般非线性，一次 evaluation pass 不等于随机网络预测的精确平均。

## 课程位置与两遍学习路线

- **承接什么：** 概率章节给出 Bernoulli 变量与条件矩，计算图章节要求 backward 对应同一次 forward realization；
- **本页解决什么：** 把 Dropout 写成训练态随机线性算子与评估态 identity 的双状态合同，精确区分一阶矩、二阶矩和非线性输出；
- **后续为何需要：** NN-58—60 会分别研究风险解释、噪声位置与随机路径，所有结论都必须建立在 mask 轴、keep probability 和缩放约定已经固定的基础上。

**第一遍只算固定输入的条件矩。** 对一个两维向量枚举四个 masks，核对输出均值、方差、平方范数和同-mask VJP。

**第二遍再讨论网络语义。** 加入 element/channel/token/path mask、normalization placement、train/eval、checkpoint RNG、分布式随机流和非线性 Jensen gap。

### 问题链

1. drop probability $p$ 与 keep probability $q$ 怎样进入 sampling 与 scaling？
2. 除以 $q$ 精确保住的是哪个条件期望，为什么不保住方差？
3. backward 为什么必须复用 forward mask，而不能重新采一个？
4. $\mathbb E[Y]=x$ 为什么不能推出 $\mathbb E[f(Y)]=f(x)$？
5. element、channel、token 与 sample masks 的边际 keep rate 相同，为何联合随机函数仍不同？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal D_\square$ 中从 $x=(2,1)$、$q=1/2$、$m=(1,0)$ 得到 $Y=(4,0)$，并算出 $\mathbb E Y=x$、$\operatorname{Var}(Y\mid x)=(4,1)$，就已掌握本页主干。

## 符号与对象账本

| 对象 | 定义 | 必须声明 | 不自动保证 |
|---|---|---|---|
| $p$ / $q=1-p$ | drop / keep probability | 训练或推理时是否启用 | 二阶矩保持 |
| $M$ | Bernoulli mask tensor | shape、广播轴、相关结构 | 各 use-site 独立 |
| $D_M$ | $\operatorname{Diag}(M/q)$ | inverted scaling | 非线性输出均值保持 |
| $Y=D_Mx$ | stochastic activation | 固定输入下的随机变量 | 单次 realization 接近 $x$ |
| RNG state | mask 的随机数身份 | seed、rank、checkpoint recompute | 可复现性 |
| eval operator | identity / 显式 MC | mode 与 averaging object | posterior predictive |

### 贯穿算例 $\mathcal D_\square$：两维 Activation Mask

固定本卷共享对象

$$
x=(2,1)^{\mathsf T},
\qquad
q=\frac12,
\qquad
M_1,M_2\overset{\mathrm{iid}}\sim\operatorname{Bernoulli}(1/2).
$$

Inverted Dropout 为

$$
Y=\frac Mq\odot x=2M\odot x.
$$

四个等概率 outputs 是

$$
(0,0),\ (4,0),\ (0,2),\ (4,2).
$$

因此

$$
\boxed{
\mathbb E[Y\mid x]=(2,1)=x,
\qquad
\operatorname{Cov}(Y\mid x)=
\begin{bmatrix}4&0\\0&1\end{bmatrix}
}.
$$

同时

$$
\|x\|_2^2=5,
\qquad
\mathbb E\|Y\|_2^2=\frac1q\|x\|_2^2=10.
$$

若本次 realization 是 $m=(1,0)$，则 $Y=(4,0)$；对上游 $g=(1,-2)$，同一 mask 给

$$
\boxed{
\bar x=\frac mq\odot g=(2,0)
}.
$$

重新采样 backward mask 会得到另一随机函数的导数，而不是同一次 forward 的 VJP。

## 核心公式七问：Inverted Dropout 双状态合同

$$
\boxed{
Y_{\mathrm{train}}=\frac Mq\odot x,
\qquad
Y_{\mathrm{eval}}=x,
\qquad
\mathbb E_M[Y_{\mathrm{train}}\mid x]=Y_{\mathrm{eval}}
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 训练时采样子函数，同时保持被 mask 张量的一阶条件均值 |
| 对象 | 固定输入下、指定 mask 轴的随机 activation |
| 来路 | Bernoulli keep event 乘 $1/q$ 的 importance-like 校正 |
| 步骤 | sample mask→broadcast→scale/multiply→保存 RNG/mask→同 realization backward |
| 读法 | 均值匹配只发生在 mask 所在局部张量，二阶矩与后续非线性会改变 |
| 检查 | 四状态枚举、sample mean/variance、train/eval、checkpoint 与 rank reproducibility |
| 去路 | MC Dropout、DropConnect、DropPath、attention dropout 与 structured pruning |

### AI / 系统对应

Transformer 中 attention-probability dropout、residual dropout、token dropout 与 DropPath 都可能使用相同 $p$，却作用在不同张量和广播轴上。高质量配置必须记录 layer、axis、RNG stream、fused kernel 和 evaluation mode；只记录一个全局 `dropout=0.1` 无法复现实验。

## 一、学习目标

读完本节，你应能：

1. 区分 drop probability $p$ 与 keep probability $q$；
2. 写出 Bernoulli mask 的概率空间、shape 与广播轴；
3. 推导 Inverted Dropout 的条件均值、方差和二阶矩；
4. 推导 Dropout backward，并解释 dropped coordinates 的梯度；
5. 区分历史 test-time scaling 与现代 training-time scaling；
6. 构造 $\mathbb E[f(Y)]\ne f(\mathbb E Y)$ 的反例；
7. 区分 element、channel、token、sample 与 path masks；
8. 审计 placement、normalization、train/eval、RNG、重算与分布式边界。

## 二、先把随机对象写完整

给定输入张量

$$
x\in\mathbb R^{s_1\times\cdots\times s_k},
$$

drop probability 为 $p\in[0,1)$，keep probability 为

$$
q=1-p\in(0,1].
$$

最基础的逐元素 mask 满足

$$
m_i\overset{\mathrm{iid}}\sim\operatorname{Bernoulli}(q).
$$

训练态 Inverted Dropout 定义为

$$
\boxed{
y_i=\frac{m_i}{q}x_i
}.
$$

evaluation 时定义为

$$
\boxed{y_i=x_i}.
$$

这里的 `training` flag 是函数定义的一部分，不是性能提示。若训练时忘记切回 evaluation，输出继续随机；若训练时错误使用 evaluation 路径，正则化干预根本没有发生。

> [!warning] $p$ 与 $q$ 的命名陷阱
> 有的论文用 $p$ 表示 keep probability，有的 API 用 `p` 表示 drop probability。本节固定 $p=P(m=0)$、$q=P(m=1)=1-p$。引用任何公式前先翻译符号，不要凭变量名套用。

## 三、为什么要除以 $q$

条件于固定输入 $x_i$：

$$
\mathbb E[y_i\mid x_i]
=\mathbb E\left[\frac{m_i}{q}x_i\middle|x_i\right]
=\frac{x_i}{q}\mathbb E[m_i]
=x_i.
$$

因此

$$
\boxed{
\mathbb E[y\mid x]=x
}.
$$

这就是 inverted scaling 的精确目标：训练态随机张量在 mask 条件期望下与 evaluation 张量相同。

注意它只证明一个局部张量恒等式，没有证明：

- 每次训练前向等于 evaluation 前向；
- loss 的期望不变；
- gradient 的期望等于无 Dropout gradient；
- 深层网络最终预测的期望不变；
- 泛化一定改善。

这些对象都含后续非线性、损失或参数依赖，需另行推导。

## 四、完整手算：$x=(2,-1,3)$

取

$$
q=0.5,
\qquad
m=(1,0,1).
$$

则

$$
y=\frac{m}{q}\odot x
=2(1,0,1)\odot(2,-1,3)
=(4,0,6).
$$

这个 sample 并不接近 $x$，但逐坐标枚举可验证期望保持。例如第一个坐标：

$$
y_1=
\begin{cases}
0,&P=0.5,\\
4,&P=0.5,
\end{cases}
$$

所以

$$
\mathbb E[y_1]=2=x_1.
$$

“均值保持”是跨 mask 重复的陈述，不是单次 realization 的陈述。

## 五、均值保持的二阶矩代价

由于 $m_i^2=m_i$：

$$
\mathbb E[y_i^2\mid x_i]
=\frac{x_i^2}{q^2}\mathbb E[m_i]
=\frac{x_i^2}{q}.
$$

所以

$$
\boxed{
\operatorname{Var}(y_i\mid x_i)
=\frac{1-q}{q}x_i^2
=\frac pqx_i^2
}.
$$

向量平方范数满足

$$
\boxed{
\mathbb E[\|y\|_2^2\mid x]
=\frac1q\|x\|_2^2
}.
$$

在上例中

$$
\|x\|_2^2=4+1+9=14,
$$

而

$$
\mathbb E\|y\|_2^2=28.
$$

三个坐标的条件方差为

$$
(4,1,9).
$$

当 $q$ 很小时，保留事件少但放大因子 $1/q$ 很大，分布呈现“多数为零、少数很大”的形态；均值正常并不代表数值尺度或尾部温和。

## 六、Backward：同一个 Mask 也门控梯度

给定上游梯度

$$
g=\nabla_y\mathcal L,
$$

在固定 realization $m$ 下，Dropout 对 $x$ 是对角线性映射：

$$
y=D_mx,
\qquad
D_m=\operatorname{diag}(m/q).
$$

因此 VJP 为

$$
\boxed{
\nabla_x\mathcal L
=\frac mq\odot g
}.
$$

被 drop 的 coordinates 在本次 forward 对 loss 没有局部影响，梯度为零；被保留的 coordinates 梯度放大 $1/q$。Backward 必须复用 forward 的同一 mask，不能重新采样，否则计算的不再是本次随机函数 realization 的导数。

若 Dropout 位于参数化层之后，参数梯度也通过该 mask 门控；但 optimizer momentum、weight decay 或其他 batch 样本仍可能更新参数，所以“本样本 dropped”不等于“参数本步绝对不动”。

## 七、历史 Scaling 与 Inverted Scaling

### 7.1 历史写法

训练：

$$
y^{\rm train}=m\odot x.
$$

测试：

$$
y^{\rm eval}=q x.
$$

两者在被 mask 张量层面满足

$$
\mathbb E[y^{\rm train}\mid x]=qx=y^{\rm eval}.
$$

### 7.2 Inverted 写法

训练：

$$
y^{\rm train}=\frac mq\odot x.
$$

测试：

$$
y^{\rm eval}=x.
$$

现代框架常用第二种，因为推理无需额外缩放，且模块 evaluation 为 identity。

两种写法可以通过邻接权重的重参数化联系，但在有限精度、weight decay、normalization placement、初始化和 optimizer state 下，不能只改一行 scaling 而假定完整训练轨迹严格相同。

## 八、为什么非线性后均值不再自动保持

局部恒等式是

$$
\mathbb E[Y]=x.
$$

若后续为仿射映射 $f(y)=Ay+b$，则线性期望给出

$$
\mathbb E[f(Y)]=A\mathbb E[Y]+b=f(x).
$$

但一般非线性只满足 Jensen 型关系或没有固定方向：

$$
\mathbb E[f(Y)]\ne f(\mathbb E[Y]).
$$

### 8.1 一个最小反例

取标量 $x=1,q=0.5$，则

$$
Y=
\begin{cases}
0,&P=0.5,\\
2,&P=0.5.
\end{cases}
$$

令

$$
f(y)=\operatorname{ReLU}(y-1).
$$

则

$$
\mathbb E[f(Y)]
=\tfrac12 f(0)+\tfrac12 f(2)
=\tfrac12,
$$

而

$$
f(\mathbb E[Y])=f(1)=0.
$$

所以 evaluation identity 只把随机张量替换为其均值，不精确计算后续非线性随机网络的 predictive mean。

## 九、Mask Granularity 决定联合分布

“Dropout rate 相同”不足以定义随机函数。设 activation shape 为

$$
x\in\mathbb R^{B\times T\times C}.
$$

常见选择包括：

| 类型 | 典型 mask shape | 被共享的轴 | 结构含义 |
|---|---|---|---|
| element dropout | $B\times T\times C$ | 无 | 每个元素独立 |
| token dropout | $B\times T\times1$ | channel | 整个 token vector 删除 |
| feature/channel dropout | $B\times1\times C$ | token | 同一样本同一 channel 共享 |
| sample gate | $B\times1\times1$ | token、channel | 整个样本 branch 共享 |
| batch-shared gate | $1\times1\times1$ | 全 batch | 所有样本同一 realization |

共享 mask 会制造坐标、token 或样本间相关性。单坐标 marginal 可能相同，联合分布、输出 covariance 与 gradient variance 却不同。

## 十、Placement 不是无关紧要的括号

比较下列结构：

$$
\operatorname{Dropout}(\phi(Wx)),
$$

$$
\phi(\operatorname{Dropout}(Wx)),
$$

$$
\operatorname{Norm}(\operatorname{Dropout}(x)),
$$

$$
\operatorname{Dropout}(\operatorname{Norm}(x)).
$$

它们一般不是同一个随机函数：

- 非线性与 expectation 不交换；
- Dropout 放在 BatchNorm 统计量之前会改变 batch moments；
- 放在 LayerNorm 前会改变同 token 的归一化 denominator；
- 放在 residual addition 前只扰动 branch，放在 addition 后连 identity rail 也扰动；
- 放在 logits 前会改变 temperature/margin，放在 loss 后没有定义。

必须在计算图上标出准确边，而不是只在配置中写一个 rate。

## 十一、随机数流、重算与分布式

随机算子还需要以下状态合同：

1. seed 与 generator/device；
2. 每 step、microbatch、layer 的 counter/order；
3. data-parallel ranks 是否独立采样；
4. gradient checkpoint 重算是否复现原 mask；
5. pipeline stage 重放与异常重试是否保持随机语义；
6. 编译/fusion 是否改变 RNG consumption order；
7. evaluation 与 MC Dropout 是否有意开启随机性。

若 checkpoint backward 重算出新 mask，forward value 与 backward derivative不属于同一随机函数；这不是“多一点正则”，而是梯度正确性错误。

## 十二、最小实现测试

对固定 $x$、大样本数 $S$，至少验证：

$$
\frac1S\sum_{s=1}^Sy^{(s)}\approx x,
$$

$$
\frac1S\sum_{s=1}^S(y_i^{(s)}-x_i)^2
\approx\frac pqx_i^2.
$$

还要检查：

- training 中 empirical zero rate 接近 $p$；
- evaluation 完全 deterministic 且等于 identity；
- backward mask 与 forward mask 相同；
- channel/token variants 的共享轴正确；
- $p=0$ 退化为 identity；
- 极端 $p\to1$ 被 API 拒绝或数值行为明确；
- checkpointing 与 non-checkpointing 在固定 RNG 下梯度一致；
- distributed ranks 的共享/独立策略符合协议。

## 十三、常见误区

1. **“`p=0.1` 表示保留 10%”**：多数现代 API 的 `p` 是 drop probability；
2. **“除以 $q$ 后方差也保持”**：方差乘上 $p/q$ 的输入相关项；
3. **“一次 eval 就是所有子网络精确平均”**：一般非线性反例已否定；
4. **“Dropout2d 逐像素采样”**：许多框架按 channel 采样；
5. **“Backward 可重新采 mask”**：这破坏 realization-level 导数；
6. **“mask 乘零一定节省 FLOP”**：先计算再乘 mask 并不省前面的计算；
7. **“加了 Dropout 就证明泛化更好”**：这是待验收经验命题。

## 十四、图：均值、方差与非线性

先看图回答：为什么 $x=(2,-1,3)$ 的一次 realization 会变成 $(4,0,6)$，但期望仍等于 $x$？为什么 keep rate 越小，variance amplifier 越大？右栏的 ReLU 反例否定了哪一种常见说法？

![[00-知识库管理/_assets/figures/neural-networks/fig-dropout-expectation-inverted-scaling-v2.svg|900]]

> [!figure] 图 30.8-01　Inverted Dropout 的 mask realization、variance amplifier 与非线性期望反例
> 左栏展示 $q=0.5$ 的逐元素 mask 与 $1/q$ scaling；中栏画出 $p/q=(1-q)/q$ 随 keep rate 的放大；右栏用 $f(y)=\operatorname{ReLU}(y-1)$ 构造 $\mathbb E f(Y)\ne f(\mathbb EY)$。来源：依据 Srivastava et al.、PyTorch 当前 Dropout 合同及本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_random_regularization_foundations_v2.py]] 确定性生成。

**怎样读图**：先区分单次 mask realization 与跨 mask 期望，再从一阶矩走到二阶矩，最后把局部张量均值与整网非线性预测均值分开。

**图没有证明什么**：图不证明某个 Dropout rate 跨任务最优，不证明 deterministic evaluation 等于 Bayesian posterior predictive，也不证明均值匹配会带来更低 test risk。

## 十五、最小验收

1. 写出 $p,q,m,x,y$ 的对象与 shape；
2. 推导 $\mathbb E[y\mid x]=x$；
3. 推导 $\operatorname{Var}(y_i\mid x)=px_i^2/q$；
4. 复算 $(2,-1,3)$ toy 的输出、方差与平方范数；
5. 推导 Dropout VJP；
6. 比较历史 scaling 与 inverted scaling；
7. 构造非线性期望反例；
8. 区分五类 mask granularity；
9. 解释 placement、normalization、RNG 与 checkpoint 边界；
10. 写出可执行的 train/eval/moment/gradient 测试。

> [!summary]
> Inverted Dropout 是训练态随机线性算子 $D_m=\operatorname{diag}(m/q)$、evaluation 态 identity 的两状态合同。它精确保持被 mask 张量的条件均值，却把二阶矩放大为 $1/q$，并通过同一 mask 门控反向梯度；经过一般非线性后，均值替换不再等于随机预测平均。真正可复现的定义还必须包含 mask 共享轴、placement、RNG 和分布式/重算语义。

- [[随机正则化与网络级泛化接口 MOC]]
- [[习题 - Dropout 的随机掩码、期望与 Inverted Scaling]]
- [[解答 - Dropout 的随机掩码、期望与 Inverted Scaling]]
