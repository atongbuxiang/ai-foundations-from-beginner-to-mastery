---
type: comparison
status: draft
area: [neural-networks/regularization, dropconnect, weight-noise, activation-noise, stochastic-estimators]
aliases: [Noise Injection by Location, DropConnect and Activation Noise]
node_id: NN-59
prerequisites: ["[[Dropout 的随机掩码、期望与 Inverted Scaling]]", "[[期望、方差与矩]]", "[[线性层与仿射层的反向传播]]", "[[随机梯度与小批量估计]]"]
related: ["[[Dropout 的方差、共适应解释与 Bayesian 边界]]", "[[数据增强、不变性、等变性与任务充分性]]", "[[随机、对抗与自适应序列的区别]]", "[[参数对称性、等价表示与可辨识边界]]"]
sources: ["[[S-2013-Wan-DropConnect]]", "[[S-1995-Bishop-Training-with-Noise]]", "[[S-2015-Kingma-Variational-Dropout]]", "[[S-2013-Wager-Dropout-Adaptive-Regularization]]", "[[S-2026-PyTorch-Dropout-Stochastic-Depth]]"]
exercises: ["[[习题 - DropConnect、权重噪声与激活噪声]]"]
solutions: ["[[解答 - DropConnect、权重噪声与激活噪声]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-noise-location-output-covariance-v2.svg]]"
created: 2026-08-24
updated: 2026-08-29
---

# DropConnect、权重噪声与激活噪声

> [!abstract] 本章主问题
> 噪声“加在哪里”决定随机函数、联合分布、梯度、诱导正则项和系统成本。Activation Dropout 对输入 features 采 mask；DropConnect 对 weight entries 采 mask；additive/multiplicative weight noise、activation noise 和 gradient masking 又是不同合同。即使几种方法保持相同 preactivation 均值、甚至匹配每个输出的边际方差，它们的跨输出/跨样本 covariance 和优化轨迹仍可不同。

## 课程位置与两遍学习路线

- **承接什么：** NN-57—58 已算出共享 feature mask 对两个 output scores 产生的均值、边际方差与 cross-output covariance；
- **本页解决什么：** 把随机变量移到 activation、connection、weight 或 gradient，构造“边际矩相同但联合分布不同”的严格反例；
- **后续为何需要：** DropPath 会把 gate 再提升到整个 residual branch，比较前必须掌握 noise location 与 sharing axes 决定 covariance 的原则。

**第一遍只比较 Activation Dropout 与 DropConnect。** 使用同一 $x,W,q$，匹配每个 output 的均值和方差，再计算 cross-output covariance 找到差异。

**第二遍再扩展噪声族。** 区分 additive/multiplicative、global/local、per-example/shared-batch、forward corruption/gradient masking，并检查 induced penalty 与 kernel 成本。

### 问题链

1. Activation Dropout 与 DropConnect 分别给哪些对象采样 Bernoulli mask？
2. 两者为何能匹配每个 output 的均值与方差，却不匹配 joint covariance？
3. global weight noise 与 local reparameterized activation noise 在单样本边际相同后，还改变了什么 batch-level joint law？
4. forward noise 的 expected objective 与 gradient masking 的 update estimator 为什么不是同一对象？
5. mask 中有很多零，为什么 dense kernel 的实际 FLOPs 未必减少？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal D_\square$ 上算出 $\Sigma_{\mathrm{act}}=\left[\begin{smallmatrix}8&-2\\-2&5\end{smallmatrix}\right]$ 与 $\Sigma_{\mathrm{dc}}=\operatorname{diag}(8,5)$，并指出唯一改变的是 mask sharing structure，就已掌握本页主干。

## 符号与对象账本

| 方法 | 随机对象 | sharing axes | 典型梯度影响 |
|---|---|---|---|
| Activation Dropout | input/features $M\odot x/q$ | 同 feature mask 可被所有 output rows 共享 | gate input VJP 与 weight columns |
| DropConnect | entries $M\odot W/q$ | 通常 connection 独立 | gate weight entries 与 input paths |
| additive weight noise | $W+\varepsilon$ | global batch 或 local sample | noise-shaped parameter gradient |
| multiplicative weight noise | $W\odot(1+\varepsilon)$ | scale 随 weight | 零/小 weight 的噪声不同 |
| local reparameterization | preactivation samples | 常按 example 独立 | 保边际、改 batch joint law |
| gradient masking | optimizer update | 坐标/sample/step | 未必对应 forward-corrupted risk |

### 贯穿算例 $\mathcal D_\square$：相同边际矩，不同联合输出

沿用

$$
x=(2,1)^{\mathsf T},
\qquad
W=\begin{bmatrix}1&2\\-1&1\end{bmatrix},
\qquad q=\frac12.
$$

无噪声输出为

$$
Wx=(4,-1)^{\mathsf T}.
$$

Activation Dropout 在两个 output rows 间共享 feature masks，因此

$$
\boxed{
\mathbb E z_{\mathrm{act}}=(4,-1),
\qquad
\Sigma_{\mathrm{act}}
=\begin{bmatrix}8&-2\\-2&5\end{bmatrix}
}.
$$

若 DropConnect 的四个 connection masks 独立，则每个 output 的 mean/variance 保持相同，但跨 row covariance 消失：

$$
\boxed{
\mathbb E z_{\mathrm{dc}}=(4,-1),
\qquad
\Sigma_{\mathrm{dc}}
=\begin{bmatrix}8&0\\0&5\end{bmatrix}
}.
$$

二者 covariance determinants 也不同：

$$
\det\Sigma_{\mathrm{act}}=36,
\qquad
\det\Sigma_{\mathrm{dc}}=40.
$$

所以相同 coordinate-wise moments 不能推出经过 Softmax、normalization 或 nonlinear loss 后的分布相同。

## 核心公式七问：Noise-Location Contract

$$
\boxed{
(\text{location},\text{law},\text{sharing axes},\text{scaling},\text{gradient},\text{system})
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 定义一个可比较、可复现的 noise injection 方法 |
| 对象 | activation、weight、connection、preactivation 或 update |
| 来路 | 相同 noise magnitude 在计算图不同位置诱导不同随机函数 |
| 步骤 | 标位置→写随机 law→写共享轴→匹配 moments→推 VJP→测 kernel/communication |
| 读法 | variance 只是边际摘要，sharing axes 决定 covariance 和 batch coupling |
| 检查 | exact enumeration、covariance、fixed-seed VJP、local/global ablation 与 profiler |
| 去路 | variational dropout、parameter noise、quantization noise 与 stochastic optimizers |

### AI / 系统对应

分布式训练中，weight noise 若在 rank 间独立，会让 replicas 优化不同随机参数；若同步，又增加通信或 RNG 合同。Activation noise 通常不减少 GEMM，DropConnect 的零 entries 也只有在结构化稀疏 kernel 中才可能省算力。统计稀疏与系统加速必须分别验收。

## 一、学习目标

读完本节，你应能：

1. 用统一线性层写出 activation、weight 与 connection noise；
2. 区分 additive 与 multiplicative、global 与 local、shared 与 independent noise；
3. 推导 Activation Dropout 与 DropConnect 的前向均值/方差；
4. 用二维例子计算两者不同的 output covariance；
5. 推导两种 Bernoulli noise 的 VJP/参数梯度；
6. 用二阶 Taylor 展开解释 noise-induced penalty 的位置依赖；
7. 解释 local reparameterization 保持什么、改变什么；
8. 区分 forward noise 与 gradient masking；
9. 审计随机 mask 的存储、通信、kernel 与真实 FLOP；
10. 设计 matched-moment、matched-quality 与 natural protocol。

## 二、统一基准：无噪声线性层

令

$$
x\in\mathbb R^{d_{\rm in}},
\qquad
W\in\mathbb R^{d_{\rm out}\times d_{\rm in}},
\qquad
b\in\mathbb R^{d_{\rm out}}.
$$

基准 preactivation：

$$
z=Wx+b.
$$

比较噪声方法时，应固定或记录：

$$
(\text{random object},\text{law},\text{scale},
\text{shared axes},\text{placement},\text{state}).
$$

只给一个“noise std”或“drop rate”不足以定义随机网络。

## 三、Activation Dropout

令 feature mask

$$
m_j\overset{\mathrm{iid}}\sim\operatorname{Bernoulli}(q),
$$

并定义

$$
\widetilde x=\frac mq\odot x.
$$

于是

$$
\boxed{
z^{\rm act}=W\widetilde x+b
}.
$$

条件于 $x$：

$$
\mathbb E[z_i^{\rm act}\mid x]
=(Wx+b)_i,
$$

$$
\operatorname{Var}(z_i^{\rm act}\mid x)
=\frac pq\sum_jW_{ij}^2x_j^2.
$$

同一个 $m_j$ 同时影响所有输出 rows，所以

$$
\boxed{
\operatorname{Cov}(z_i^{\rm act},z_k^{\rm act}\mid x)
=\frac pq\sum_jW_{ij}W_{kj}x_j^2
}.
$$

因此 activation masks 通过共享 input features 耦合不同 output units。

## 四、DropConnect

令每个 connection 有独立 mask：

$$
M_{ij}\overset{\mathrm{iid}}\sim\operatorname{Bernoulli}(q_w).
$$

Inverted DropConnect 写成

$$
\widetilde W=\frac M{q_w}\odot W,
$$

$$
\boxed{
z^{\rm dc}=\widetilde W x+b
}.
$$

条件均值同样保持：

$$
\mathbb E[z_i^{\rm dc}\mid x]=W_{i:}x+b_i.
$$

每个输出的方差为

$$
\operatorname{Var}(z_i^{\rm dc}\mid x)
=\frac{1-q_w}{q_w}\sum_jW_{ij}^2x_j^2.
$$

若不同 rows 的 $M_{ij}$ 独立，则对 $i\ne k$：

$$
\boxed{
\operatorname{Cov}(z_i^{\rm dc},z_k^{\rm dc}\mid x)=0
}.
$$

所以当 $q_w=q$ 时，两个方法可以匹配每个输出的条件均值与边际方差，却不匹配 output joint law。

## 五、完整手算：相同边际方差，不同 Covariance

取

$$
W=
\begin{bmatrix}
1&2\\
-1&1
\end{bmatrix},
\qquad
x=
\begin{bmatrix}
2\\1
\end{bmatrix},
\qquad q=0.5.
$$

无噪声输出：

$$
Wx=
\begin{bmatrix}
4\\-1
\end{bmatrix}.
$$

### 5.1 Activation Dropout 枚举

四个等概率 feature masks 产生：

| $m$ | $\widetilde x$ | $z=W\widetilde x$ |
|---|---|---|
| $(0,0)$ | $(0,0)$ | $(0,0)$ |
| $(1,0)$ | $(4,0)$ | $(4,-4)$ |
| $(0,1)$ | $(0,2)$ | $(4,2)$ |
| $(1,1)$ | $(4,2)$ | $(8,-2)$ |

平均为

$$
\mathbb E[z]=(4,-1).
$$

由公式

$$
\operatorname{Var}(z_1)=1^2(2^2)+2^2(1^2)=8,
$$

$$
\operatorname{Var}(z_2)=(-1)^2(2^2)+1^2(1^2)=5,
$$

$$
\operatorname{Cov}(z_1,z_2)
=1(-1)(2^2)+2(1)(1^2)
=-2.
$$

所以

$$
\boxed{
\Sigma_{\rm act}=
\begin{bmatrix}
8&-2\\-2&5
\end{bmatrix}
}.
$$

### 5.2 独立 DropConnect

每个 row 的 connection masks 独立，diagonal variances 仍是 8 与 5，但 cross-row covariance 为 0：

$$
\boxed{
\Sigma_{\rm dc}=
\begin{bmatrix}
8&0\\0&5
\end{bmatrix}
}.
$$

这给出一个严格反例：相同均值、相同每坐标方差，不推出相同 multivariate distribution，也不推出经过 Softmax/normalization 后相同。

## 六、Activation Dropout 的反向传播

令上游列梯度

$$
\delta=\nabla_z\mathcal L.
$$

前向为

$$
z=W\left(\frac mq\odot x\right)+b.
$$

因此

$$
\boxed{
\nabla_W\mathcal L
=\delta\left(\frac mq\odot x\right)^\mathsf T
},
$$

$$
\boxed{
\nabla_x\mathcal L
=\frac mq\odot(W^\mathsf T\delta)
},
$$

$$
\nabla_b\mathcal L=\delta.
$$

同一个 feature mask 门控 $x$ 的输入梯度，也从右侧门控 $W$ 的 gradient columns。

## 七、DropConnect 的反向传播

前向：

$$
z=\left(\frac M{q_w}\odot W\right)x+b.
$$

对原参数 $W$：

$$
\boxed{
\nabla_W\mathcal L
=\frac M{q_w}\odot(\delta x^\mathsf T)
}.
$$

对输入：

$$
\boxed{
\nabla_x\mathcal L
=\left(\frac M{q_w}\odot W\right)^\mathsf T\delta
}.
$$

被 drop 的 weight entry 本次 data-gradient 为零；但 decoupled weight decay、optimizer state update 或其他 batch masks 仍可能改变它。必须区分“data path gradient 为零”和“Parameter update 为零”。

## 八、Additive Weight Noise

令

$$
\widetilde W=W+\sigma_W E,
\qquad
\mathbb E[E]=0.
$$

前向

$$
z=(W+\sigma_WE)x+b.
$$

若 $E_{ij}$ 独立、方差 1：

$$
\mathbb E[z\mid x]=Wx+b,
$$

$$
\operatorname{Var}(z_i\mid x)
=\sigma_W^2\|x\|_2^2.
$$

它是 additive、与 $W_{ij}$ 大小无关的扰动；DropConnect 的 variance 则乘 $W_{ij}^2$。因此两者的 signal-to-noise ratio、零权重行为和 scale symmetry不同。

对某次 $E$ realization，

$$
\nabla_W\mathcal L=\delta x^\mathsf T
$$

的形式看似无 mask，但 $\delta$ 是在 noisy forward 上计算的，仍依赖 $E$。不能从局部 outer-product 形状推出优化轨迹与无噪声相同。

## 九、Additive Activation Noise

令

$$
\widetilde x=x+\sigma_x\varepsilon,
\qquad
\mathbb E[\varepsilon]=0,
\qquad
\operatorname{Cov}(\varepsilon)=I.
$$

则

$$
z=W\widetilde x+b,
$$

$$
\operatorname{Cov}(z\mid x)
=\sigma_x^2WW^\mathsf T.
$$

它天然产生跨输出 covariance。若 noise scale 随 $x$ 或 channel 改变，covariance 再相应变化。Gaussian、uniform、quantization-like noise 即使方差相同，也可能因尾部和高阶矩在非线性网络中表现不同。

## 十、Multiplicative Gaussian Noise

另一种写法是

$$
\widetilde x_i=x_i(1+\alpha\varepsilon_i),
\qquad
\varepsilon_i\sim\mathcal N(0,1).
$$

于是

$$
\mathbb E[\widetilde x_i\mid x_i]=x_i,
$$

$$
\operatorname{Var}(\widetilde x_i\mid x_i)=\alpha^2x_i^2.
$$

它可在一、二阶矩上与某个 Bernoulli Dropout rate 匹配：

$$
\alpha^2=\frac pq.
$$

但 Bernoulli 有 point mass at zero，Gaussian 没有；高阶矩、稀疏性和 nonlinear response 不同。Moment matching 不是 distribution equality。

## 十一、Noise-Induced Penalty 依赖扰动位置

设被扰动对象为 $u$，noise 为零均值 $\varepsilon$。小噪声 Taylor 展开：

$$
\ell(u+\varepsilon)
\approx
\ell(u)
+\nabla\ell(u)^\mathsf T\varepsilon
+\frac12\varepsilon^\mathsf T
H_u\ell(u)\varepsilon.
$$

取期望：

$$
\boxed{
\mathbb E\ell(u+\varepsilon)
\approx
\ell(u)
+\frac12\operatorname{tr}(H_u\ell\,\Sigma_\varepsilon)
}.
$$

若 $u=x$，出现 input/activation sensitivity；若 $u=W$，出现 parameter-space curvature；若扰动 preactivation，则是另一 Hessian。Bishop 的输入噪声—Tikhonov 联系在特定平方误差/小噪声条件下可化为 Jacobian penalty；不能据此称所有 weight noise 都等价同一个正则项。

## 十二、Local Reparameterization 改变 Estimator，而不只是代码位置

对 Gaussian weight posterior/noise，线性层每个样本的 preactivation moments 可能可解析。可从

$$
W^{(s)}\to z_n^{(s)}=W^{(s)}x_n
$$

的 global weight sample，改成直接为每个 datapoint 采

$$
z_n\sim\mathcal N(\mu_z(x_n),\Sigma_z(x_n)).
$$

在论文条件下，每个 datapoint 的 marginal expected loss 保持，且 local independent noise 可降低 minibatch gradient estimator variance。

但完整 joint law 改变：global $W^{(s)}$ 在 batch samples 间共享，local $z_n$ 通常独立。若 loss 含跨样本 coupling，例如 BatchNorm、contrastive denominator、batch covariance 或 ranking pairs，不能只凭单样本 marginal 直接替换。

## 十三、Forward Noise 不等于 Gradient Masking

Forward corruption 定义随机 loss

$$
\mathcal L(\theta;\xi),
$$

其正确 stochastic gradient 是

$$
\nabla_\theta\mathcal L(\theta;\xi).
$$

而先计算 clean gradient 再做

$$
\widetilde g=r\odot g
$$

通常不是某个 forward-corrupted expected risk 的梯度。它改变 optimizer update estimator、坐标采样和 noise covariance，但不定义同一个 predictor family。

因此 activation Dropout、DropConnect 与 gradient Dropout/ChildTuning 类方法必须分别命名，不能因都有 Bernoulli mask 就合并。

## 十四、共享轴与跨样本相关性

Weight noise 可选择：

- 整个 minibatch 共享一张 $\widetilde W$；
- 每个样本独立 $\widetilde W_n$；
- 每个 sequence/time step 重采；
- 每个 optimizer step 固定；
- 在 gradient accumulation microbatches 间重采或复用。

这些选择决定：

- batch gradient variance 是否随 batch size 下降；
- samples 是否看到同一随机模型；
- normalization/contrastive loss 的 joint distribution；
- random seed 与 distributed reproducibility；
- mask storage 和通信。

“每步采一次 weight noise”必须回答“每个什么步、共享给谁”。

## 十五、系统成本：随机稀疏不等于稀疏加速

### Activation Noise

通常可与 elementwise kernel 融合，但仍需要 RNG、mask/seed 保存和 memory traffic。Channel/token masks 较小，但广播语义不同。

### DropConnect

若真的物化与 dense $W$ 同 shape 的随机 mask：

- RNG 数量为 $O(d_{\rm out}d_{\rm in})$；
- mask/storage 与 weight 同阶；
- unstructured zeros 未必被 dense GEMM 利用；
- 分片参数要定义 mask ownership；
- backward 还需复用 mask。

“50% weights 为零”不等于 FLOP 减半；除非 kernel/结构稀疏真正跳过乘加。

### Additive Noise

可在线生成或融合，但 parameter-noise QAT/variational methods 可能保留额外 mean/variance 参数和 optimizer state。

## 十六、公平比较的三条轨道

### Matched-Moment

让不同 noise methods 的 preactivation mean 与 diagonal variance 尽量匹配，用来暴露 covariance/高阶矩差异。

### Matched-Quality

分别调 rate/std 到相同 validation NLL，再比较吞吐、稳定性、calibration 与鲁棒性。

### Natural Protocol

各方法使用推荐 sampling granularity、rate 与实现，比较真实 Pareto frontier。

三条都应报告：

- clean/noisy train loss；
- held-out NLL/accuracy/calibration；
- output covariance 与 gradient variance；
- 参数/状态/mask bytes；
- achieved FLOP/s、memory bandwidth、wall time；
- 多 seed 与 frequency/group metrics；
- deterministic 与 MC inference 语义。

## 十七、常见误区

1. **“噪声方差相同，所以方法相同”**：joint covariance 和高阶矩可不同；
2. **“DropConnect 就是把输入 Dropout 换个写法”**：mask 共享轴不同；
3. **“被 mask 权重本步不会更新”**：decay/optimizer 仍可能改变；
4. **“Gaussian 与 Bernoulli 二阶矩匹配就完全等价”**：point mass/tails 不同；
5. **“Local reparameterization 保持完整 batch joint law”**：通常只保持所需 marginals/expected sum-loss；
6. **“Gradient masking 是 forward Dropout 的反向”**：一般目标不同；
7. **“随机 50% 零权重就快两倍”**：dense kernel 不会自动跳过；
8. **“噪声都等价 $L_2$”**：位置、loss、curvature 与展开条件决定 penalty。

## 十八、图：Noise Location 与 Covariance

先看图回答：为什么 activation mask 与 DropConnect 能有同样的 diagonal variance，却得到 $-2$ 与 0 的 cross-output covariance？右栏为什么把 objective、estimator 和 runtime 分成三本账？

![[00-知识库管理/_assets/figures/neural-networks/fig-noise-location-output-covariance-v2.svg|900]]

> [!figure] 图 30.8-03　Activation noise、DropConnect 与 additive noise 的位置合同和 output covariance 反例
> 左栏写出三种随机对象；中栏用 $W=\begin{bmatrix}1&2\\-1&1\end{bmatrix}$、$x=(2,1)$、$q=0.5$ 比较共享 feature mask 与独立 connection masks；右栏分离 expected objective、gradient estimator 与实际 kernel。来源：依据 Wan et al.、Bishop、Kingma et al. 与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_random_regularization_foundations_v2.py]] 确定性生成。

**怎样读图**：先定位随机变量，再核对 mask 在哪些 axes 共享；接着比较完整 covariance 而非只看 diagonal；最后分别问优化的是哪个 expected loss、用哪个 estimator、运行哪个 kernel。

**图没有证明什么**：图不证明某种 noise universally 更好，不证明 covariance 是全部任务差异，也不证明 unstructured zeros 会带来硬件加速。

## 十九、最小验收

1. 写出三类 noise 的前向对象与 shape；
2. 推导 Activation Dropout 的 output covariance；
3. 推导独立 DropConnect 的 covariance；
4. 复算二维 toy 的两个矩阵；
5. 推导两种 Bernoulli noise 的 $W,x$ gradients；
6. 比较 additive/multiplicative moments；
7. 写出 small-noise Taylor penalty；
8. 解释 local reparameterization 的 marginal/joint 边界；
9. 区分 forward noise 与 gradient masking；
10. 设计 matched-moment、matched-quality 与 natural 三轨验收。

> [!summary]
> Noise injection 的本体是随机变量在计算图中的位置与共享结构。Activation Dropout 对 features 采样，DropConnect 对 connections 采样，additive/multiplicative noise 又有不同尺度和尾部；相同均值/边际方差不保证相同 covariance、梯度或 nonlinear predictor。理论比较要声明 expected objective 与 estimator，系统比较还要验证 mask 是否真正被 kernel 利用。

- [[随机正则化与网络级泛化接口 MOC]]
- [[习题 - DropConnect、权重噪声与激活噪声]]
- [[解答 - DropConnect、权重噪声与激活噪声]]
