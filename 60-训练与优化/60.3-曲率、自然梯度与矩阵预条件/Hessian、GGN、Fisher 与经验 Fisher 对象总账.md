---
type: derivation
status: verified
area: [training, optimization, curvature]
node_id: TRN-17
aliases: [曲率对象总账, Hessian GGN Fisher 对照]
prerequisites: ["[[Hessian、二阶微分与曲率]]", "[[Newton 法、Gauss-Newton 与拟 Newton 法]]", "[[条件概率、全概率与 Bayes 公式]]"]
related: ["[[GGN、经验 Fisher 与曲率近似陷阱]]", "[[自然梯度、KL 局部几何与坐标不变性]]", "[[K-FAC、Kronecker 分块与阻尼合同]]"]
sources: ["[[S-2020-Martens-Natural-Gradient-Curvature]]", "[[S-2019-Kunstner-Empirical-Fisher]]", "[[S-2024-Su-10588-Hessian近似与自适应学习率]]"]
exercises: ["[[习题 - Hessian、GGN、Fisher 与经验 Fisher 对象总账]]"]
solutions: ["[[解答 - Hessian、GGN、Fisher 与经验 Fisher 对象总账]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-curvature-object-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Hessian、GGN、Fisher 与经验 Fisher 对象总账

> [!abstract] 一句话结论
> 四种矩阵可能 shape 相同，却由不同随机变量、不同求导对象和不同期望构成：Hessian 是训练目标的二阶导；GGN 保留输出 loss 曲率并丢掉模型的二阶导项；true Fisher 对模型自身预测分布的 score 取协方差；empirical Fisher 对观测标签的样本 gradient 做 outer product。只有写清模型、标签来源和期望测度，才能讨论它们何时相等。

## 一、先锁定共同计算图

设输入 $x$ 经模型得到输出坐标

$$
z=f_\theta(x)\in\mathbb R^K,
$$

单样本 loss 为 $\ell(z,y)$，训练目标

$$
L(\theta)=\mathbb E_{(x,y)\sim q_{data}}[\ell(f_\theta(x),y)].
$$

定义模型 Jacobian $J_\theta(x)=\partial z/\partial\theta\in\mathbb R^{K\times P}$。以下所有矩阵均作用在 $P$ 维参数切空间，但“都在 $\mathbb R^{P\times P}$”绝不表示对象相同。

> [!warning] 三个不可省略的问题
> 1. 对谁求导：训练 objective、输出 loss 还是 log likelihood？
> 2. 对谁取期望：数据标签 $q(y\mid x)$ 还是模型标签 $p_\theta(y\mid x)$？
> 3. 计算的是 full population、finite dataset、mini-batch 还是单样本估计？

## 二、Hessian：真实目标的二阶局部模型

$$
H(\theta)=\nabla_\theta^2L(\theta).
$$

若正则条件允许交换期望与求导，$H$ 是样本 Hessian 的数据期望。对任意方向 $v$，二阶 Taylor 模型为

$$
L(\theta+v)\approx L(\theta)+g^Tv+\frac12v^THv.
$$

Hessian 对称，但不保证 PSD。负特征值表示该点的局部 quadratic model 沿某方向向下弯；零特征值可能来自过参数化、symmetry、flat direction 或局部退化。

## 三、Hessian 的链式分解与 GGN

对单样本应用二阶链式法则：

$$
\nabla_\theta^2\ell
=J^TH_z\ell J
+\sum_{k=1}^K\frac{\partial\ell}{\partial z_k}\nabla_\theta^2 f_{\theta,k}(x).
$$

第一项只需要模型的一阶 Jacobian 与输出 loss 的 Hessian；第二项包含模型关于参数的二阶导。Generalized Gauss–Newton matrix 定义为

$$
G=\mathbb E_{q_{data}}[J^TH_z\ell J].
$$

若 $H_z\ell\succeq0$，则对任意 $v$，

$$
v^TGv=\mathbb E[(Jv)^TH_z\ell(Jv)]\ge0,
$$

所以 GGN 为 PSD。它不是凭空“把 Hessian 变正”，而是有意识地删掉模型二阶项。

### 3.1 何时 $H=G$

- 模型对参数为线性，$\nabla_\theta^2f_k=0$；
- 或在某点输出梯度 $\nabla_z\ell=0$；
- 或遗漏项在指定期望下抵消。

一般非线性网络远离驻点时不能假设相等。

## 四、True Fisher：模型分布的 score covariance

若模型定义条件分布 $p_\theta(y\mid x)$，score 为

$$
s_\theta(x,y)=\nabla_\theta\log p_\theta(y\mid x).
$$

给定输入测度 $q(x)$，true Fisher 是

$$
F(\theta)=\mathbb E_{x\sim q(x)}
\mathbb E_{y\sim p_\theta(\cdot\mid x)}[ss^T].
$$

它显然 PSD。在支持集不随参数改变、可交换积分求导等 regularity 条件下，score 均值为零：

$$
\mathbb E_{p_\theta}[s]
=\nabla_\theta\int p_\theta(y\mid x)dy=0,
$$

并有 information identity

$$
F=-\mathbb E_{p_\theta}[\nabla_\theta^2\log p_\theta(y\mid x)].
$$

这里的标签是从当前模型采样，而不是直接使用数据集中观察到的 $y_n$。

## 五、Empirical Fisher：数据标签 gradient 的二阶原始矩

常见 finite-data 定义为

$$
F_{emp}=\frac1N\sum_{n=1}^N
g_ng_n^T,\qquad
g_n=\nabla_\theta[-\log p_\theta(y_n\mid x_n)].
$$

它也 PSD，但其 population 版本是随机梯度的 non-central second moment：

$$
\mathbb E[gg^T]
=\operatorname{Cov}(g)+\mathbb E[g]\mathbb E[g]^T.
$$

这可携带 gradient-noise 信息，却不自动等于 true Fisher，更不自动等于 Hessian。把 batch-mean gradient 做一次 outer product又是另一个对象：

$$
\bar g_B\bar g_B^T
\ne \frac1B\sum_{i=1}^Bg_ig_i^T.
$$

左边含所有样本交叉项，rank 至多 1；右边是 per-sample outer products 的平均。

## 六、四对象对照表

| 对象 | 定义来源 | PSD？ | label 来源 | 典型 rank 限制 |
|---|---|---|---|---|
| Hessian $H$ | objective 二阶导 | 不一定 | data objective | 无简单 sample-rank 上界 |
| GGN $G$ | $J^TH_z\ell J$ | 输出 loss convex 时是 | data pairs | 每样本至多 $\operatorname{rank}(J)$ |
| Fisher $F$ | model score covariance | 是 | $y\sim p_\theta$ | 受 score span 限制 |
| empirical Fisher $F_{emp}$ | observed-label gradients outer product | 是 | $y\sim q_{data}$ | finite sample 至多 $N$ |

### 6.1 常见相等条件

1. 若 NLL 的输出分布是以 $z$ 为 natural parameter 的指数族，true Fisher 与相应 GGN 可相等；
2. 若模型正确指定且在合适 population optimum，expected data Hessian 与 Fisher 可相等；
3. empirical Fisher 还需观测标签分布接近模型分布、足够数据和适当极限，才可能接近 true Fisher；
4. “在某点相等”不表示沿整条训练轨迹相等，也不表示 mini-batch estimators 相同。

## 七、最小 logistic 数值例

令 $p_\theta(y=1\mid x)=\sigma(\theta x)$，单样本 NLL。其 gradient 与 Hessian 为

$$
g=(p-y)x,\qquad H=p(1-p)x^2.
$$

模型对 logit 是线性的，所以 $H=G$；true Fisher 对 $y\sim\operatorname{Bernoulli}(p)$ 取期望也为 $p(1-p)x^2$。

取 $p=.8,x=2$：

$$
H=G=F=.8(.2)4=.64.
$$

但 empirical Fisher 对一个固定标签：

- $y=1$：$F_{emp}=(-.2\cdot2)^2=.16$；
- $y=0$：$F_{emp}=(.8\cdot2)^2=2.56$。

同一模型、同一参数、同一输入，只改 observed label，empirical Fisher 就可比 true Fisher 小 4 倍或大 4 倍。

## 八、科学空间的 Hessian proxy 该放哪里

[[S-2024-Su-10588-Hessian近似与自适应学习率]]从近最优线性化

$$
g\approx H_*(\theta-\theta^*)
$$

出发，并在轨迹协方差近各向同性时得到 $\mathbb E[gg^T]\approx\sigma^2H_*^2$。这解释了 gradient second moment 何时携带 curvature scale，但对象更接近训练轨迹的 gradient outer product；它不把 Adam $v_t$ 变成 $H$、GGN 或 $F$。

## 九、图：四个同 shape 矩阵的生成路径

先看图回答：标签从 data 还是 model 来？模型二阶项在哪条路径被删除？

![[00-知识库管理/_assets/figures/training-optimization/fig-curvature-object-ledger-v1.svg|900]]

> [!figure] 图 TRN-17　Hessian、GGN、Fisher、empirical Fisher 对象总账
> 图从共同计算图分出 objective second derivative、output-curvature pullback、model-score expectation 与 observed-label outer product，并在右侧列 PSD、期望测度与相等条件。来源：依据 [[S-2020-Martens-Natural-Gradient-Curvature]] 与 [[S-2019-Kunstner-Empirical-Fisher]] 独立绘制。

**怎样读图**：不要从矩阵名字出发，沿箭头回到随机变量与测度；只有两条路径的每个对象都对齐时才写等号。

**图没有证明什么**：图不判断哪一种预条件器在特定网络最好，也不把 PSD 当成“更接近真实 Hessian”的充分条件。

## 十、本节出口

你应能从一段代码回答：它算的是 per-sample gradient、model-sampled score、output Hessian pullback 还是 objective HVP；并能为任何“Fisher≈Hessian”声明列出模型正确性、输出族、采样测度、最优点和有限样本条件。

## 练习与独立解答

- [[习题 - Hessian、GGN、Fisher 与经验 Fisher 对象总账]]
- [[解答 - Hessian、GGN、Fisher 与经验 Fisher 对象总账]]
