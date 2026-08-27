---
type: derivation
status: verified
area: [training, optimization, statistics]
node_id: TRN-02
aliases: [Mini-batch Gradient, 有效批量]
prerequisites: ["[[训练系统的对象、状态与一步更新合同]]", "[[随机梯度与小批量估计]]", "[[期望、方差与矩]]"]
related: ["[[SGD、采样顺序与梯度累积的等价边界]]", "[[梯度噪声协方差、Noise Scale 与 SDE 近似]]", "[[数据并行、All-Reduce 与全局 Batch 语义]]"]
sources: ["[[S-2025-Su-11260-学习率与Batch-Size均衡]]", "[[S-2018-McCandlish-Noise-Scale]]"]
exercises: ["[[习题 - Mini-batch 梯度、平均求和与有效 Batch]]"]
solutions: ["[[解答 - Mini-batch 梯度、平均求和与有效 Batch]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-minibatch-reduction-covariance-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Mini-batch 梯度、平均求和与有效 Batch

> [!abstract] 一句话结论
> 独立同分布样本的 batch **平均梯度**保持总体梯度的期望，covariance 按 $1/B$ 缩小；batch **求和**则把期望和标准差分别放大 $B$ 与 $\sqrt B$。真正进入训练的有效 batch 还取决于 token mask、权重、梯度累积、data-parallel world size 与样本相关性。

## 一、先固定经验目标

数据集 $\{z_i\}_{i=1}^N$，参数 $\theta\in\mathbb R^d$，单样本梯度

$$g_i(\theta)=\nabla_\theta\ell(\theta;z_i)\in\mathbb R^d.$$

经验目标及 full gradient 是

$$F_N(\theta)=\frac1N\sum_{i=1}^N\ell(\theta;z_i),
\qquad G(\theta)=\frac1N\sum_{i=1}^N g_i(\theta).$$

在本节的一次计算中固定 $\theta$，所以随机性只来自 batch index。令总体 gradient covariance

$$C(\theta)=\frac1N\sum_{i=1}^N(g_i-G)(g_i-G)^\top\in\mathbb R^{d\times d}.$$

## 二、with-replacement batch 平均的期望与 covariance

独立均匀抽取 $I_1,\ldots,I_B$，定义

$$\widehat G_B=\frac1B\sum_{j=1}^B g_{I_j}.$$

利用期望线性性：

$$
\mathbb E[\widehat G_B]
=\frac1B\sum_{j=1}^B\mathbb E[g_{I_j}]
=\frac1B\cdot B G=G.
$$

再令 $\xi_j=g_{I_j}-G$。独立性给 $j\ne k$ 时 $\mathbb E[\xi_j\xi_k^\top]=0$，因此

$$
\begin{aligned}
\operatorname{Cov}(\widehat G_B)
&=\mathbb E\left[\left(\frac1B\sum_j\xi_j\right)
\left(\frac1B\sum_k\xi_k\right)^\top\right]\\
&=\frac1{B^2}\sum_{j=1}^B\mathbb E[\xi_j\xi_j^\top]
=\boxed{\frac{C}{B}}.
\end{aligned}
$$

所以每个方向 $u$ 上的 variance 为 $u^TCu/B$，标准差为 $1/\sqrt B$ 级；不要把 variance 和 standard deviation 的缩放混为一谈。

## 三、无放回抽样的有限总体修正

若从 $N$ 个样本中等概率无放回抽 $B$ 个，batch 内 gradient 负相关。使用上面分母为 $N$ 的 $C$，精确公式是

$$
\boxed{\operatorname{Cov}(\widehat G_B)
=\frac{N-B}{B(N-1)}C.}
$$

检查端点：$B=1$ 时为 $C$；$B=N$ 时为零，因为整批平均就是确定的 full gradient。若用无偏 sample covariance $S=\frac1{N-1}\sum_i(g_i-G)(g_i-G)^T$，同一公式写成 $(1-B/N)S/B$。

> [!warning] 跨 step 不再独立
> 每个 epoch 先 shuffle 再依次切 batch 时，同一 epoch 内不同 batch 互相约束。单步 estimator 仍可无偏，但 noise sequence 一般不是 iid；SDE 推导若忽略这种时间相关性，必须标为近似。

## 四、mean 与 sum 的尺度翻译

同一组样本的 sum gradient 是

$$\widehat G_B^{sum}=\sum_{j=1}^B g_{I_j}=B\widehat G_B^{mean}.$$

其期望和 covariance 分别为

$$\mathbb E[\widehat G_B^{sum}]=BG,
\qquad \operatorname{Cov}(\widehat G_B^{sum})=BC.$$

要让无状态 SGD 的单步相同，若 mean 版本用 $\eta_{mean}$，sum 版本必须用

$$\boxed{\eta_{sum}=\eta_{mean}/B.}$$

这只是固定 $B$、无其他非线性 gradient transform 时的尺度等价。clipping、adaptive denominator、epsilon、regularizer 插入位置或变 batch 会破坏简单翻译。

## 五、加权样本与“有效样本数”

若 estimator 是归一化加权平均

$$\widehat G_w=\sum_{i=1}^B a_i g_i,
\qquad a_i\ge0,\quad\sum_i a_i=1,$$

且 $g_i$ iid、covariance 都为 $C$，则

$$\operatorname{Cov}(\widehat G_w)=\left(\sum_i a_i^2\right)C.$$

定义 Kish effective sample size

$$\boxed{B_{eff}=\frac1{\sum_i a_i^2}},$$

便有 covariance $C/B_{eff}$。等权时 $a_i=1/B$，恢复 $B_{eff}=B$；权重高度集中时，名义 batch 很大也可能只有很小的有效样本量。

> [!warning] $B_{eff}$ 不是万能标量
> 若不同样本 covariance 不同、样本相关、token 从属同一 sequence，noise 是各向异性的；一个标量 effective batch 只能概括特定二阶矩，不能保存完整 covariance geometry。

## 六、token、sequence 与 data parallel 的 batch 口径

语言模型常见四个数字：

$$B_{seq}=B_{local}\times W\times K,
\qquad B_{token}=\sum mask,$$

其中 $W$ 是 data-parallel world size，$K$ 是 accumulation steps。只有当各 rank 的梯度规约、每个 micro-batch reduction 和最后除数一致时，才可把它称为某个 global mean。

变长 sequence 下，以下目标不同：

$$
\frac1{B_{seq}}\sum_s\frac1{T_s}\sum_t\ell_{st}
\quad\text{与}\quad
\frac1{\sum_sT_s}\sum_{s,t}\ell_{st}.
$$

前者每条 sequence 权重相同，后者每个 token 权重相同。两者不是实现细节，而是不同的经验目标。

## 七、最小手算

一维 per-sample gradients 为 $\{-1,1,3,5\}$。总体均值 $G=2$，用分母 $N=4$ 的 variance

$$C=\frac{9+1+1+9}{4}=5.$$

with-replacement 且 $B=2$ 时，batch mean variance 为 $5/2=2.5$。无放回时

$$\frac{4-2}{2(4-1)}5=\frac53.$$

若两样本权重为 $a=(0.9,0.1)$，则 $B_{eff}=1/(0.9^2+0.1^2)\approx1.22$，远小于名义 $2$。

## 八、图：Batch 改变的是中心、尺度还是相关性

先看图回答：mean/sum、with/without replacement 和 unequal weights 分别改变 gradient estimator 的哪一部分？

![[00-知识库管理/_assets/figures/training-optimization/fig-minibatch-reduction-covariance-v1.svg|900]]

> [!figure] 图 TRN-02　Mini-batch estimator 的中心、covariance 与有效样本数
> 图把 expectation、covariance 和 update scale 分成三列；蓝色表示目标中心，琥珀表示随机散布，红色表示错误地混用 reduction 与 LR。来源：本课程依据有限总体抽样恒等式独立绘制。

**怎样读图**：先确认目标是 mean 还是 sum，再看抽样相关性，最后才把 estimator 乘 learning rate 变成 update。$B$ 本身不能独立决定 update noise。

**图没有证明什么**：二维椭圆只示意 covariance，不表示真实深网 gradient 是 Gaussian，也不表示一个 $B_{eff}$ 能恢复所有高阶矩和时间相关性。

## 九、AI 实验审计清单

至少记录：

1. batch 单位（image/sequence/token/transition）；
2. local batch、world size、accumulation；
3. loss reduction 和 mask denominator；
4. sampler 是否 replacement、shuffle、stratified、weighted；
5. DDP 是 sum 还是 average，是否存在 uneven inputs；
6. gradient clip 在规约/累积前还是后；
7. 比较时固定的是 LR、update RMS、noise scale 还是 compute。

[[S-2025-Su-11260-学习率与Batch-Size均衡]]提供 learning-rate–batch 联动的中文问题入口；[[S-2018-McCandlish-Noise-Scale]]进一步把 gradient covariance 与有用 batch 尺度连接。二者都不能替代这里的 reduction 与 sampling 合同。

## 十、本节回顾

- mean estimator 无偏，iid covariance 为 $C/B$；
- without replacement 有 finite-population correction；
- sum 与 mean 需要按 $B$ 翻译 LR，且只在限定条件下等价；
- token mean 与 sequence mean 是不同目标；
- 名义 batch、有效 batch 与 critical batch 是三个不同概念；
- 下一节 [[SGD、采样顺序与梯度累积的等价边界]] 将判断 micro-batch accumulation 何时真正等于大 batch。

## 练习与独立解答

- [[习题 - Mini-batch 梯度、平均求和与有效 Batch]]
- [[解答 - Mini-batch 梯度、平均求和与有效 Batch]]
