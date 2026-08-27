---
type: derivation
status: verified
area: [generative-models, discrete-diffusion, categorical]
node_id: GEN-57
prerequisites: ["[[条件概率、全概率与 Bayes 公式]]", "[[DDPM 前向 Markov 加噪与闭式边缘]]", "[[常用离散分布]]"]
related: ["[[Absorbing-state、Mask Diffusion 与并行迭代生成]]", "[[连续时间 Markov 链、离散 Score 与采样]]", "[[VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]"]
sources: ["[[S-2021-Austin-D3PM]]", "[[S-2019-Su-6705-从正态分布到Gumbel-Softmax]]", "[[S-2022-Su-9085-从重参数看离散概率分布]]"]
exercises: ["[[习题 - Categorical Diffusion、转移矩阵与离散后验]]"]
solutions: ["[[解答 - Categorical Diffusion、转移矩阵与离散后验]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-categorical-diffusion-posterior-ledger-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Categorical Diffusion、转移矩阵与离散后验

> [!abstract] 一句话结论
> 连续 DDPM 用均值与协方差描述一步 Gaussian 加噪；categorical diffusion 用 row-stochastic matrix $Q_t$ 描述一步状态替换。矩阵乘积 $\bar Q_t$ 给出任意时刻的闭式边缘，Bayes 公式给出 $q(x_{t-1}\mid x_t,x_0)$；模型只需近似含未知数据分布的反向核。Gumbel–Softmax 是梯度松弛工具，不是 D3PM 转移矩阵的定义。

## 一、对象：离散状态不是整数坐标

设 $x_t\in\mathcal X=\{1,\ldots,K\}$。数字 $1,ldots,K$ 只是类别标签；除非另有 ordinal/graph/embedding 结构，“类别 3 比类别 2 大 1”没有统计意义。

一步 forward corruption 定义为

$$
Q_t[i,j]=q(x_t=j\mid x_{t-1}=i).
$$

每一行是一个 Categorical distribution，因此

$$
Q_t[i,j]\ge0,
\qquad \sum_{j=1}^KQ_t[i,j]=1.
$$

这两个条件比“矩阵元素看起来很小”重要得多：非负性保证概率合法，行和为一保证总质量守恒。

## 二、为什么矩阵乘积就是闭式边缘

令 $e_i$ 是状态 $i$ 的 one-hot 行向量。一步后

$$
q(x_1=\cdot\mid x_0=i)=e_iQ_1.
$$

两步后，对中间状态 $k$ 求和：

$$
\begin{aligned}
q(x_2=j\mid x_0=i)
&=\sum_{k=1}^Kq(x_1=k\mid x_0=i)q(x_2=j\mid x_1=k)\\
&=\sum_kQ_1[i,k]Q_2[k,j]\\
&=(Q_1Q_2)[i,j].
\end{aligned}
$$

归纳得到

$$
\boxed{q(x_t=\cdot\mid x_0=i)=e_i\bar Q_t,
\qquad \bar Q_t=Q_1\cdots Q_t.}
$$

这与 Gaussian DDPM 的 $q(x_t\mid x_0)$ 闭式扮演相同角色：训练时可直接从 $x_0$ 采 $x_t$，不必真的模拟 $t$ 次链。但它只替代 fixed-time marginal sampling，不给出与逐步模拟相同的整条随机路径 coupling。

## 三、三类常见 forward kernel

### 3.1 均匀替换

$$
Q_t=(1-\beta_t)I+\beta_t\frac{\mathbf1\mathbf1^\top}{K}.
$$

含义是以 $1-\beta_t$ 保持原状态，以 $\beta_t$ 从所有 $K$ 类均匀重采。注意均匀重采仍可能抽回原类，所以真正“改变标签”的概率是 $\beta_t(1-1/K)$。

由于 $U=\mathbf1\mathbf1^\top/K$ 满足 $U^2=U$、$IU=U$，各步核可交换，且

$$
\bar Q_t=\bar\alpha_t I+(1-\bar\alpha_t)U,
\qquad \bar\alpha_t=\prod_{s=1}^t(1-\beta_s).
$$

### 3.2 结构化近邻核

若类别有图或 embedding，可令相近状态更易互换，例如

$$
Q_t[i,j]\propto
\begin{cases}
\exp(-d(i,j)^2/\tau_t),&j\in\mathcal N(i),\\
0,&\text{otherwise}.
\end{cases}
$$

归一化后它是合法 kernel，但“embedding 近”是否等于语义可混淆是建模假设。若 embedding 也训练，forward corruption 本身会随参数变化，已不再是固定已知核。

### 3.3 吸收状态核

加入特殊 mask 状态 $m$，真实 token 逐渐跳到 $m$，而 $m$ 一旦到达就保持。它将在 GEN-58 单独推导。

## 四、离散 Bayes 后验逐步推导

训练 ELBO 需要

$$q(x_{t-1}\mid x_t,x_0).$$

固定 $x_0=k,x_t=j$。Bayes 公式给出

$$
q(x_{t-1}=i\mid x_t=j,x_0=k)
=\frac{q(x_{t-1}=i,x_t=j\mid x_0=k)}
{q(x_t=j\mid x_0=k)}.
$$

由 Markov 性，分子拆成

$$
q(x_{t-1}=i\mid x_0=k)q(x_t=j\mid x_{t-1}=i)
=(e_k\bar Q_{t-1})_iQ_t[i,j].
$$

分母是 $(e_k\bar Q_t)_j$，所以

$$
\boxed{
q(x_{t-1}=i\mid x_t=j,x_0=k)
=\frac{(e_k\bar Q_{t-1})_iQ_t[i,j]}
{(e_k\bar Q_t)_j}.}
$$

检查分子对 $i$ 求和：

$$
\sum_i(e_k\bar Q_{t-1})_iQ_t[i,j]
=(e_k\bar Q_t)_j,
$$

所以后验自动归一化。若分母为零，该 conditioning event 在 forward process 下不可能发生，不能强行除法；实现中应通过支持集保证训练样本不会进入该分支。

## 五、一个三状态手算例子

令

$$
Q_1=Q_2=
\begin{bmatrix}
0.8&0.1&0.1\\
0.1&0.8&0.1\\
0.1&0.1&0.8
\end{bmatrix},
\qquad x_0=1.
$$

先算

$$
e_1Q_1=(0.8,0.1,0.1),
$$

再算

$$
e_1Q_1Q_2=(0.66,0.17,0.17).
$$

若观测 $x_2=2$，则 $x_1=i$ 的未归一权重是

$$
(0.8\times0.1,\ 0.1\times0.8,\ 0.1\times0.1)
=(0.08,0.08,0.01).
$$

除以分母 $0.17$，得到

$$
q(x_1=\cdot\mid x_2=2,x_0=1)
=\left(\frac8{17},\frac8{17},\frac1{17}\right).
$$

直觉上，最终看到 2 可能来自“1 到最后一步才变成 2”，也可能“第一步已到 2 后保持”；两条路径概率相同。

## 六、反向模型与 $x_0$ 参数化

真实反向核

$$
q(x_{t-1}\mid x_t)
=\sum_{x_0}q(x_{t-1}\mid x_t,x_0)q(x_0\mid x_t)
$$

中的 $q(x_0\mid x_t)$ 依赖未知数据分布。一种 D3PM 参数化让网络预测

$$
\hat p_\theta(x_0\mid x_t,t),
$$

再与已知 analytic posterior 混合：

$$
p_\theta(x_{t-1}\mid x_t)
=\sum_{\hat x_0}
q(x_{t-1}\mid x_t,\hat x_0)
\hat p_\theta(\hat x_0\mid x_t,t).
$$

另一种做法直接输出 reverse logits。两者函数类和归纳偏置不同；不能只因为最终都给 Categorical probabilities 就称为同一参数化。

## 七、ELBO 从哪来

对 forward chain $q(x_{1:T}\mid x_0)$ 和 generative chain

$$
p_\theta(x_{0:T})=p(x_T)\prod_{t=1}^Tp_\theta(x_{t-1}\mid x_t),
$$

应用变分恒等式，可把负对数似然上界分解为 terminal prior mismatch、各步 posterior KL 与重构项：

$$
\mathcal L_{VLB}
=\mathbb E_q\!\left[
D_{KL}(q(x_T\mid x_0)\|p(x_T))
+\sum_{t=2}^TD_{KL}
(q(x_{t-1}\mid x_t,x_0)\|p_\theta(x_{t-1}\mid x_t))
-\log p_\theta(x_0\mid x_1)
\right].
$$

D3PM 还可加入预测 $x_0$ 的 auxiliary cross-entropy。它常有助优化，但这时训练 objective 不再只是“原始 ELBO 的另一种写法”；必须报告权重。

## 八、Gumbel–Softmax 在这里处于哪一层

[[S-2019-Su-6705-从正态分布到Gumbel-Softmax]] 严格区分了：

- Gumbel-max 的 hard $\arg\max$ 是精确 Categorical sample；
- finite-temperature Gumbel–Softmax 是 simplex 上的连续松弛；
- straight-through hard/soft 组合又是一个代理梯度程序。

D3PM 若只需从已知 $Q_t$ 采样 token，可以直接调用 Categorical sampler，不需要通过 Gumbel–Softmax 定义 forward kernel。只有当“采样选择本身”位于需要端到端求导的路径中，松弛/估计器才成为额外设计。

[[S-2022-Su-9085-从重参数看离散概率分布]] 进一步说明 iid additive noise + argmax 可以反推一类平移不变 choice probabilities；但这仍是“如何构造一次分类选择”，不是多步 Markov diffusion 的完整定义。

## 九、图：从一步核到后验的三条账

先看图回答：$Q_t$、$\bar Q_t$ 和后验分别消去了哪个中间变量？为什么 posterior 的分子必须同时包含“到达 $i$”和“由 $i$ 到 $j$”？

![[00-知识库管理/_assets/figures/generative-models/fig-categorical-diffusion-posterior-ledger-v1.svg|900]]

> [!figure] 图 50.8-01　Categorical diffusion 的转移—边缘—后验账本
> 左侧是 row-stochastic 一步核，中央用矩阵乘法消去中间状态，右侧用 Bayes 把到达概率与最后一步 likelihood 相乘。来源：据 D3PM 与本节推导独立绘制。

**怎样读图**：先沿上方 forward 箭头读 $e_{x_0}Q_1\cdots Q_t$；再从右侧观测 $x_t$ 反看每个候选 $x_{t-1}$ 的两段路径权重，最后归一化。

**图没有证明什么**：图不证明某个 $Q_t$ 最优，不证明辅助 CE 提升似然，也不证明直接预测 $x_0$ 与直接预测 reverse logits 在有限网络和优化下等价。

## 十、本节回顾与训练

- 离散 diffusion 的 forward object 是 stochastic matrix，不是 Gaussian 方差；
- $\bar Q_t$ 给 fixed-time marginal，不能唯一决定 multi-time coupling；
- posterior 是“前段到达概率 × 最后一步 likelihood ÷ 总观测概率”；
- $x_0$ 参数化借 analytic posterior 把干净 token 预测变成 reverse kernel；
- Gumbel–Softmax 是松弛/梯度层，不是 D3PM 的定义层；
- [[习题 - Categorical Diffusion、转移矩阵与离散后验]]
- [[解答 - Categorical Diffusion、转移矩阵与离散后验]]
