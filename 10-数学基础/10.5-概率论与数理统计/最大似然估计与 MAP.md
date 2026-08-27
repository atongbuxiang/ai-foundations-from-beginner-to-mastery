---
type: concept
status: draft
area: [math/statistics, ai/probabilistic-modeling, ai/optimization]
aliases: [MLE, maximum likelihood estimation, MAP, maximum a posteriori, 最大后验估计]
prerequisites: ["[[统计模型、估计量与偏差方差]]", "[[常用连续分布与指数族]]", "[[条件概率、全概率与 Bayes 公式]]", "[[多元链式法则与计算图]]"]
related: ["[[Fisher 信息、Cramér–Rao 界与渐近正态性]]", "[[Bayesian 推断与后验预测]]", "[[交叉熵与 KL 散度]]", "[[概率论与数理统计 MOC]]"]
sources: ["MIT-18.655-Lecture-9-10-Methods-of-Estimation", "MIT-18.650-Lectures-4-5-MLE", "Casella-Berger-Statistical-Inference", "Murphy-Probabilistic-Machine-Learning", "Su-2018-5239-MLE-to-EM", "Su-2020-7681-L2-Scale-Invariance"]
created: 2026-08-19
updated: 2026-08-27
---

# 最大似然估计与 MAP

> [!abstract] 本章主问题
> 最大似然固定观测数据，把 $p_\theta(x)$ 看成参数的函数并寻找最能解释数据的参数；MAP 再乘参数先验，寻找后验密度的 mode。二者都是点估计，不自动表达不确定性；likelihood 不是参数概率，MAP 依赖参数坐标，而“正则化 = 先验”只有在目标尺度、参数化、优化更新和先验正规化都对齐时才成立。

## 学习目标

完成本节后，你应当能够：

1. 区分 PMF/PDF、likelihood、log-likelihood 与 posterior；
2. 从 iid 联合密度推导 MLE，并正确处理支持依赖参数、边界与约束；
3. 推导 Bernoulli、Gaussian、Laplace、Uniform 的 MLE；
4. 解释 score equation 只是 interior optimum 的必要条件，不保证存在、唯一或全局最优；
5. 从 expected log-likelihood 推导 KL projection 与 cross-entropy 接口；
6. 从 Bayes 公式推导 MAP，并说明 MLE 与 MAP 的差别；
7. 推导 Gaussian/Laplace prior 与 L2/L1 penalty 的对应及 $n$-scaling；
8. 解释 MLE 的参数变换 equivariance 与 MAP density mode 的坐标依赖；
9. 识别 separation、mixture singularity、label switching、zero probability 和过参数化等失败模式；
10. 用 logsumexp、softplus、constraint transform 和梯度检查实现稳定 likelihood。

> [!question] 初学者读完必须能回答
> 1. 固定参数看 $p(x\mid\theta)$ 与固定数据看 $L(\theta;x)$ 时，归一化对象有什么不同？
> 2. MLE 的 argmax 何时存在、唯一并位于内部，score equation 为什么只给必要条件？
> 3. 支持依赖参数、边界、separation 与 mixture singularity 会怎样破坏常规优化叙述？
> 4. expected log-likelihood 最大化为什么对应从真实分布到模型族的 KL projection？
> 5. MAP 如何由 likelihood 与 prior 得到，它为什么仍只是 posterior 的一个点？
> 6. L2/L1 penalty 与 Gaussian/Laplace prior 的对应需要怎样的样本量尺度和目标约定？
> 7. 为什么 MLE 对一一参数变换 equivariant，而连续密度的 MAP mode 通常依赖坐标？

## 进入正文前：固定数据后，比较参数如何解释同一份观测

> [!info] 课程位置
> 上一章定义了统计模型、估计器与 risk，本章选择两种具体点估计原则：MLE 只比较 likelihood，MAP 再加入 prior。下一章会研究 score 曲率、Fisher 信息与渐近精度；再下一章则保留完整 posterior，而不是只取一个 mode。

> [!tip] 建议两遍阅读
> - 第一遍只用 $n=10,K=3$ 的 Bernoulli 数据，手算 likelihood、MLE、Beta posterior、MAP 和 posterior mean。
> - 第二遍再学习支持依赖参数、边界解、KL projection、正则化尺度、参数变换、separation、mixture singularity 与稳定优化。求导等于零只是候选条件，不替代存在性、约束与全局性检查。

> [!question] 本章的推导问题链
> 1. 固定参数看数据分布与固定数据看 likelihood 时，谁需要归一化？
> 2. Bernoulli log-likelihood 的 score 怎样导出样本均值 MLE？
> 3. 当 $K=0$ 或 $K=n$ 时，为什么内部 score 方程不再描述最优点？
> 4. 加入 Beta prior 后，posterior 和 MAP 怎样改变？
> 5. MAP、posterior mean 和完整 posterior 为什么不能互换？
> 6. 用总损失还是平均损失会怎样改变“penalty 等于 prior”的尺度？
> 7. likelihood 最大化与 Bayesian 参数概率更新分别依赖什么合同？

### 贯穿例：十次观测、三次成功

观测到

$$
n=10,
\qquad
K=\sum_{i=1}^{10}Y_i=3.
$$

在 Bernoulli 模型中，若保留完整有序样本，likelihood 与 $q$ 有关的部分是

$$
L(q;y_{1:10})
=q^3(1-q)^7,
\qquad 0\le q\le1.
$$

若只记录计数 $K=3$，Binomial likelihood 还会多出 $\binom{10}{3}$；它与 $q$ 无关，所以不改变 argmax。

log-likelihood 为

$$
\ell(q)=3\log q+7\log(1-q).
$$

对内部点 $0<q<1$，

$$
\ell'(q)=\frac3q-\frac7{1-q}
=\frac{3-10q}{q(1-q)}.
$$

令 score 为零得到

$$
\widehat q_{\mathrm{MLE}}=\frac3{10}.
$$

并且

$$
\ell''(q)
=-\frac3{q^2}-\frac7{(1-q)^2}<0,
$$

所以这个内部驻点是唯一全局最大值。若 $K=0$，最大值在边界 $q=0$；若 $K=n$，最大值在 $q=1$。此时不能坚持求解只对内部点成立的 score 方程。

#### 加入 Beta$(2,2)$ prior

指定

$$
\pi(q)
=\frac1{B(2,2)}q^{2-1}(1-q)^{2-1}
\propto q(1-q).
$$

Bayes 公式给出 posterior kernel

$$
\begin{aligned}
\pi(q\mid y)
&\propto L(q;y)\pi(q)\\
&\propto q^3(1-q)^7q(1-q)\\
&=q^4(1-q)^8.
\end{aligned}
$$

因此

$$
q\mid y\sim\operatorname{Beta}(5,9).
$$

posterior mode 是

$$
\widehat q_{\mathrm{MAP}}
=\frac{5-1}{5+9-2}
=\frac13.
$$

它被 prior 从 MLE 的 $3/10$ 轻微拉向 prior mode $1/2$。posterior mean 则为

$$
\mathbb E[q\mid y]
=\frac5{14},
$$

与 MAP 的 $1/3$ 不同。完整 posterior 还包含方差、偏度和区间信息，两个点估计都没有保留这些内容。

#### “正则化等于先验”必须核对尺度

MAP 最大化

$$
\ell_n(q)+\log\pi(q),
$$

等价于最小化总负对数目标

$$
-\ell_n(q)-\log\pi(q).
$$

若训练代码使用平均负对数 likelihood，则同一个 prior 对应

$$
-\frac1n\ell_n(q)-\frac1n\log\pi(q).
$$

所以固定 prior 的 penalty 系数在平均目标中带 $1/n$。若代码始终使用固定 $\lambda R(q)$ 而样本量改变，它对应的隐式 prior 强度也随 $n$ 改变；不能只凭目标外形就宣称 Bayesian 等价。

> [!note] 本轮对象账本
> | 对象 | 本例 | 归一化位置 |
> |---|---|---|
> | $p(y\mid q)$ | Bernoulli 数据模型 | 固定 $q$ 后对数据 $y$ 求和为 $1$ |
> | $L(q;y)$ | 固定已观测数据后的 likelihood | 不要求对 $q$ 积分为 $1$ |
> | $\pi(q)$ | Beta$(2,2)$ prior density | 对参数 $q$ 积分为 $1$ |
> | $\pi(q\mid y)$ | Beta$(5,9)$ posterior density | 对参数 $q$ 积分为 $1$ |
> | MLE | $3/10$ | likelihood 的 argmax |
> | MAP | $1/3$ | posterior density 的 mode |
> | posterior mean | $5/14$ | 平方损失下的 Bayesian 点动作 |

> [!analysis] Bernoulli MLE/MAP 推导的公式七问
> 1. **为什么引入？** MLE 找最能解释固定数据的模型参数，MAP 在此基础上加入先验偏好。
> 2. **对象是什么？** 数据固定后，$q$ 是优化变量；likelihood 是参数函数，posterior 才是归一化参数密度。
> 3. **条件是什么？** score 方程只适用于可微内部最优；还要检查参数区间、边界、存在性、唯一性和支持。
> 4. **MLE 怎样得到？** iid likelihood 取 log 后求导，得到 $(K-nq)/(q(1-q))=0$，内部解为 $K/n$。
> 5. **MAP 怎样得到？** log-likelihood 加 log-prior；Beta$(\alpha,\beta)$ 把成功/失败伪计数分别增加 $\alpha-1,\beta-1$。
> 6. **边界在哪里？** posterior mode 依赖连续参数坐标，点估计丢掉不确定性；分离、奇异模型或支持依赖参数时常规 Hessian 叙述可能失败。
> 7. **AI 中对应什么？** binary cross-entropy 就是 Bernoulli 负 log-likelihood；weight decay 可有 Gaussian prior 解释，但必须核对总和/平均、参数化、Jacobian 和样本量尺度。

> [!success] 第一遍停靠线
> 应能从 $n=10,K=3$ 推出 MLE $3/10$；把 Beta$(2,2)$ prior 与 likelihood 相乘得到 Beta$(5,9)$ posterior；分别算出 MAP $1/3$ 和 posterior mean $5/14$；还能解释 likelihood 为什么不是参数概率，以及平均训练损失中的 prior penalty 为什么带 $1/n$。

## 阅读前检查

- [[统计模型、估计量与偏差方差]]：model、parameter、estimand 与 risk；
- [[常用连续分布与指数族]]：density、support、natural parameter 与 log-partition；
- [[条件概率、全概率与 Bayes 公式]]：posterior 正比于 likelihood × prior；
- [[多元链式法则与计算图]]：score、Hessian 与自动微分。

## 零、同一个 $p(x\mid\theta)$ 的两种阅读方式

### 概率模型阅读

固定 $\theta$，让 $x$ 变化：

$$
x\mapsto p(x\mid\theta).
$$

它是数据空间上的 PMF/PDF，满足

$$
\sum_xp(x\mid\theta)=1
\quad\text{或}\quad
\int p(x\mid\theta)dx=1.
$$

### Likelihood 阅读

观测到 $x$ 后固定 $x$，让 $\theta$ 变化：

$$
L(\theta;x)=p(x\mid\theta).
$$

它是参数上的非负函数，一般不满足

$$
\int_\Theta L(\theta;x)d\theta=1.
$$

> [!warning] Likelihood 不是 $P(\theta\mid x)$
> frequentist likelihood 只比较不同参数对同一数据的相对支持。只有指定 prior 并归一化后，才得到 posterior density。

## 一、iid likelihood 与 log-likelihood

若 $X_1,\dots,X_n$ iid $\sim p_\theta$，联合 likelihood：

$$
L_n(\theta;x_{1:n})
=\prod_{i=1}^np_\theta(x_i).
$$

MLE 定义为

$$
\widehat\theta_{\rm MLE}
\in\arg\max_{\theta\in\Theta}L_n(\theta;x).
$$

因 $\log$ 严格单调：

$$
\widehat\theta_{\rm MLE}
\in\arg\max_{\theta\in\Theta}
\ell_n(\theta),
$$

$$
\ell_n(\theta)
=\log L_n(\theta)
=\sum_{i=1}^n\log p_\theta(x_i).
$$

实际训练常最小化 negative log-likelihood：

$$
\operatorname{NLL}_n(\theta)
=-\ell_n(\theta).
$$

### 非 iid 数据

一般应写联合模型

$$
p_\theta(x_{1:n}),
$$

而非强行乘 marginal。自回归模型使用链式分解：

$$
p_\theta(x_{1:T})
=\prod_{t=1}^Tp_\theta(x_t\mid x_{<t}).
$$

token log-likelihood 可相加来自 joint factorization，不意味着 token 无条件 iid。

## 二、例 1：Bernoulli MLE

令 $X_i\sim\operatorname{Bernoulli}(p)$，$S=\sum_iX_i$：

$$
L(p)=p^S(1-p)^{n-S},
\qquad0\le p\le1.
$$

log-likelihood：

$$
\ell(p)=S\log p+(n-S)\log(1-p).
$$

若 $0<S<n$，

$$
\ell'(p)=\frac Sp-\frac{n-S}{1-p}=0
$$

给出

$$
\widehat p=\frac Sn=\bar X.
$$

二阶导

$$
\ell''(p)=-\frac S{p^2}-\frac{n-S}{(1-p)^2}<0,
$$

故为唯一内部最大值。

若 $S=0$，最大值在边界 $\widehat p=0$；若 $S=n$，在 $\widehat p=1$。此时 score equation 的内部推导不适用。

## 三、例 2：Gaussian 均值与方差

令 $X_i\sim N(\mu,\sigma^2)$，参数 $\sigma^2>0$：

$$
\ell(\mu,\sigma^2)
=-\frac n2\log(2\pi)
-\frac n2\log\sigma^2
-\frac1{2\sigma^2}\sum_i(x_i-\mu)^2.
$$

对 $\mu$：

$$
\frac{\partial\ell}{\partial\mu}
=\frac1{\sigma^2}\sum_i(x_i-\mu)=0
\Longrightarrow
\widehat\mu=\bar x.
$$

对 $v=\sigma^2$：

$$
\frac{\partial\ell}{\partial v}
=-\frac n{2v}
+\frac1{2v^2}\sum_i(x_i-\mu)^2=0.
$$

代入 $\widehat\mu$：

$$
\widehat\sigma^2_{\rm MLE}
=\frac1n\sum_i(x_i-\bar x)^2.
$$

它是 MLE，但有限样本有偏：

$$
E[\widehat\sigma^2_{\rm MLE}]
=\frac{n-1}{n}\sigma^2.
$$

无偏样本方差分母 $n-1$，却不是 Gaussian likelihood 的 maximizer。MLE 与无偏性是不同选择标准。

若 $n=1$ 且均值、方差都未知，令 $\mu=x_1$、$\sigma^2\downarrow0$ 会使 likelihood 无界，有限参数 MLE 不存在。

## 四、例 3：Laplace location 与中位数

若

$$
p(x\mid\mu,b)=\frac1{2b}e^{-|x-\mu|/b},
$$

固定 $b$，最大化 likelihood 等价于最小化

$$
\sum_i|x_i-\mu|.
$$

任何样本中位数都是 MLE。Gaussian 假设导出 least squares/mean；Laplace 假设导出 absolute deviation/median。损失函数不是凭审美选择，而是对应了噪声模型。

## 五、例 4：Uniform support 随参数变化

令 $X_i\sim U(0,\theta)$，$\theta>0$：

$$
L(\theta)
=\theta^{-n}\mathbf1_{\{\theta\ge x_{(n)}\}}
\mathbf1_{\{x_{(1)}\ge0\}}.
$$

在允许区域 $\theta\ge x_{(n)}$，$\theta^{-n}$ 单调下降，所以

$$
\widehat\theta_{\rm MLE}=X_{(n)}.
$$

若忽略指示函数，只对 $-n\log\theta$ 求导，会错误地说“没有驻点”。支持依赖参数时，边界本身携带信息，regular score/Fisher 理论也可能失效。

## 六、score、Hessian 与最优性条件

定义 score：

$$
s_n(\theta)=\nabla_\theta\ell_n(\theta).
$$

若 MLE 是参数空间内部可微局部极值，必要条件

$$
s_n(\widehat\theta)=0.
$$

observed Hessian 为

$$
H_n(\theta)=\nabla_\theta^2\ell_n(\theta),
$$

observed information 常记

$$
J_n(\theta)=-H_n(\theta).
$$

### Score equation 不保证什么

- 解存在；
- 解唯一；
- 是最大值而非最小值/鞍点；
- 是全局最大；
- 位于 interior；
- 数值算法找到该解。

若 log-likelihood 在 convex parameter domain 上严格凹且边界趋于 $-\infty$，可推出存在唯一全局最大值；神经网络 likelihood 通常不满足全局凹性。

## 七、存在性、唯一性与可辨识性

### 1. Exponential family moment matching

canonical exponential family：

$$
p_\eta(x)=h(x)e^{\eta^TT(x)-A(\eta)}.
$$

iid average log-likelihood：

$$
\bar\ell_n(\eta)
=\eta^T\bar T-A(\eta)+\text{const}.
$$

score：

$$
\nabla\bar\ell_n(\eta)
=\bar T-\nabla A(\eta)
=\bar T-E_\eta[T(X)].
$$

所以内部 MLE 满足 moment matching：

$$
E_{\widehat\eta}[T(X)]=\bar T.
$$

Hessian：

$$
\nabla^2\bar\ell_n(\eta)
=-\nabla^2A(\eta)
=-\operatorname{Cov}_\eta(T)\preceq0.
$$

非最小族或充分统计量在低维 affine subspace 上时，严格凹/唯一性可能失效；经验统计量落在 convex support 边界时，有限自然参数 MLE 可能不存在。

### 2. Logistic separation

若线性分类数据完全可分，logistic regression 可沿分离方向令权重范数趋于无穷，同时训练 NLL 趋向下确界；没有有限 MLE。优化器“权重一直变大”不一定是数值 bug，而可能是统计目标不取到最小值。

### 3. Gaussian mixture singularity

混合成分均值对准某个样本、方差趋零时，该样本 density 可趋无穷，使 unconstrained mixture likelihood 无界。EM 单调增加 likelihood 不保证存在有限全局 MLE。

### 4. Label switching

交换 mixture component 标签给出同一 likelihood，最大点至少有置换对称。唯一性应在 quotient/equivalence class 上讨论。

## 八、MLE 与 KL projection

设真实分布 $P_0$ 有 density $p_0$。population expected log-likelihood：

$$
Q(\theta)=E_{P_0}[\log p_\theta(X)].
$$

KL：

$$
D_{\mathrm{KL}}(P_0\|P_\theta)
=E_{P_0}\left[\log\frac{p_0(X)}{p_\theta(X)}\right].
$$

所以

$$
Q(\theta)
=E_{P_0}[\log p_0(X)]
-D_{\mathrm{KL}}(P_0\|P_\theta).
$$

第一项与 $\theta$ 无关，因此最大化 expected log-likelihood 等价于最小化 forward KL：

$$
\theta^*\in\arg\min_\theta
D_{\mathrm{KL}}(P_0\|P_\theta).
$$

样本 MLE 是用经验平均近似 $Q(\theta)$ 的 M-estimator。若模型正确且 identifiable，$\theta^*=\theta_0$；若错设，则趋向 pseudo-true KL projection。

> [!warning] 经验 NLL 小不等于 population KL 小
> 还需 uniform convergence、complexity control、优化与分布稳定；过参数模型可记忆训练数据。

## 九、Conditional MLE 与 cross-entropy

监督分类建模

$$
p_\theta(y\mid x).
$$

固定/不建模 input marginal 时，conditional log-likelihood：

$$
\ell(\theta)=\sum_i\log p_\theta(y_i\mid x_i).
$$

对 one-hot label $y_i$：

$$
-\log p_\theta(y_i\mid x_i)
=-\sum_{k=1}^K\mathbf1_{\{y_i=k\}}
\log p_\theta(k\mid x_i),
$$

即 categorical cross-entropy。

### Soft label 与 label smoothing

若 target distribution 为 $q_i(k)$，loss 为

$$
-\sum_kq_i(k)\log p_\theta(k\mid x_i).
$$

它是对 soft target 的 cross-entropy，但不再是原始 hard-label empirical likelihood。label smoothing 改变了估计目标/regularization，应明确说明。

### Language model

$$
-\log p_\theta(x_{1:T})
=-\sum_{t=1}^T\log p_\theta(x_t\mid x_{<t}).
$$

padding mask、length normalization、token mean vs sequence mean 会改变经验目标的 weighting；都必须记录。

## 十、从 MLE 到 MAP

指定 prior density $\pi(\theta)$，Bayes 公式：

$$
p(\theta\mid x)
=\frac{p(x\mid\theta)\pi(\theta)}{p(x)}.
$$

MAP 定义：

$$
\widehat\theta_{\rm MAP}
\in\arg\max_\theta p(\theta\mid x).
$$

证据 $p(x)$ 与 $\theta$ 无关，所以

$$
\widehat\theta_{\rm MAP}
\in\arg\max_\theta
[\ell_n(\theta)+\log\pi(\theta)].
$$

或最小化

$$
-\ell_n(\theta)-\log\pi(\theta).
$$

若 prior 平坦且 proper、参数化固定，MAP 可与 MLE 重合；“平坦 prior”本身依坐标且在无界空间常 improper。

## 十一、Gaussian prior 与 L2 penalty

设

$$
\theta\sim N(0,\tau^2I_d).
$$

则

$$
\log\pi(\theta)
=-\frac d2\log(2\pi\tau^2)
-\frac1{2\tau^2}\|\theta\|_2^2.
$$

MAP 等价于最小化

$$
-\sum_{i=1}^n\log p_\theta(x_i)
+\frac1{2\tau^2}\|\theta\|_2^2.
$$

若代码使用 mean NLL：

$$
-\frac1n\sum_i\log p_\theta(x_i)
+\lambda\|\theta\|_2^2,
$$

与固定 prior 对应时

$$
\lambda=\frac1{2n\tau^2}.
$$

所以在 mean reduction 下保持同一 $\lambda$ 同时改变 $n$，对应的 prior strength 在 Bayesian 解释上会改变。

### Laplace prior 与 L1

若独立坐标

$$
\pi(\theta_j)\propto e^{-|\theta_j|/b},
$$

则 negative log-prior 给

$$
\frac1b\|\theta\|_1.
$$

L1 的 non-differentiability 与 sparsity 需要 subgradient/proximal 方法；MAP 取零不等于 posterior 在该坐标上有 point mass。

## 十二、图示：MLE、MAP 与正则化的对象关系

先用下图回答一个视觉问题：**likelihood、prior、posterior 与它们各自的 mode 为什么不能被混成同一个“最优参数”？**

![[00-知识库管理/_assets/figures/probability/fig-mle-map-geometry-v2.svg|880]]

> [!figure] 图 10.5.16｜Likelihood 的两种阅读、MAP 移动与 mode 信息损失
> A 区分固定 $\theta$ 的数据密度与固定 $x_{obs}$ 的 likelihood；B 展示 prior 与 likelihood 相乘后 posterior mode 相对 MLE 移动；C 用双峰 posterior 说明 MAP 只保留最高 mode，并标出密度 mode 对参数坐标的依赖。来源：独立绘制；生成脚本：[[plot_statistical_estimation_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先问积分是对 $x$ 还是对 $\theta$；B 分别辨认 likelihood 峰、prior 偏好和 posterior 峰，不能把三条曲线的纵轴都解释为同一种概率；C 将 MAP 点与整条 posterior 比较，主动寻找被点估计丢掉的宽度、另一峰和相关结构。

**适用边界（图没有证明什么）。** 曲线只是一维光滑示意，不保证实际 likelihood/posterior 单峰、有界或存在有限极值；MAP 的坐标依赖针对连续密度 mode，一一变换下 MLE 的 argmax 映射性质需满足目标定义良好；“penalty = prior”只在参数化、尺度、Jacobian 与正规化条件对齐时成立。

## 十三、“正则化 = prior”为什么只是有条件的等价

要把 penalty $\Omega(\theta)$ 解释为 prior，需要

$$
\pi(\theta)\propto e^{-\lambda\Omega(\theta)}
$$

在参数空间上可归一化，且目标尺度与 Bayesian posterior 完全对应。

### 需要审计的条件

1. penalty 是否定义了 proper density；
2. 参数化/基准测度是什么；
3. loss 是 sum 还是 mean；
4. 是否对 bias、normalization parameter 等选择性 regularize；
5. optimizer 的 weight decay 是否真的等价于向 loss 加 L2；
6. 参数存在尺度/置换不变性时，prior 是否在等价参数上给出不协调权重；
7. data augmentation、dropout、early stopping 等不一定对应简单 prior；
8. hyperparameter 是否根据同一数据调节。

### Weight decay 与 L2

普通 SGD 更新中，loss 加 $\lambda\|\theta\|^2/2$ 产生

$$
\theta_{t+1}
=(1-\eta\lambda)\theta_t
-\eta\nabla L(\theta_t),
$$

与 decoupled weight decay 形式一致。对 Adam 等 adaptive optimizer，coupled L2 gradient 会被 preconditioner 缩放，而 decoupled weight decay 不同；因此不能无条件写成同一 MAP prior。

### 参数对称性

正齐次网络可对相邻层做

$$
W_1\mapsto cW_1,
\qquad
W_2\mapsto c^{-1}W_2
$$

而函数不变，但 L2 penalty 改变。[[S-2020-Su-7681-L2正则与尺度不变性]]提供这一 AI 问题入口。函数相同不代表 parameter prior density 相同。

## 十四、MLE equivariance 与 MAP 坐标依赖

### MLE 的一一变换性质

若 $\phi=g(\theta)$ 为一一变换，MLE 满足

$$
\widehat\phi_{\rm MLE}=g(\widehat\theta_{\rm MLE}).
$$

因为 likelihood 本身只是用不同坐标索引同一分布。

若 $g$ 非一一，$\phi$ 的 profile likelihood/argmax set 需更谨慎，但 extension principle 仍常定义 $g(\hat\theta)$。

### MAP 不具有普通坐标不变性

posterior density 在变换 $\phi=g(\theta)$ 下：

$$
p_\phi(\phi\mid x)
=p_\theta(\theta\mid x)
\left|\det\frac{\partial\theta}{\partial\phi}\right|.
$$

Jacobian 改变 density mode，因此一般

$$
\operatorname{MAP}_\phi
\ne g(\operatorname{MAP}_\theta).
$$

这不是 Bayes 公式错误，而是 continuous density 的 mode 依赖坐标/基准测度。

## 十五、MAP 不是完整 Bayesian 推断

MAP 只给 posterior mode。它不能单独回答：

- posterior mean/median；
- credible interval；
- parameter correlation；
- 多峰之间的质量；
- posterior predictive；
- prior sensitivity；
- marginal likelihood/model comparison。

在平方损失下 Bayesian point estimator 是 posterior mean；绝对损失下是 posterior median；0–1 型局部损失才与 mode 更接近。选择 MAP 必须说明决策损失。

## 十六、隐变量与 EM 接口

若观测 likelihood

$$
p_\theta(x)=\int p_\theta(x,z)dz
$$

难直接最大化，引入当前参数 $\theta^{(t)}$ 下的 posterior

$$
q_t(z)=p_{\theta^{(t)}}(z\mid x).
$$

由 Jensen/ELBO：

$$
\log p_\theta(x)
\ge E_{q_t}[\log p_\theta(x,Z)]
-E_{q_t}[\log q_t(Z)].
$$

E-step 计算/近似 $q_t$；M-step 最大化

$$
Q(\theta\mid\theta^{(t)})
=E_{q_t}[\log p_\theta(x,Z)].
$$

在精确 EM 条件下 observed-data likelihood 不下降，但：

- 不保证全局最优；
- E-step 可能不可算；
- mixture likelihood 可能无界；
- generalized/variational EM 需重写各自保证。

[[S-2018-Su-5239-从最大似然到EM]]把分类交叉熵、joint KL 与隐变量交替更新连为直观入口；严格单调性与条件由正式统计来源承担。

## 十七、稳定数值实现

### 1. 永远优先 log-likelihood

概率乘积会下溢：

$$
\prod_ip_i
$$

改算

$$
\sum_i\log p_i.
$$

### 2. Categorical log-softmax

logit $z_k$：

$$
\log p(y=k)
=z_k-\operatorname{LSE}(z),
$$

$$
\operatorname{LSE}(z)
=m+\log\sum_je^{z_j-m},
\quad m=\max_jz_j.
$$

不要先 softmax 再 log；极小概率会先舍入为零。

### 3. Binary logistic 的 softplus

若 $y\in\{0,1\}$、logit $z$：

$$
-\log p(y\mid z)
=\operatorname{softplus}(z)-yz.
$$

稳定实现使用 framework fused `binary_cross_entropy_with_logits`。

### 4. 正值/单纯形约束

- $\sigma=\operatorname{softplus}(\rho)+\varepsilon$；
- probability vector 用 softmax logits；
- covariance 用 Cholesky factor；
- 对变换后的 parameter 做 MAP 时必须明确 prior 定义在哪个坐标并包含 Jacobian。

### 5. Gradient/Hessian 验证

检查：

- per-example log-likelihood 与 batch reduction；
- analytic score vs AD；
- directional finite difference；
- boundary/zero-count cases；
- normalized density 在简单模型上积分为 1；
- optimizer 输出与 closed-form MLE 对照。

## 十八、AI 目标中哪些不是原始 MLE

| 方法 | 与 MLE 的关系 |
|---|---|
| hard-label cross-entropy | conditional categorical MLE |
| label smoothing | 改过 target 的 cross-entropy/regularization |
| class weighting | 改变经验测度或 cost，不是原始样本 likelihood |
| focal loss | 修改 proper log score，通常不是原模型 NLL |
| negative sampling | surrogate sampling objective，不等于 full softmax MLE |
| NCE | 用分类估计未归一化模型参数，有独立一致性条件 |
| contrastive loss | 依构造可能是 ratio estimation/MI bound，不自动是 data likelihood |
| dropout/early stopping | 隐式/算法 regularization，不自动等于某简单 MAP |
| RLHF preference loss | 通常是指定 preference model 的 conditional likelihood |

## 十九、常见误区

### 误区 1：likelihood 越大，参数发生的概率越大

likelihood 不是参数概率；它只比较参数对固定数据的相对支持。

### 误区 2：把 likelihood 对参数积分归一化就总能得到 posterior

这相当于选择相对于某坐标 Lebesgue measure 的 flat prior；变换坐标后答案改变，且积分可能发散。

### 误区 3：解 score=0 就完成 MLE

边界最大、无界 likelihood、多解、鞍点和约束都可让该步骤失败。

### 误区 4：MLE 总无偏

Gaussian variance MLE 已是反例；MLE 主要优势通常是 regular conditions 下的一致性与渐近效率。

### 误区 5：MAP 总比 MLE 泛化好

依赖 prior 是否合理、参数化、超参数选择和模型错设；错误 prior 可增加风险。

### 误区 6：L2 一定等于 Gaussian prior

需核对 sum/mean、系数、weight decay 实现、parameter transform、对称性和 prior 是否 proper。

### 误区 7：训练 NLL 降到零说明学到真实分布

它可能来自记忆、分离、density spike 或数据泄漏；必须看独立 evaluation 与 model diagnostics。

## 二十、Likelihood/MAP 审计模板

1. 完整 joint/conditional model 是什么？
2. 数据依赖是否允许 product factorization？
3. support 是否依参数变化？
4. 参数是否 identifiable，有何对称性？
5. likelihood 是否有有限 maximizer，是否唯一？
6. score 解是否为 interior/global maximum？
7. 目标使用 sum 还是 mean reduction？
8. 若 MAP，prior 对哪个参数坐标定义，是否 proper？
9. penalty coefficient 与 $n$ 的对应是什么？
10. optimizer weight decay 是否等于 loss L2？
11. log-prob 是否用稳定 fused 实现？
12. 训练目标与真正业务 estimand 是否一致？
13. 模型错设时 pseudo-true target 是什么？
14. 是否报告 standard error/posterior uncertainty，而非只给点？
15. 是否用独立数据评估完整选择程序？

## 二十一、与后续章节的接口

- [[Fisher 信息、Cramér–Rao 界与渐近正态性]]：score 波动与 curvature 如何决定 MLE 局部精度；
- [[Bayesian 推断与后验预测]]：从 posterior mode 扩展到完整 posterior 与 prediction；
- [[假设检验、置信区间与多重比较]]：likelihood ratio、Wald/score inference；
- [[MCMC 与随机模拟诊断]]：高维 posterior 无法解析归一化/积分时的计算；
- [[交叉熵与 KL 散度]]：log score、KL projection 与信息论解释。

## 本章自检

- [ ] 能区分 density、likelihood 和 posterior；
- [ ] 能推导四个经典模型的 MLE 并处理边界；
- [ ] 能说明 score=0 的适用范围；
- [ ] 能从 expected log-likelihood 推出 KL projection；
- [ ] 能推导 conditional cross-entropy；
- [ ] 能从 prior 推导 MAP/L2/L1，并核对 sum/mean scaling；
- [ ] 能解释 MLE equivariance 与 MAP coordinate dependence；
- [ ] 能识别 separation、mixture singularity 和 label switching；
- [ ] 能用 logsumexp/softplus 写稳定 NLL；
- [ ] 能判断一个 AI loss 是否真是原模型 likelihood。

## 练习与解答

- [[习题 - 最大似然估计与 MAP]]
- [[解答 - 最大似然估计与 MAP]]

## 参考文献与延伸

- MIT 18.655, Lectures 9–10：minimum contrast、MLE、exponential family、存在唯一性与 EM；
- MIT 18.650, Lectures 4–5：MLE 与 parametric inference；
- Casella & Berger, *Statistical Inference*；
- Murphy, *Probabilistic Machine Learning*；
- [[S-2018-Su-5239-从最大似然到EM]]；
- [[S-2020-Su-7681-L2正则与尺度不变性]]。
