---
type: model
status: draft
area: [neural-networks/normalization, batch-normalization, inference]
aliases: [BatchNorm Forward, Batch Normalization Train Eval]
node_id: NN-34
prerequisites: ["[[归一化的对象、轴与不变性]]", "[[期望、方差与矩]]", "[[随机变量的收敛与大数定律]]"]
related: ["[[BatchNorm 反向传播、尺度不变性与噪声]]", "[[InstanceNorm、GroupNorm 与 WeightNorm]]", "[[小批量、混合精度、分布式与因果归一化边界]]"]
sources: ["[[S-2015-Ioffe-Szegedy-BatchNorm]]", "[[S-2018-Santurkar-BatchNorm-Optimization]]", "[[S-2026-PyTorch-Normalization-Semantics]]"]
exercises: ["[[习题 - BatchNorm 前向统计与训练—推理差异]]"]
solutions: ["[[解答 - BatchNorm 前向统计与训练—推理差异]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-batchnorm-forward-state-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# BatchNorm 前向统计与训练—推理差异

> [!abstract] 本章主问题
> BatchNorm 在训练时用当前归约组的均值与方差标准化，同时更新 running buffers；常见推理模式改用固定 buffers，因此训练图和推理图不是同一个前向算子。真正的实现合同还包括卷积归约轴、biased/unbiased variance 的分工、momentum 方向、batch companions 与可折叠的 affine 变换。

## 一、学习目标

完成本节后，你应能：

1. 对全连接与卷积输入写出 BatchNorm 的精确归约组；
2. 从原始输入计算 batch mean、biased variance、标准化输出与 affine 输出；
3. 区分当前 batch statistics、running statistics 与 population moments；
4. 写出 PyTorch 风格 running update，并解释 momentum 记号；
5. 预测同一输入在 train/eval、不同 companion batch 下为何改变；
6. 把 eval-mode Conv/Linear + BatchNorm 精确折叠成一个 affine layer；
7. 识别 $m=1$、小 batch、非 IID spatial samples 与错误 mode 的失败；
8. 把原始 ICS 动机与后来机制证据分开陈述。

## 二、对象、形状与符号

先考虑二维输入

$$
X\in\mathbb R^{N\times C}.
$$

对每个 feature/channel $c$，统计组是

$$
\mathcal B_c=\{X_{1c},\ldots,X_{Nc}\},
\qquad m=N.
$$

训练前向定义

$$
\mu_c^{(B)}=\frac1m\sum_{i=1}^m x_{ic},
$$

$$
q_c^{(B)}=\frac1m\sum_{i=1}^m(x_{ic}-\mu_c^{(B)})^2,
$$

$$
\widehat x_{ic}
=\frac{x_{ic}-\mu_c^{(B)}}{\sqrt{q_c^{(B)}+\varepsilon}},
\qquad
y_{ic}=\gamma_c\widehat x_{ic}+\beta_c.
$$

$\gamma,\beta\in\mathbb R^C$ 在 batch 轴广播。这里 $B$ 上标表示当前 mini-batch，不表示总体真值。

## 三、一个完整手算

取单一 feature 的 batch

$$
x=(1,3),\qquad \gamma=2,\qquad\beta=-1,\qquad\varepsilon=0.
$$

先算

$$
\mu_B=\frac{1+3}{2}=2,
$$

$$
q_B=\frac{(1-2)^2+(3-2)^2}{2}=1.
$$

所以

$$
\widehat x=(-1,1),
\qquad
y=2(-1,1)-1=(-3,1).
$$

检查：

$$
\operatorname{mean}(\widehat x)=0,\qquad
\operatorname{mean}(\widehat x^2)=1.
$$

若 $\varepsilon>0$，第二个等式变成 $1/(1+\varepsilon)<1$。这里还有一个容易漏掉的二维特例：当 $m=2,\varepsilon=0$ 且两值不同，无 affine 的输出恒为 $(-1,1)$ 或 $(1,-1)$，所以把 3 换成 5 并不会改变第一个标准化值；加入第三个 companion、取 $\varepsilon>0$ 或改变相等关系后，输出通常会改变。一般的 companion dependence 仍来自共享 $\mu_B,q_B$，二维常量结果只是低维退化。

## 四、为什么训练用 biased variance

训练 forward 的目标不是构造 population variance 的无偏估计，而是用同一组数据做标准化。使用

$$
q_B=\frac1m\sum_i(x_i-\mu_B)^2
$$

可在 $\varepsilon=0,q_B>0$ 时得到组内平方均值精确为 1。若改用

$$
s_B^2=\frac1{m-1}\sum_i(x_i-\mu_B)^2,
$$

则标准化后的组内 biased variance 是 $(m-1)/m$。

这不意味着 running buffer 也必须存 biased observation。以访问日 PyTorch 2.13 为例：

- 当前训练 forward 使用 correction=0；
- 更新 running variance 的当前 observation 使用 correction=1。

这是框架合同，不是由“BatchNorm”三个字自动推出的跨框架定理。

## 五、population moments、batch estimates 与 running buffers

设训练分布在当前参数下的 feature moments 为

$$
\mu_c^\star=\mathbb E[X_c],
\qquad
q_c^\star=\operatorname{Var}(X_c).
$$

它们依赖上游网络参数，训练中会漂移；每一步遍历全数据重算又太昂贵。于是实现维护 buffers：

$$
\bar\mu_c,\qquad \bar q_c.
$$

PyTorch 风格 momentum $a\in(0,1]$ 的更新是

$$
\boxed{
\bar\mu\leftarrow(1-a)\bar\mu+a\mu_B
},
$$

$$
\boxed{
\bar q\leftarrow(1-a)\bar q+a\,s_B^2
},
$$

其中 $s_B^2$ 在该实现中是 unbiased batch observation。

> [!warning] momentum 方向
> 这里 $a=0.1$ 表示“新 batch 占 0.1”，不是 optimizer 中“旧速度保留 0.1”。不同库可能把 decay 写成旧值系数，迁移配置时必须看公式。

若 momentum=None，PyTorch 使用 cumulative moving average；这仍不是“对当前模型参数下全训练分布 moments 的精确估计”，因为网络参数在历史期间持续变化。

## 六、训练前向是一个带副作用的状态变换

训练调用可以写成

$$
(Y,\bar\mu_{\text{new}},\bar q_{\text{new}})
=F_{\text{train}}(X,\bar\mu_{\text{old}},\bar q_{\text{old}};\gamma,\beta).
$$

输出 $Y$ 使用当前 $X$ 的 batch statistics；旧 buffers 通常不参与标准化，但会被更新。于是一次 forward 同时：

1. 计算激活；
2. 改变模型持久状态。

这解释了为什么：

- gradient accumulation 不等于用大 batch 做一次 BN；
- validation 若误留在 train mode 会污染 buffers；
- checkpoint 必须保存 buffers，而不仅是可训练 parameters；
- data order、last incomplete batch 与 augmentation 会影响最终 state。

## 七、推理前向

常见 eval mode 使用固定 buffers：

$$
\boxed{
y_{ic}^{\text{eval}}
=\gamma_c
\frac{x_{ic}-\bar\mu_c}{\sqrt{\bar q_c+\varepsilon}}
+\beta_c
}.
$$

此时每个样本独立，输出不再依赖同批 companions；同一输入的 train-mode 与 eval-mode 输出通常不同，因为统计量不同。

若 track_running_stats=False，PyTorch 不维护 buffers，eval 仍用当前 batch statistics。于是“调用 eval”并不自动保证 per-sample deterministic function；还要检查模块配置。

## 八、train/eval mismatch 从哪里来

定义统计差

$$
\Delta\mu_c=\mu_c^{(B)}-\bar\mu_c,
\qquad
\Delta q_c=q_c^{(B)}-\bar q_c.
$$

同一输入的差异来自

$$
\frac{x-\mu_B}{\sqrt{q_B+\varepsilon}}
\quad\text{与}\quad
\frac{x-\bar\mu}{\sqrt{\bar q+\varepsilon}}.
$$

常见原因：

- batch 太小或类别/域混合不代表部署分布；
- running momentum 与训练时长不匹配；
- fine-tuning 时冻结了 weight 却错误更新/冻结 BN state；
- 训练增强强、部署输入弱；
- distributed replicas 各自看到不同统计组；
- eval 忘记切换，或导出时丢失 buffers。

这不是一个标量“误差率”，而是每层、每 channel、随分布变化的 affine mismatch。

## 九、卷积 BatchNorm 的有效组大小

对

$$
X\in\mathbb R^{N\times C\times H\times W},
$$

固定 channel $c$，归约集合是

$$
\{X_{nchw}:1\le n\le N,\ 1\le h\le H,\ 1\le w\le W\},
$$

所以 nominal group size

$$
m=NHW.
$$

$\gamma_c,\beta_c$ 仍只有 $C$ 个。原始论文称这是 convolutional/spatial BatchNorm。

但 $NHW$ 不等于 IID effective sample size：邻近空间位置高度相关，padding/border 的分布也不同。统计 variance 的理论若使用 IID 假设，必须把这一点标为近似。

## 十、$m=1$ 与零方差

若组内只有一个标量，

$$
\mu_B=x_1,\qquad q_B=0,\qquad\widehat x_1=0.
$$

训练输出只剩 $\beta$，当前输入信息被删除。某些实现还会拒绝“每 channel 只有一个 value”的训练调用，因为 variance/update 无法提供所需语义。

卷积中 batch size $N=1$ 不必然意味着 $m=1$；只要 $HW>1$，仍有多个 spatial values，但它们的相关性和任务适用性要另审计。

## 十一、Linear/Conv 后的 bias 为什么常可省

若 preactivation

$$
z_i=w^{\mathsf T}x_i+b
$$

且 $b$ 对同一统计组所有元素相同，那么

$$
z_i-\mu_z
=w^{\mathsf T}x_i+b-(w^{\mathsf T}\mu_x+b)
=w^{\mathsf T}(x_i-\mu_x).
$$

训练 batch centering 消除了 $b$；后续 $\beta$ 已提供平移参数。因此 Conv/Linear 紧接 BN 时，前者 bias 常设为 false。

边界：若 affine=False、归约组不共享该 bias、BN 被旁路/折叠配置不同，或计算图还有其他消费者，这个删除不能机械执行。

## 十二、推理时折叠 BatchNorm

eval mode 的 BN 是固定 affine map。设前层

$$
z=Wx+b,
$$

逐输出 channel 定义

$$
a_c=\frac{\gamma_c}{\sqrt{\bar q_c+\varepsilon}}.
$$

则

$$
y_c=a_c(z_c-\bar\mu_c)+\beta_c
=a_cW_cx+\left[a_c(b_c-\bar\mu_c)+\beta_c\right].
$$

所以可折叠为

$$
\boxed{
W_c'=a_cW_c,\qquad
b_c'=a_c(b_c-\bar\mu_c)+\beta_c
}.
$$

若原层无 bias，取 $b_c=0$。折叠只对固定 eval statistics 成立；train-mode BN 依赖当前 batch，不能折叠为单样本 affine layer。

## 十三、BatchNorm 是否“让分布变成标准正态”

不会。它只控制组内一阶、二阶统计量：

- skewness、kurtosis、multimodality 仍可存在；
- features/channel 之间 covariance 未被白化；
- $\gamma,\beta$ 会重新改变 mean/scale；
- train/eval 使用的统计源不同；
- 同一 feature 的 batch empirical distribution 不是总体分布。

“normalization”不是“Gaussianization”，更不是 decorrelation。

## 十四、机制解释的证据分层

### 14.1 历史动机

Ioffe–Szegedy 以 internal covariate shift 解释 BN：上游参数更新使层输入分布变化，固定 moments 有助后续层学习。

### 14.2 后续挑战

Santurkar et al. 的 noisy-BN 实验显示，即使主动制造更强的一阶/二阶分布漂移，BN 的训练收益仍可保留；论文进一步观察沿 gradient direction 的 loss/gradient 更平滑、更可预测。

### 14.3 当前课程判断

以下是不同等级的陈述：

- **定义**：BN 用组统计量标准化，并在常见实现中有 train/eval 双语义；
- **精确性质**：它产生 batch coupling、若 $\varepsilon=0$ 则有正尺度不变性；
- **已观察机制**：允许更大学习率、带来 batch-dependent stochasticity、改变优化几何；
- **未封闭问题**：哪种机制在给定架构/optimizer/数据上占主导。

不能把某一种解释写成跨模型唯一因果。

## 十五、图：训练状态、推理状态与可折叠路径

先看图回答：训练输出使用哪一组 statistics，running buffers 在何时更新，为什么 eval path 能折叠进 Conv/Linear 而 train path 不能？

![[00-知识库管理/_assets/figures/neural-networks/fig-batchnorm-forward-state-v2.svg|900]]

> [!figure] 图 30.5-02　BatchNorm 的当前批统计、持久状态与推理折叠
> 左栏把 $(N,C,H,W)$ 的每 channel 归约组标成 $(N,H,W)$；中栏分开训练路径的 current batch normalization 与 running-state update，并对比 evaluation 的 fixed-state path；右栏从 $z=Wx+b$ 推到 $W',b'$ 的固定 affine 折叠，同时列出 estimator、momentum 和 mode 三个实现检查点。来源：依据 Ioffe–Szegedy 2015 与 PyTorch 2.13 BatchNorm2d 文档独立绘制；由 [[00-知识库管理/_labs/code/plot_normalization_foundations_v2.py]] 确定性生成。

**怎样读图**：先沿蓝色数据流看本次输出真正使用的统计量，再沿绿色状态流看 buffers 如何演化；只有右侧 eval 分支中 statistics 固定，才能把两层代数合并。

**图没有证明什么**：图没有证明 running statistics 等于部署总体 moments，也没有证明更大 nominal group 必然估计更准；spatial correlation、domain shift、distributed grouping 与有限精度仍需单独测量。

## 十六、最小实现与测试合同

一个可审计的 BatchNorm 前向实现应显式保存：

1. reduction axes；
2. forward variance correction；
3. running variance observation correction；
4. epsilon 与 accumulation dtype；
5. momentum 的新旧值系数；
6. training 与 track-running-stats；
7. affine 参数和 buffer shape。

最小测试包括：

- 手算 batch 与实现逐元素一致；
- 每 channel 的 affine 前 mean/energy 检查；
- 固定输入换 companion 后 train 输出改变；
- eval 输出不随 companion 改变；
- 保存—加载后 buffers 一致；
- folding 前后 eval 输出在容差内一致；
- $q=0$、$m=1$、极大值与低精度不产生未说明行为。

> [!summary]
> BatchNorm 不是一行无状态公式，而是“当前批归约 + affine 参数 + running-state 更新 + mode 切换”的模块。训练与推理的统计来源不同；只有固定 eval statistics 才能折叠成普通 affine map。

- [[归一化、尺度与统计量 MOC]]
- [[习题 - BatchNorm 前向统计与训练—推理差异]]
- [[解答 - BatchNorm 前向统计与训练—推理差异]]
