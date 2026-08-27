---
type: concept
status: draft
area: [math/information-theory, math/statistics, math/geometry, ai/generative-models]
aliases: [f-散度, Bregman 散度, 概率分布距离, Probability Metrics]
prerequisites: ["[[交叉熵与 KL 散度]]", "[[互信息与依赖性]]", "[[最大熵原理与指数族]]", "[[联合分布、边缘分布与独立性]]"]
related: ["[[信息论与统计学习接口 MOC]]", "[[变分推断、ELBO 与证据分解]]", "[[多元高斯分布]]", "[[正定核、RKHS 与表示定理]]", "[[率失真、信息瓶颈与最小描述长度]]"]
sources: ["Csiszar-1967-f-Divergence", "Nowozin-Cseke-Tomioka-2016-fGAN", "Bregman-1967-Relaxation-Method", "Sriperumbudur-et-al-2010-Kernel-Metrics", "Gretton-et-al-2012-MMD", "Arjovsky-Chintala-Bottou-2017-WGAN", "Su-6016-fGAN", "Su-6280-Wasserstein-WGAN", "Su-8244-WGAN-Distance", "Su-8512-Gaussian-Distances"]
created: 2026-08-19
updated: 2026-08-27
---

# f-散度、Bregman 散度与概率度量

> [!abstract] 本章主问题
> 没有一种“分布距离”在所有任务上都最好。$f$-divergence 比较 density ratio，具有 Markov data processing，却通常不使用样本空间的 ground geometry；Bregman divergence 来自 convex potential 的一阶线性化误差，依赖所选坐标/参数空间；integral probability metric 比较一类 test functions 的 expectation，Wasserstein 与 MMD 分别通过 Lipschitz 几何和 RKHS kernel 感知分布。选择时必须同时检查：概率对象、支撑、方向、几何、拓扑、可估性、sample complexity 与训练 surrogate。

## 学习目标

完成本节后，你应当能够：

1. 区分 divergence、pseudometric 与 metric 的公理；
2. 定义一般 $f$-divergence 并列出 KL、reverse KL、$\chi^2$、Hellinger、TV 与 JS；
3. 用 Jensen 证明 $f$-divergence 非负性；
4. 证明 $f$-divergence 的 data processing inequality；
5. 推导 Fenchel variational representation 与受限 critic gap；
6. 定义 Bregman divergence 并解释 KL 的 negative-entropy形式；
7. 在指数族中推导 KL 与 log-partition Bregman geometry；
8. 定义 IPM、total variation、$W_p$ 与 MMD；
9. 用 disjoint point masses 比较 JS/TV/KL 与 Wasserstein/MMD topology；
10. 解释 characteristic kernel、Lipschitz critic 与 ground cost；
11. 使用 Pinsker inequality 连接 KL 与 TV；
12. 审计 empirical divergence、critic estimate、Sinkhorn 与 MMD estimator；
13. 区分 population distance、sample estimator 与 train objective；
14. 为 VI、GAN、domain shift、two-sample testing 与 representation matching 选择合适对象。

> [!question] 初学者读完必须能回答
> 1. divergence、pseudometric 与 metric 的 nonnegativity、identity、symmetry、triangle 条件怎样区分？
> 2. $f$-divergence 依赖什么 density-ratio/measure 结构，为什么具有 data processing？
> 3. Bregman divergence 怎样由 convex tangent gap 定义，为什么通常不对称且依赖坐标？
> 4. IPM 的 test-function class、Wasserstein 的 ground cost 与 MMD 的 kernel 分别引入什么几何？
> 5. disjoint support 或 point masses 靠近时，KL/JS/TV 与 Wasserstein 的拓扑反应有何不同？
> 6. TV 或 KL 为什么可同时出现在多个家族中，家族标签为何不是互斥分类？
> 7. population distance、finite-sample estimator、critic lower bound 与实际 train objective 为什么必须分层报告？

## 阅读前检查

- [[交叉熵与 KL 散度]]：KL 的方向、支撑和非 metric 性；
- [[最大熵原理与指数族]]：convex conjugate、log-partition 与 Bregman relation；
- [[联合分布、边缘分布与独立性]]：coupling 与 marginals；
- [[多元高斯分布]]：Gaussian KL、Bhattacharyya 与 $W_2$；
- convex analysis/RKHS/optimal transport 的完整定理将在相应后续卷继续深化。

## 零、先按“依赖什么结构”分类

| 家族 | 典型形式 | 依赖的结构 | 典型成员 |
|---|---|---|---|
| $f$-divergence | $E_Qf(dP/dQ)$ | density ratio/measure relation | KL、JS、TV、Hellinger、$\chi^2$ |
| Bregman divergence | convex function 与 tangent gap | vector/parameter coordinates | squared Euclidean、KL on simplex、$B_A$ |
| IPM | $\sup_{g\in\mathcal F}|E_Pg-E_Qg|$ | test-function class | TV、$W_1$、MMD |
| optimal transport | coupling 的最小 ground cost | sample-space metric/cost | $W_p$、Sinkhorn-regularized OT |

先用下图回答一个视觉问题：**density ratio、convex tangent gap、test-function class 与 ground cost 为什么会产生不同的分布差异量？**

![[00-知识库管理/_assets/figures/information-theory/fig-divergence-metric-topology-v2.svg|880]]

> [!figure] 图 10.6.9｜$f$-divergence、Bregman 几何与 IPM/OT 结构
> A 把 $f$-divergence 写成 $Q$ 下 density ratio 函数的期望；B 用 convex function 在 $q$ 处的切线与 $p$ 处函数值之间的竖直缺口构造 Bregman divergence；C 以样本点、test function 与 coupling/ground cost 表示 IPM 和 optimal transport 的结构。来源：独立绘制；生成脚本：[[plot_information_geometry_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先检查 $P,Q$ 的测度关系与 ratio 是否定义；B 先固定 potential 和坐标，再确认参数顺序决定在哪一点作切线；C 分别问函数类能分辨哪些差异、ground metric/cost 是否表达任务几何，以及所用 kernel 是否 characteristic。

**适用边界（图没有证明什么）。** 三栏不是互斥分类：TV 同时是 $f$-divergence 与 IPM，KL 在适当坐标中也可呈 Bregman 结构；示意 coupling 不一定是最优 coupling；metric 仍需 symmetry 与 triangle inequality。任何 empirical critic/MMD/Sinkhorn 数值都不是无误差的 population quantity，也未必等于实际优化 surrogate。

同一个对象可能属于多个视角：TV 同时是 $f$-divergence 和 IPM；KL 是 $f$-divergence，也是在 probability simplex/指数族坐标上的 Bregman divergence。家族分类描述结构，不是互斥标签。

## 进入正文前：同一对分布，为什么会得到不同的“差异”

> [!info] 课程位置
> [[变分推断、ELBO 与证据分解]]得到 exact posterior $P=\operatorname{Bernoulli}(1/2)$ 与近似 $Q=\operatorname{Bernoulli}(1/4)$，并只使用了 reverse KL $D(Q\Vert P)$。本章保持这对分布不变，逐项比较方向、支撑、概率坐标与 ground geometry，回答“该用哪个差异量”；下一章[[率失真、信息瓶颈与最小描述长度]]会把这些差异放回具体的压缩、任务和编码目标。

> [!tip] 建议两遍阅读
> - **第一遍：** 在二点空间上手算 forward/reverse KL、TV、$W_1$ 与 negative-entropy Bregman gap，观察它们为什么数值和语义不同。
> - **第二遍：** 再读一般 $f$-divergence、data processing、Fenchel critic、指数族双坐标、MMD、OT topology 与 finite-sample estimator。

> [!question] 本章的推导问题链
> 1. divergence、pseudometric 与 metric 分别要求哪些公理？
> 2. 交换 KL 参数为什么会交换 expectation 权重和 support penalty？
> 3. Bregman divergence 为什么必须先选 convex potential 和坐标？
> 4. $W_1$ 为什么需要样本空间的 ground cost，而 KL/TV 不读取两点之间的物理距离？
> 5. population distance、经验 estimator、variational lower bound 与训练 surrogate 为什么是四层对象？

### 贯穿算例：exact posterior 与“仍停在 prior”的近似

沿用上一章对观测 $X=1$ 的结果：

$$
P=\operatorname{Bernoulli}\!\left(\frac12\right)
\quad\text{是 exact posterior},
$$

$$
Q=\operatorname{Bernoulli}\!\left(\frac14\right)
\quad\text{是未更新的 variational approximation}.
$$

二点概率表为

| state $z$ | $P(z)$ | $Q(z)$ | $P(z)-Q(z)$ |
|---:|---:|---:|---:|
| $0$ | $1/2$ | $3/4$ | $-1/4$ |
| $1$ | $1/2$ | $1/4$ | $+1/4$ |

#### 方向一：forward KL

$$
\begin{aligned}
D_{\mathrm{KL}}(P\Vert Q)
&=\frac12\ln\frac{1/2}{3/4}
+\frac12\ln\frac{1/2}{1/4}\\
&=\frac12\ln\frac43\\
&\approx0.143841\ \text{nat}.
\end{aligned}
$$

#### 方向二：reverse KL

$$
\begin{aligned}
D_{\mathrm{KL}}(Q\Vert P)
&=\frac34\ln\frac{3/4}{1/2}
+\frac14\ln\frac{1/4}{1/2}\\
&=\frac34\ln\frac32+\frac14\ln\frac12\\
&\approx0.130812\ \text{nat}.
\end{aligned}
$$

第二个数正是上一章的 ELBO gap。两个 KL 都合法，却回答不同的平均问题；不能因为数值接近就交换方向。

#### TV 与 Wasserstein：同为 $1/4$，原因不同

total variation 是

$$
\operatorname{TV}(P,Q)
=\frac12\sum_z|P(z)-Q(z)|
=\frac14.
$$

若给状态空间规定 ground distance $d(0,1)=1$，需要把 $1/4$ probability mass 从 $0$ 移到 $1$，因此

$$
W_1(P,Q)=\frac14.
$$

这里两个数相同只是二点单位距离的巧合。若把 ground distance 改为 $d(0,1)=c$，则

$$
W_1(P,Q)=\frac c4,
$$

而 TV 与两个 KL 完全不变。Wasserstein 读取“质量搬多远”，TV 只读取“总共搬多少质量”。

#### KL 还是一个 Bregman gap

在 Bernoulli mean parameter $u\in(0,1)$ 上定义 negative entropy

$$
F(u)=u\ln u+(1-u)\ln(1-u).
$$

则

$$
B_F(p,q)
=F(p)-F(q)-F'(q)(p-q)
=D_{\mathrm{KL}}(\operatorname{Ber}(p)\Vert\operatorname{Ber}(q)).
$$

取 $p=1/2,q=1/4$，Bregman gap 就是 forward KL 的 $0.143841$ nat。这里依赖的是 probability-coordinate potential；换坐标或换 potential 会得到另一种几何。

### 支撑失配校准：有限与无穷不是同一故障等级

再把近似改成 $Q_0=\delta_0$，即坚称 $Z=1$ 不可能。则

$$
D(P\Vert Q_0)=+\infty,
\qquad
D(Q_0\Vert P)=\ln2,
$$

同时

$$
\operatorname{TV}(P,Q_0)=\frac12,
\qquad
W_1(P,Q_0)=\frac12
$$

（仍取单位 ground distance）。forward KL 对漏掉 $P$ 的真实 support 给无穷惩罚；reverse KL、TV 与 $W_1$ 仍有限。哪一种反应“正确”取决于任务：编码真实数据时漏 support 是灾难；允许几何移动的生成任务可能更关心搬运距离。

> [!note] 符号与对象账本
> | 符号 | 类型 | 在本例中的角色 |
> |---|---|---|
> | $P$ | target distribution | exact posterior Ber$(1/2)$ |
> | $Q$ | approximation | 未更新的 Ber$(1/4)$ 近似 |
> | $D_f(P\Vert Q)$ | divergence | 由 density ratio 与 convex generator 定义 |
> | $B_F(p,q)$ | coordinate divergence | convex potential 在 $q$ 处切线的剩余量 |
> | $\operatorname{TV}(P,Q)$ | metric/IPM | bounded events/tests 能区分的最大概率差 |
> | $W_1(P,Q)$ | metric/OT cost | 在指定 ground metric 下搬运概率质量的最小成本 |
> | $\widehat D$ | estimator | 从有限样本或受限 critic 得到的近似数，不自动等于 population quantity |

> [!analysis] 分布差异量的公式七问
> | 问题 | 回答 |
> |---|---|
> | 比较的概率对象是什么？ | 先声明是 joint、conditional、posterior、empirical measure 还是模型输出；非概率 score 不能直接代入。 |
> | 方向由谁加权？ | KL/$f$-divergence 要写清 Radon–Nikodym ratio 和 expectation 的分布；交换参数通常改变数值与 support penalty。 |
> | 是否需要坐标或 ground geometry？ | Bregman 需要 vector coordinates 与 potential；Wasserstein 需要 ground cost；普通 KL/TV 不读取点间距离。 |
> | 它是 divergence 还是 metric？ | 检查 symmetry 与 triangle inequality；KL/Bregman 通常不是 metric，TV/$W_p$ 是适当空间上的 metric。 |
> | 支撑不重叠时怎样反应？ | forward KL 可无穷，JS/TV/Hellinger 有界，Wasserstein 仍按搬运距离变化。 |
> | 实际算到的是什么？ | empirical plug-in、neural critic lower bound、MMD U-statistic 或 Sinkhorn regularized cost 都带估计/近似误差。 |
> | AI 中怎样选？ | VI 看 posterior expectation 可算性，GAN 看支撑与 critic，domain shift 看任务函数类，几何生成看 ground cost，两样本检验看 sample complexity。 |

> [!success] 第一遍停靠线
> 若你能对同一 $P=\operatorname{Ber}(1/2),Q=\operatorname{Ber}(1/4)$ 复算正反 KL、TV 与 $W_1$，解释 $W_1=c/4$ 为何随 ground distance 改变，并用 $Q_0=\delta_0$ 说明 forward KL 无穷而其他量仍有限，就已掌握第一遍主干。Fenchel critic、MMD、Gaussian 与 topology 留到第二遍。

## 一、divergence 与 metric 不是同义词

一个 divergence 通常只要求

$$
D(P,Q)\ge0,
\qquad D(P,Q)=0\Longleftrightarrow P=Q
$$

（第二条也可能只对严格版本成立）。metric 还要求：

$$
d(P,Q)=d(Q,P),
$$

$$
d(P,R)\le d(P,Q)+d(Q,R).
$$

pseudometric 允许不同对象距离为零。KL 不对称且不满足 triangle inequality；$W_p$ 在相应有限 moment 空间是 metric；MMD 在 kernel 不 characteristic 时可能只是 pseudometric。

## 二、$f$-divergence 的统一定义

先在 $P\ll Q$ 情形定义 likelihood ratio

$$
r(x)=\frac{dP}{dQ}(x).
$$

若 $f:(0,\infty)\to\mathbb R$ convex 且 $f(1)=0$：

$$
\boxed{
D_f(P\|Q)=E_Q\left[f\left(\frac{dP}{dQ}\right)\right].
}
$$

一般测度情形要用 $f(0)$、$f'(\infty)$ 的 lower-semicontinuous extension 处理 singular mass；不能总是假设双方都有同一 Lebesgue density。

### 2.1 常见生成函数

| 名称 | $f(t)$ | $D_f(P\|Q)$ |
|---|---|---|
| forward KL | $t\log t$ | $D(P\|Q)$ |
| reverse KL | $-\log t$ | $D(Q\|P)$ |
| Pearson $\chi^2$ | $(t-1)^2$ | $\int (p-q)^2/q$ |
| squared Hellinger | $(\sqrt t-1)^2$ | $\int(\sqrt p-\sqrt q)^2$ |
| total variation | $\tfrac12|t-1|$ | $\tfrac12\int|p-q|$ |
| Jensen–Shannon | $\tfrac12[t\log\frac{2t}{1+t}+\log\frac2{1+t}]$ | $\tfrac12D(P\|M)+\tfrac12D(Q\|M)$ |

其中 $M=(P+Q)/2$。向 $f$ 加线性项 $a(t-1)$ 不改变 divergence，因为 $E_Q[r-1]=0$；所以 generator 不唯一。

## 三、非负性与 equality

由 Jensen：

$$
D_f(P\|Q)
=E_Qf(r)
\ge f(E_Qr)
=f(1)=0.
$$

若 $f$ 在 $1$ 附近严格凸且 equality 条件适用，则 equality 要求

$$
r=1\quad Q\text{-a.s.},
$$

即 $P=Q$。若 $f$ 不严格凸，$D_f=0$ 是否识别 distribution 需单独检查。

### 3.1 方向与支撑

- forward KL $D(P\|Q)$ 强烈惩罚 $P$ 有质量而 $Q$ 为零；
- reverse KL $D(Q\|P)$ 交换哪一方承担 expectation；
- JS 因 mixture $M$ 覆盖双方而总 finite，equal-weight 时

$$
0\le\operatorname{JS}(P,Q)\le\log2;
$$

- Hellinger 与 TV 对 singular distributions 仍 finite；
- finite 不代表优化 gradient 一定有用。

## 四、$f$-divergence 的 data processing

令同一 Markov kernel $K(dy\mid x)$ 作用于 $P,Q$，得到 $P_Y,Q_Y$。在 $Q$ 与 channel 的 joint law 下，令

$$
r(X)=\frac{dP}{dQ}(X).
$$

输出 likelihood ratio 满足

$$
\frac{dP_Y}{dQ_Y}(Y)=E_Q[r(X)\mid Y].
$$

于是 conditional Jensen：

$$
\begin{aligned}
D_f(P_Y\|Q_Y)
&=E_{Q_Y}f(E_Q[r(X)\mid Y])\\
&\le E_Qf(r(X))\\
&=D_f(P\|Q).
\end{aligned}
$$

因此任何相同 randomized post-processing 都不能增加 $f$-divergence。Bregman divergence 一般没有这一 property；Wasserstein 也不是“任意 Markov kernel 下无条件收缩”，但 $L$-Lipschitz deterministic map 给 $W_p$ 至多放大 $L$ 倍。

## 五、Fenchel variational representation

convex conjugate：

$$
f^*(u)=\sup_{t>0}\{ut-f(t)\}.
$$

Fenchel inequality：

$$
f(t)\ge ut-f^*(u).
$$

取 $t=p/q$、令 test function $T(x)$ 代替 $u$：

$$
D_f(P\|Q)
\ge E_PT(X)-E_Qf^*(T(X)).
$$

在适当 function class 与 regularity 下取 supremum：

$$
\boxed{
D_f(P\|Q)
=\sup_T\{E_PT-E_Qf^*(T)\}.
}
$$

最优 $T^*(x)$ 与 $f'(p/q)$ 相连。这使只有 samples 的 density-ratio estimation 成为可能，也是 f-GAN 的基础。

### 5.1 理论 supremum 与 neural critic 是四层对象

实际训练得到

$$
\sup_{T\in\mathcal T_\psi}
\left[\widehat E_PT-\widehat E_Qf^*(T)\right]
$$

而非自动得到 population $D_f$。误差包括：

1. critic family approximation gap；
2. finite-sample estimation/generalization gap；
3. inner optimization gap；
4. generator 与 critic 交替训练的 game-dynamics gap。

[[S-2018-Su-6016-fGAN与变分散度]]提供推导入口；任何 train discriminator loss 都不能未经校准直接称为“真实 divergence”。

## 六、Bregman divergence：convex tangent 的剩余量

令 $F$ 是 differentiable strictly convex function，定义

$$
\boxed{
B_F(u,v)=F(u)-F(v)-\langle\nabla F(v),u-v\rangle.
}
$$

convexity 表示 graph 在 tangent hyperplane 上方，因此

$$
B_F(u,v)\ge0.
$$

它测量从 $v$ 的一阶线性化预测 $F(u)$ 时留下的 convexity gap。

### 6.1 例子

- $F(u)=\tfrac12\|u\|_2^2$：

$$
B_F(u,v)=\frac12\|u-v\|_2^2;
$$

- probability simplex interior 上

$$
F(p)=\sum_ip_i\log p_i=-H(p),
$$

则

$$
B_F(p,q)=\sum_ip_i\log\frac{p_i}{q_i}=D(p\|q).
$$

Bregman divergence 一般不对称、不满足 triangle inequality，也不对 arbitrary stochastic processing 收缩。它依赖选定 vector coordinates 与 potential。

## 七、指数族中的 KL–Bregman 双坐标

指数族

$$
p_\eta(x)=h(x)e^{\eta^\top T(x)-A(\eta)}
$$

满足

$$
\mu=\nabla A(\eta)=E_\eta T.
$$

直接展开：

$$
\begin{aligned}
D(p_\eta\|p_{\eta'})
&=E_\eta[(\eta-\eta')^\top T-A(\eta)+A(\eta')]\\
&=A(\eta')-A(\eta)-\nabla A(\eta)^\top(\eta'-\eta)\\
&=\boxed{B_A(\eta',\eta)}.
\end{aligned}
$$

在 mean coordinates 与 convex conjugate $A^*$ 下：

$$
D(p_\eta\|p_{\eta'})=B_{A^*}(\mu,\mu').
$$

这解释了 information geometry 中 natural/mean dual coordinates，也提醒 Bregman argument order 不能凭直觉交换。

## 八、IPM：用 test functions 区分 distributions

给函数类 $\mathcal F$：

$$
\boxed{
\gamma_\mathcal F(P,Q)
=\sup_{g\in\mathcal F}|E_Pg-E_Qg|.
}
$$

直觉：若一组 tests 无法区分两分布，它们在该 function class 的观测分辨率下接近。function class 越大，distinguishing power 通常越强，但 finite-sample estimation 越难。

### 8.1 total variation 是最强 bounded-test 差异

$$
\operatorname{TV}(P,Q)
=\sup_A|P(A)-Q(A)|
=\frac12\int|p-q|.
$$

等价地

$$
\operatorname{TV}(P,Q)
=\frac12\sup_{\|g\|_\infty\le1}|E_Pg-E_Qg|.
$$

它能用所有 bounded measurable tests，故很强；但 continuous high-dimensional empirical measures 即使来自同一 law，也常因无重复样本而 empirical TV 接近 1，直接 plug-in 很不实用。

## 九、Wasserstein：把 ground geometry 写进距离

metric space $(\mathcal X,d)$ 上，coupling 集

$$
\Pi(P,Q)=\{\gamma:\gamma_X=P,\gamma_Y=Q\}.
$$

定义

$$
\boxed{
W_p(P,Q)
=\left[inf_{\gamma\in\Pi(P,Q)}
E_\gamma d(X,Y)^p\right]^{1/p}.
}
$$

$W_p$ 问“把 $P$ 的质量搬成 $Q$ 最少花多少 ground cost”。所以改变单位、feature scaling 或 cost metric 会改变答案。

### 9.1 Kantorovich–Rubinstein dual for $W_1$

在适当 metric-space 与 finite-first-moment 条件下：

$$
\boxed{
W_1(P,Q)
=\sup_{\|g\|_{\rm Lip}\le1}
\{E_Pg-E_Qg\}.
}
$$

WGAN critic 试图近似 1-Lipschitz function class。neural architecture、spectral normalization、weight clipping 或 sampled gradient penalty 都只是不同近似/约束机制，不自动等于全局 Lipschitz ball。

## 十、MMD：用 RKHS unit ball 比较 mean embeddings

给 positive-definite kernel $k$ 与 RKHS $\mathcal H$：

$$
\operatorname{MMD}_k(P,Q)
=\sup_{\|g\|_\mathcal H\le1}|E_Pg-E_Qg|.
$$

mean embedding

$$
\mu_P=E_P[k(X,\cdot)]
$$

存在时：

$$
\operatorname{MMD}_k(P,Q)=\|\mu_P-\mu_Q\|_\mathcal H.
$$

平方展开：

$$
\boxed{
\operatorname{MMD}_k^2
=E k(X,X')+E k(Y,Y')-2E k(X,Y).
}
$$

若 kernel characteristic，MMD 为零才推出 $P=Q$；否则不同 distributions 可能有同一 embedding。RBF bandwidth 决定哪些尺度的差异被强调。

## 十一、disjoint point masses 揭示 topology 差异

令

$$
P=\delta_0,
\qquad Q_\theta=\delta_\theta.
$$

当 $\theta\ne0$，supports disjoint：

| 对象 | 值 |
|---|---:|
| $D(P\|Q_\theta)$ | $+\infty$ |
| $D(Q_\theta\|P)$ | $+\infty$ |
| JS | $\log2$ |
| TV | $1$ |
| squared Hellinger（本章 convention） | $2$ |
| $W_1$ on $\mathbb R$ | $|\theta|$ |
| RBF-MMD$^2$ | $2-2e^{-\theta^2/(2\sigma^2)}$ |

当 $\theta\to0$：

- JS/TV 对所有非零 $\theta$ 保持最大，不提供逐渐接近的 ground-geometric signal；
- KL 始终 infinite；
- $W_1\to0$；
- RBF-MMD $\to0$。

这就是生成模型中 support manifold 近乎不相交时，density-ratio divergence 与 geometry-aware/IPM objective 训练行为可能不同的最小反例。

> [!warning] topology 好不等于 estimator 容易
> $W_1$ 对平移给连续 signal，但高维 empirical $W_p$ 可能有严重 sample complexity；MMD 易从 samples 算，却高度依赖 kernel。理论 geometry、统计估计和 optimizer dynamics 是三件事。

## 十二、几个连接不等式

natural-log convention 下 Pinsker inequality：

$$
\boxed{
\operatorname{TV}(P,Q)
\le\sqrt{\frac12D(P\|Q)}.
}
$$

所以 small KL 保证 small TV；反向一般不成立，没有额外 lower bounds/support conditions 时，小 TV 可伴随大 KL。

对 bounded function $|g|\le M$：

$$
|E_Pg-E_Qg|
\le2M\operatorname{TV}(P,Q).
$$

对 $L$-Lipschitz $g$：

$$
|E_Pg-E_Qg|\le L W_1(P,Q).
$$

这些 inequality 告诉我们：distance 的操作意义取决于下游 test/loss class。

## 十三、Gaussian 例子：同一 pair 的不同几何

对 $P=N(\mu_p,\Sigma_p)$、$Q=N(\mu_q,\Sigma_q)$：

- KL 使用 relative covariance、Mahalanobis mean mismatch 与 log-det；方向交换会改变 inverse covariance；
- Bhattacharyya/Hellinger 是较对称的 overlap measure；
- $W_2$ 使用 Euclidean ground geometry：

$$
W_2^2(P,Q)
=\|\mu_p-\mu_q\|_2^2
+\operatorname{tr}\left[
\Sigma_p+\Sigma_q
-2(\Sigma_q^{1/2}\Sigma_p\Sigma_q^{1/2})^{1/2}
\right].
$$

[[S-2021-Su-8512-多元正态分布的KL巴氏与W距离]]提供长推导入口；奇异 covariance、matrix square root 与 empirical covariance error 需单独审计。

## 十四、finite-sample estimation 不是公式代入

### 14.1 $f$-divergence

若 densities 未知，需要 density estimation、density-ratio estimation 或 variational critic。高维 ratio estimation 困难；受限 critic 给 lower bound，不是 exact divergence。

### 14.2 Wasserstein/OT

empirical OT 直接在样本 measures 上求，但高维 convergence 可很慢；batch size、ground cost 和 outliers 影响大。entropic regularization/Sinkhorn 提升计算稳定性，却改变 objective，并引入 regularization/debiasing choices。

### 14.3 MMD

biased V-statistic 包含 diagonal terms、保证非负；unbiased U-statistic 去掉 diagonals，但 finite sample 可为负。two-sample test 还需 null calibration/permutation/asymptotic threshold。kernel 与 bandwidth 若用 test data 选择会产生选择偏差。

### 14.4 train critic

同一 data 上训练并报告 critic maximum 会 upward overfit empirical objective；而受限 class 又造成 population lower-bound bias。应使用 held-out samples、capacity control、multiple seeds 与 estimator sensitivity。

## 十五、AI 目标选择地图

| 任务 | 首选问题 | 合适对象/警告 |
|---|---|---|
| likelihood/MLE | 模型给真实数据多少 log score | forward KL/cross-entropy；需 normalized density |
| standard VI | tractable $q$ 逼近 posterior | reverse KL 来自 ELBO identity |
| two-sample test | samples 是否来自同一 law | MMD/energy/classifier test；需 calibration |
| geometry-aware generation | 小移动应是小差异吗 | Wasserstein/IPM；ground metric 决定语义 |
| bounded downstream risks | 所有 bounded tests 的差异 | TV；直接高维估计很难 |
| moment/feature matching | 哪类 functions 的 expectation 要匹配 | matching IPM/MMD function class |
| exponential-family optimization | 参数/mean coordinates 的 convex gap | Bregman/$B_A$；不是任意 measure metric |
| GAN | sample-only adversarial objective | population divergence、restricted critic 与 game surrogate 分层 |

## 十六、WGAN/f-GAN 叙事的严格边界

[[S-2019-Su-6280-Wasserstein距离与WGAN]]给出 coupling 与 dual 入口；[[S-2021-Su-8244-WGAN成功与距离近似]]提醒：

1. population $W_1(P,Q)$；
2. empirical $W_1(\widehat P,\widehat Q)$；
3. restricted neural critic optimum；
4. alternating training 达到的 objective

不是同一个数。WGAN 效果好不能反向证明第 4 层精确估计第 1 层；同样，f-GAN critic loss 改善也不证明真实 $f$-divergence 等量下降。

## 十七、常见错误与纠正

| 错误 | 为什么错 | 纠正 |
|---|---|---|
| 所有 divergence 都是 distance | 可能不对称/无 triangle | 逐项检查公理 |
| symmetric 就自动 metric | 还需 triangle | 例如 symmetrized KL 仍非 metric |
| $f$-divergence 感知样本距离 | 只看 density ratio，不带 ground cost | 若需要几何选 OT/IPM |
| Wasserstein 总比 KL 好 | sample complexity/cost choice 不同 | 按任务与估计预算选择 |
| MMD=0 总代表相同分布 | kernel 可能非 characteristic | 说明 kernel 条件 |
| critic objective 就是真 divergence | function/sample/optimization gaps | 报 population target 与 estimator |
| gradient penalty 精确保证 Lipschitz | 只在 sampled paths/points 约束 | 验证 enforcement 与 extrapolation |
| Sinkhorn 就是原 $W_p$ | entropy regularization 改 objective | 报 $\varepsilon$ 与 debiasing |
| Bregman divergence 有 DPI | 一般没有 | 只对具体结构证明 |

## 十八、选择与实现审计清单

1. 比较的是 probability measures、densities、parameters 还是 samples？
2. 需要方向性吗？
3. 支撑不相交时应 finite 还是 infinite？
4. sample-space geometry/units 是否有语义？
5. 需要 metric、weak convergence 还是 risk control？
6. function class/ground cost/kernel 是什么？
7. population quantity 能否从 samples 一致估计？
8. estimator 是 plug-in、U/V-statistic、OT solver 还是 critic bound？
9. dimension、sample size 与 convergence rate 是否匹配？
10. train/eval data 是否分开？
11. critic/metric hyperparameter 是否在 test data 选择？
12. numerical regularization 是否改变定义？
13. reduction 与单位是否可比较？
14. downstream task 是否真的由该 distance 控制？

## 十九、你现在应能独立重建的主链

$$
D_f(P\|Q)=E_Qf(dP/dQ)
\quad\xrightarrow{\text{Jensen}}\quad
D_f\ge0
\quad\xrightarrow{\text{conditional Jensen}}\quad
\text{DPI}.
$$

$$
B_F(u,v)=F(u)-F(v)-\nabla F(v)^\top(u-v),
$$

$$
\gamma_\mathcal F(P,Q)
=\sup_{g\in\mathcal F}|E_Pg-E_Qg|.
$$

三条主线分别回答 density-ratio、convex-coordinate 与 test-function/geometry 问题。下一章 INFO-10 将用这些工具研究允许 distortion 的压缩、task-relevant representation 与 model-description trade-off。

## 习题与解答

- [[习题 - f-散度、Bregman 散度与概率度量]]：15 道 A–E 分层训练；
- [[解答 - f-散度、Bregman 散度与概率度量]]：生成函数、DPI、Bregman、Wasserstein/MMD 与 GAN 审计。

## 参考来源

- Csiszár, *Information-Type Measures of Difference of Probability Distributions and Indirect Observations*, 1967；
- Nowozin, Cseke & Tomioka, [f-GAN](https://papers.neurips.cc/paper_files/paper/2016/file/cedebb6e872f539bef8c3f919874e9d7-Paper.pdf), 2016；
- Sriperumbudur et al., [Hilbert Space Embeddings and Metrics on Probability Measures](https://www.jmlr.org/papers/v11/sriperumbudur10a.html), 2010；
- Gretton et al., [A Kernel Two-Sample Test](https://www.jmlr.org/papers/v13/gretton12a.html), 2012；
- Arjovsky, Chintala & Bottou, [Wasserstein GAN](https://proceedings.mlr.press/v70/arjovsky17a), 2017；
- [[S-2018-Su-6016-fGAN与变分散度]]；
- [[S-2019-Su-6280-Wasserstein距离与WGAN]]；
- [[S-2021-Su-8244-WGAN成功与距离近似]]；
- [[S-2021-Su-8512-多元正态分布的KL巴氏与W距离]]。
